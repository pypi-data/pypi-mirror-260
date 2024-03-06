# Copyright Capgemini Engineering B.V.

"""Build Maven.

Build Maven artifacts
"""
import os

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import ProcessError
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Maven(Executable):
    """Build Maven."""

    def __init__(self):
        """__init__."""
        self.__build_settings_path = None
        self.__build_pom_path = None
        self.__output = None
        self.__verbose = None

    @print_job_info
    def execute(self, project_config, job_config):
        """Build the Maven artifacts."""
        self.__output = self._validate_parameter(job_config, "output")
        self.__verbose = self._validate_parameter(job_config, "verbose")
        self.__build_settings_path = self._validate_parameter(job_config, "build_settings_path", optional=True)
        self.__build_pom_path = self._validate_parameter(job_config, "build_pom_path", optional=True)

        self.__build_maven()

    @function_debug
    def __build_maven(self):
        """Run maven build.

        -e Produce execution error messages
        -U Forces a check for missing releases and updated snapshots on remote repositories
        -B Run in non-interactive (batch) mode (disables output color; supresses download progress)
        -Dorg.slf4j.simpleLogger.log.org.apache.maven.cli.transfer=warn Supresses download INFO messages
        """
        publish_command = [
            "mvn",
            "package",
            "-DskipTests=true",
            "-e",
            "-U",
            "-B",
            "-Dorg.slf4j.simpleLogger.log.org.apache.maven.cli.transfer=warn",
        ]
        if self.__build_settings_path:
            publish_command.extend(["-s", self.__build_settings_path])
        if self.__build_pom_path:
            publish_command.extend(["-f", self.__build_pom_path])

        with open(os.path.join(self.__output, "maven_build.log"), "w", encoding="utf-8") as maven_build_output_file:
            try:
                process = Subprocess(
                    publish_command,
                    stdout=maven_build_output_file,
                    stderr=maven_build_output_file,
                    verbose=self.__verbose,
                )
                process.execute()
            except ProcessError as error:
                raise CLIError(error) from error


# pylint: enable=too-few-public-methods
