# Copyright Capgemini Engineering B.V.

"""Building binaries.

Building binaries using Gradle
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
        self.__output = None
        self.__verbose = None
        self.__version = None

    @print_job_info
    def execute(self, project_config, job_config):
        """Build binaries."""
        self.__input = self._validate_parameter(job_config, "input")
        self.__output = self._validate_parameter(job_config, "output")
        self.__verbose = self._validate_parameter(job_config, "verbose")
        self.__version = self._validate_parameter(job_config, "version")

        self.__build_project()

    @function_debug
    def __build_project(self):
        """Build the Gradle project."""
        gradle_build_command = [
            "gradle",
            "--project-dir",
            self.__input,
            f"-Pversion={self.__version.get_semver()}",
            "assemble",
        ]

        with open(os.path.join(self.__output, "gradle_build.log"), "w", encoding="utf-8") as output_file:
            try:
                process = Subprocess(gradle_build_command, stdout=output_file, stderr=output_file,
                                     verbose=self.__verbose)
                process.execute()
            except ProcessError as error:
                raise CLIError(error) from error


# pylint: enable=too-few-public-methods
