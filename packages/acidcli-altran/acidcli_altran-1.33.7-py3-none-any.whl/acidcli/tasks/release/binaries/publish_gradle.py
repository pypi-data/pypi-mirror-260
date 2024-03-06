# Copyright Capgemini Engineering B.V.

"""Publish Gradle.

Publish Gradle(Maven type) package to the artifact store
"""
import os

import i18n

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import ProcessError
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class PublishGradle(Executable):
    """Publish Gradle."""

    def __init__(self):
        """Initialize publish Gradle."""
        self.__input = None
        self.__output = None
        self.__password = None
        self.__username = None
        self.__verbose = None
        self.__version = None

    @print_job_info
    def execute(self, project_config, job_config):
        """Create and upload the Python package."""
        self.__input = self._validate_parameter(job_config, "input")
        self.__output = self._validate_parameter(job_config, "output")
        self.__verbose = self._validate_parameter(job_config, "verbose")
        self.__version = self._validate_parameter(job_config, "version")

        environment = self._validate_parameter(job_config, "environment")
        self.__username = environment.technical_user
        self.__password = environment.technical_password

        if project_config.artifact_repository_url is None:
            raise CLIError(
                "Skipping upload to artifact repository.\n"
                "If this is not intended please make sure the 'artifact_repository_url' is defined in the acidcli "
                "configuration file."
            )

        if not self.__version.is_pipeline():
            raise CLIError(i18n.t("acidcli.release.only_allowed_to_run_in_pipeline"))

        upload_url, package_name = self.__get_repository(
            project_config,
        )

        self.__publish_package(upload_url, package_name)

    @function_debug
    def __get_repository(self, project_config):
        """Get package destination."""
        if self.__version.is_release_candidate() or self.__version.is_beta() or self.__version.is_alpha():
            upload_type = "snapshot"
            package_name = f"{self.__version.get_semver()}-SNAPSHOT"
        elif self.__version.is_release():
            upload_type = "release"
            package_name = self.__version.get_semver()

        return project_config.artifact_repository_url.format(upload_type), package_name

    @function_debug
    def __publish_package(self, upload_url, package_name):
        """Publish package to destination."""
        publish_package_command = [
            "gradle",
            "--project-dir",
            self.__input,
            f"-Pversion={package_name}",
            f"-PTECHNICAL_USER={self.__username}",
            f"-PTECHNICAL_PASSWORD={self.__password}",
            f"-PPUBLISH_URL={upload_url}",
            "publish",
        ]

        with open(
            os.path.join(self.__output, "gradle_publish.log"), "w", encoding="utf-8"
        ) as gradle_publish_output_file:
            try:
                sub_process = Subprocess(
                    publish_package_command,
                    stdout=gradle_publish_output_file,
                    stderr=gradle_publish_output_file,
                    verbose=self.__verbose,
                    redacted=True,
                )
                sub_process.execute()
            except ProcessError as error:
                raise CLIError(error) from error


# pylint: enable=too-few-public-methods
