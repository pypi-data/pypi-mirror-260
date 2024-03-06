# Copyright Capgemini Engineering B.V.

"""LinesOfCode.

Lines of code counter
"""
from os.path import join

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class LinesOfCode(Executable):
    """LinesOfCode."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Count lines of code.

        Count the lines of code in a file using cloc

        :param job: job model object with job configuration.
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["output"])

        for code_type in self.__job.parent.parent.code_locations:
            self.__count_lines_of_code(code_type.directories, code_type.name)

    @function_debug
    def __count_lines_of_code(self, directories, code_type):
        """Count lines of code.

        Run cloc as a subprocess for the provided directories.

        :param directories: list of the directories that should be checked by cloc.
        :param code_type: string which generalizes the type of code found in the provided directories.

        :return: immutable bytes object containing the cloc output.
        """
        filename = f"cloc_{code_type}.json"
        cloc_command = [
            "cloc",
            "--by-file-by-lang",
            "--json",
            f"--report-file={join(self._parameter_value(self.__job, 'output'), filename)}",
        ]
        cloc_command.extend(directories)

        process = Subprocess(cloc_command, verbose=self._parameter_value(self.__job, "verbose"))
        cloc_output = process.execute_pipe(self._parameter_value(self.__job, "output"), f"cloc_{code_type}")
        return cloc_output.stdout


# pylint: enable=too-few-public-methods
