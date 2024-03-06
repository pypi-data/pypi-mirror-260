# Copyright Capgemini Engineering B.V.

"""Subprocess launcher.

Subprocess wrapper for acid cli tasks, pre- and post conditions.
"""
from os.path import join
from shutil import which
from time import strftime
from subprocess import CalledProcessError, DEVNULL, PIPE, STDOUT, Popen, TimeoutExpired, check_call, run

from loguru import logger
import i18n


class ProcessError(Exception):
    """Process error.

    Something went wrong executing the Python subprocess call
    """

    def __init__(self, msg=None, command_output=None):
        """Init Process error."""
        super().__init__(msg)
        self.command_output = command_output


class SubprocessRuntimeError(Exception):
    """Runtime error.

    Something went wrong before or after the Python subprocess call
    """


# pylint: disable=too-few-public-methods
class Subprocess:
    """Class to handle the execution of all command line tooling.

    User friendly subprocess wrapper, providing useful and informative
    error messages to the user in case of failures.
    """

    def __init__(
        self, command, stdout=DEVNULL, stderr=DEVNULL, verbose=0, timeout=None, redacted=False
    ):  # pylint: disable=R0913
        """Class initializer.

        Creates a command object that can be executed.

        :param command: Command to execute on operating system in tuple format
        :param stdout: Optional location to redirect standard output stream
        :param stderr: Optional location to redirect error output stream
        :param verbose: Optional verbosity level of the processes output
        :param timeout: Optional variable providing command timeout
        :param redacted: Optional variable for redacting all command arguments
        """
        if not isinstance(command, (list, tuple)):
            raise SubprocessRuntimeError(f"Command ({command}) is not of type list or tuple.")

        self.base_command = command[0]
        self.command = command
        self.stdout = stdout
        self.stderr = stderr
        self.timeout = timeout
        self.verbose = verbose
        self.redacted = redacted

        command[0] = self.__which()

    def __which(self):
        """Check if tool is available.

        Check if the tool that is to be executed is installed on the system.

        :return: tool location (Full path)
        """
        abspath = which(self.base_command)

        if not abspath:
            raise SubprocessRuntimeError(i18n.t("acidcli.subprocess.not_installed", command=self.base_command))

        logger.debug(f"Located `{self.base_command}` in `{abspath}`")
        return abspath

    def execute(self):
        """Execute the command.

        Execute the command as defined in the object. Raising informative exceptions
        in case of an `execution error` or `command timeout`.
        """
        if self.redacted:
            logger.debug(logger.debug(f"Starting call: {self.base_command} [REDACTED]"))
        else:
            logger.debug(f"Starting call: {self.command}")
        stdout = self.stdout
        stderr = self.stderr

        if self.verbose == 2:
            stderr = None
        elif self.verbose >= 3:
            stdout = None
            stderr = None

        try:
            check_call(
                self.command,
                stdout=stdout,
                stderr=stderr,
                shell=False,
                timeout=self.timeout,
            )
        except CalledProcessError as error:
            raise ProcessError(f"{self.base_command} returned a non-zero exit status {error.returncode}") from error
        except TimeoutExpired as error:
            raise ProcessError(f"{self.base_command} timed out after {error.timeout} seconds") from error

    def execute_async(self):
        """Execute the command asynchronously.

        Execute the command asynchronously as defined in the object and don't wait on or check any return value.
        Raising informative exceptions in case of an `Operating System error` or `Value error`.
        """
        if self.redacted:
            logger.debug(logger.debug(f"Starting asynchronous call: {self.base_command} [REDACTED]"))
        else:
            logger.debug(f"Starting asynchronous call: {self.command}")
        try:
            Popen(self.command)
        except ValueError as error:
            raise ProcessError(f"{self.base_command} has an invalid argument: {error.args}") from error
        except OSError as error:
            raise ProcessError(
                f"{self.base_command} returned an OS error: {error.errno} '{error.strerror}' {error.filename}"
            ) from error

    def execute_pipe(self, output_directory, filename, check_return_code=True, disable_logfile=False):
        """Execute command returning stdout as string.

        Execute the command as defined in the object returning process
        information. This command will always produce a log file with the
        output of the executed command. With the possibility to raise an
        informative exception in case of a non-zero return code.

        :param output_directory: log file output directory
        :param filename log file filename
        :param check_return_code: Optional raise exception with non-zero return code
        :param disable_logfile: Optional, if set to true, the output is not written to a logfile
        :return: Subprocess CompletedProcess object
        """
        if self.redacted:
            logger.debug(logger.debug(f"Starting call: {self.base_command} [REDACTED]"))
        else:
            logger.debug(f"Starting call: {self.command}")

        command_output = run(
            self.command,
            stdout=PIPE,
            stderr=STDOUT,
            shell=False,
            check=False,
            timeout=self.timeout,
        )

        if not disable_logfile:
            self.__write_log_file(output_directory, filename, command_output)

        if self.verbose >= 3:
            logger.opt(raw=True).debug(command_output.stdout.decode("utf-8"))

        if command_output.returncode != 0 and check_return_code:
            raise ProcessError(
                f"{self.base_command} returned a non-zero exit status {command_output.returncode}",
                command_output=command_output.stdout.decode("utf-8"),
            )

        return command_output

    @staticmethod
    def __write_log_file(output_directory, filename, command_output):
        """Write process data to log file.

        Write command output to unique (timestamped) log file based on the
        provided `output_directory` and `filename`.

        :param output_directory: log file output directory
        :param filename log file filename
        :param command_output: Optional raise exception with non-zero return code
        """
        try:
            with open(join(output_directory, f"{filename}_{strftime('%Y%m%d-%H%M%S')}.log"), "wb") as file:
                file.write(command_output.stdout)
        except FileNotFoundError as exception:
            raise SubprocessRuntimeError(
                f"Unable to open ('{exception.filename}') and write results.\n"
                f"Please use preconditions to enforce: ['OutputDirectoryExists', 'OutputDirectoryIsEmpty']."
            ) from exception


# pylint: enable=too-few-public-methods
