# Copyright Capgemini Engineering B.V.

"""Testing binaries.

Testing binaries using Gradle
"""
import os

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import ProcessError
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Gradle(Executable):
    """Gradle."""

    def __init__(self):
        """Initialize."""
        self.__input = None
        self.__command = None
        self.__output = None
        self.__verbose = None

    @print_job_info
    def execute(self, project_config, job_config):
        """Test units."""
        self.__input = self._validate_parameter(job_config, "input")
        self.__command = self._validate_parameter(job_config, "command")
        self.__output = self._validate_parameter(job_config, "output")
        self.__verbose = self._validate_parameter(job_config, "verbose")

        self.__test_project()

    @function_debug
    def __test_project(self):
        """Test the Gradle project."""
        gradle_test_command = ["gradle", "--project-dir", self.__input]
        gradle_test_command.extend(self.__command)

        with open(os.path.join(self.__output, "gradle_test.log"), "w", encoding="utf-8") as output_file:
            try:
                process = Subprocess(
                    gradle_test_command,
                    stdout=output_file,
                    stderr=output_file,
                    verbose=self.__verbose,
                )
                process.execute()
            except ProcessError as error:
                raise CLIError(error) from error


# pylint: enable=too-few-public-methods
