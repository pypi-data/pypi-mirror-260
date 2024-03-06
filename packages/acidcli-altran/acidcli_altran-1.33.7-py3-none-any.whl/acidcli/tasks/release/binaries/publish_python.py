# Copyright Capgemini Engineering B.V.

"""Publish Python.

Publish Python package to the artifact store
"""
from shutil import move, Error
import i18n

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class PublishPython(Executable):
    """Publish Python."""

    def __init__(self):
        """Initialize publish Python."""
        self.upload_type = None
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Publish Python package.

        Publish Python package to configured artifact store

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["output"])

        if self.__job.parent.parent.artifact_repository_url is None:
            raise CLIError(
                "Skipping upload to artifact repository.\n"
                "If this is not intended please make sure the 'artifact_repository_url' is defined in the acidcli "
                "configuration file."
            )

        version = self._parameter_value(self.__job, "version")
        if not version.is_pipeline():
            raise CLIError(i18n.t("acidcli.release.only_allowed_to_run_in_pipeline"))

        environment = self._parameter_value(self.__job, "environment")

        username = environment.technical_user
        password = environment.technical_password

        self.__set_package_version()
        self.__configure_repository()
        self.__publish_package(username, password)
        self.__move_binaries()

    @function_debug
    def __set_package_version(self):
        """Set package version.

        Configure poetry version for publishing.
        """
        configure_version_command = [
            "poetry",
            "version",
            f"{self._parameter_value(self.__job, 'version').get_semver()}",
        ]
        process = Subprocess(configure_version_command, verbose=self._parameter_value(self.__job, "verbose"))
        process.execute_pipe(self._parameter_value(self.__job, "output"), "poetry_version")

    @function_debug
    def __configure_repository(self):
        """Configure repository.

        Configure the repository that poetry uses when publishing.
        """
        version = self._parameter_value(self.__job, "version")
        if version.is_release_candidate() or version.is_beta() or version.is_alpha():
            self.upload_type = "snapshot"
        elif version.is_release():
            self.upload_type = "release"

        upload_url = self.__job.parent.parent.artifact_repository_url.format(self.upload_type)

        configure_repository_command = [
            "poetry",
            "config",
            f"repositories.{self.upload_type}",
            f"{upload_url}",
        ]

        process = Subprocess(configure_repository_command, verbose=self._parameter_value(self.__job, "verbose"))
        process.execute_pipe(self._parameter_value(self.__job, "output"), "poetry_config")

    @function_debug
    def __publish_package(self, username, password):
        """Publish package.

        publish package to configured repository.

        :param username: username to log into repository.
        :param password: password to log into repository.
        """
        publish_package_command = [
            "poetry",
            "publish",
            "--build",
            "--repository",
            f"{self.upload_type}",
            "--username",
            f"{username}",
            "--password",
            f"{password}",
        ]

        process = Subprocess(
            publish_package_command, verbose=self._parameter_value(self.__job, "verbose"), redacted=True
        )
        poetry_publish_output = process.execute_pipe(
            self._parameter_value(self.__job, "output"), "poetry_publish", check_return_code=False
        )

        if any(
            error_code in poetry_publish_output.stdout.decode("utf-8")
            for error_code in [
                "HTTP Error 403: Forbidden",
                "HTTP Error 404: Repository not found",
                "HTTP Error 401: Unauthorized",
            ]
        ):
            raise CLIError(i18n.t("acidcli.nexus.failed_upload"))

        if "HTTP Error 400: Repository does not allow updating assets" in poetry_publish_output.stdout.decode("utf-8"):
            raise CLIError(i18n.t("acidcli.nexus.redeploy_not_allowed"))

    @function_debug
    def __move_binaries(self):
        """Move binaries.

        Move binaries to output folder.
        """
        source = "dist"

        try:
            move(
                source,
                self._parameter_value(self.__job, "output"),
            )
        except Error as error:
            raise CLIError(f"Could not move binaries {source}: {error}") from error


# pylint: enable=too-few-public-methods
