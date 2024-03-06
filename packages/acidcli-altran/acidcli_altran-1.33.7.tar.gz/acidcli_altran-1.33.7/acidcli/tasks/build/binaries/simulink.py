# Copyright Capgemini Engineering B.V.

"""Building binaries.

Building binaries using Simulink
"""

from itertools import tee, islice, zip_longest
import i18n
from loguru import logger

from acidcli.facility.decorators import print_job_info, function_debug
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable
from acidcli.facility import ProcessError
from acidcli.exceptions import CLIError
from acidcli.quality_gate import QualityGate


class Simulink(Executable):
    """Simulink Build Binaries."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Build binaries."""
        self.__job = job
        self._required_parameters_available(self.__job, ["config"])
        output = self.__build_binaries()

        warnings = self.__parse_warnings(output.stdout.decode("utf-8"))
        warnings = self.__strip_warnings(warnings)
        self.__print_warnings(warnings)

        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, "buildWarnings", len(warnings), mandatory=True)

    @function_debug
    def __build_binaries(self):
        """Run build script to build the binaries.

        Build Simulink binaries.

        :return: Process object.
        """
        build_simulink_command = ["matlab", "-nodesktop", "-batch",
                                  f'"run(\'{self._parameter_value(self.__job, "config")}\')"']
        process = Subprocess(build_simulink_command, verbose=self._parameter_value(self.__job, "verbose"))
        try:
            return process.execute_pipe(self._parameter_value(self.__job, "output"), "simulink_build")
        except ProcessError as error:
            raise CLIError(i18n.t("acidcli.simulink_errors_occurred",
                                  script=self._parameter_value(self.__job, "config"),
                                  errors=self.__parse_command_output_error(error.command_output)))\
                from error

    @staticmethod
    @function_debug
    def __parse_command_output_error(stdout):
        """Parse command output error.

        Parse errors from Matlab invocation.

        :param: stdout: stdout to search true.
        :return: String with found errors.
        """
        stdout_lines = stdout.splitlines()
        found_errors = []
        for num, line in enumerate(stdout_lines, 0):
            if "Error in" in line:
                found_errors.extend(stdout_lines[num:num+2])
                found_errors.append("")
            elif "Error using" in line or \
                    ("requires a" in line and "license" in line):
                found_errors.append(line)
                found_errors.append("")
        return "\n".join(found_errors)

    @function_debug
    def __parse_warnings(self, stdout):
        r"""Parse warnings.

        Parse warnings from Matlab invocation.
        If a warning spans multiple lines, it will be added as a single warning.

        Function iterates over stdout to find warnings.

        Looks for "[\x08Warning" as start of warning.
        Looks for warning endings in __is_line_ending funciton.

        :param: stdout: stdout to search true.
        :return: List with warnings.
        """
        stdout_lines = stdout.splitlines()
        found_warnings = []
        in_warning = False

        concat_warning = ""
        for current_line, next_line in self.__look_ahead(stdout_lines):
            if "[\x08Warning" in current_line:
                in_warning = True
            if in_warning:
                concat_warning = concat_warning + current_line

                if self.__is_line_ending(current_line, next_line):
                    found_warnings.append(concat_warning)
                    in_warning = False
                    concat_warning = ""
        return found_warnings

    @staticmethod
    def __is_line_ending(current_line, next_line):
        r"""Is line ending.

        Checks for warning line ending.
        Looks for "]\x08" as end of warning.

        Can handle "]\x08" being split out over next line as overflow. This is handle by detecting
        "]" at the end of a line and "\x08" at the beginning of the next line.

        :param: current_line: current log line.
        :param: next_line: upcomming log line.
        :return: true if ending in current line or ending split over current and next line.
        """
        if "]\x08" in current_line:
            return True
        if next_line is not None:
            if current_line.endswith("]") and next_line.startswith("\x08"):
                return True

        return False

    @staticmethod
    def __strip_warnings(warnings):
        r"""Strip warnings.

        Removes "[\x08Warning: " from beginning of warning (including space).
        Removes "]\x08 " from end of warning (including space).
        Removes "]\x08" from end of warning (excluding space).

        :param: warnings: warnings to strip.
        :return: list with stripped warnings.
        """
        stripped_warnings = []

        for warning in warnings:
            stripped_warning = warning

            if stripped_warning.startswith("[\x08Warning"):
                stripped_warning = stripped_warning[11:]
            if stripped_warning.endswith("]\x08 "):
                stripped_warning = stripped_warning[:-3]
            if stripped_warning.endswith("]\x08"):
                stripped_warning = stripped_warning[:-2]

            stripped_warnings.append(stripped_warning)

        return stripped_warnings

    @staticmethod
    @function_debug
    def __print_warnings(warnings):
        """Print warnings.

        Print warnings to logger as Warn if there are warnings.

        :param: warnings: warnings to print.
        :return: List with warnings.
        """
        if warnings:
            for line in warnings:
                logger.warning(line)

    @staticmethod
    @function_debug
    def __look_ahead(iterable):
        """Look ahead.

        Returns current item + next item in iterable.

        https://stackoverflow.com/a/4197869

        :param: iterable: iterable to look into.
        :return: Current item, next iterable item.
        """
        items, nexts = tee(iterable, 2)
        nexts = islice(nexts, 1, None)
        return zip_longest(items, nexts)
# pylint: enable=too-few-public-methods
