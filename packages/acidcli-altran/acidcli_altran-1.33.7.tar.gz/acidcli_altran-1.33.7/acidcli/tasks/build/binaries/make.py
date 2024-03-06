# Copyright Capgemini Engineering B.V.

"""Building binaries.

Building binaries using make
"""
from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess, ProcessError
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Make(Executable):
    """Make."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Build make binaries.

        Run make to compile a c/c++ project

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["output"])
        self.__build_binaries()

    @function_debug
    def __build_binaries(self):
        """Build the binaries.

        Use make to build the binaries
        """
        build_command = ["make"]
        build_command.extend(self._parameter_value(self.__job, "command"))

        try:
            process = Subprocess(build_command, verbose=self._parameter_value(self.__job, "verbose"))
            process.execute_pipe(
                self._parameter_value(self.__job, "output"), "make_build.log"
            )
        except ProcessError as error:
            raise CLIError(error) from error

# pylint: enable=too-few-public-methods
