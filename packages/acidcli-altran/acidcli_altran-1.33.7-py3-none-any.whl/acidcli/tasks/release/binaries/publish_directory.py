# Copyright Capgemini Engineering B.V.

"""Publish Directory.

Publish directory binaries to the artifact store
"""
import os
import shutil
import i18n

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.upload import Upload
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class PublishDirectory(Executable):
    """Publish Directory."""

    def __init__(self):
        """Initialize."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Execute.

        Create and upload the directory binaries.

        :param job: Job model
        """
        self.__job = job
        environment = self._parameter_value(self.__job, "environment")

        self._required_parameters_available(job, ["input", "output"])
        if self.__job.parent.parent.artifact_repository_url is None:
            raise CLIError(i18n.t("acidcli.release.make_sure_artifact_repository_url_is_defined"))

        version = self._parameter_value(self.__job, "version")
        if not version.is_pipeline():
            raise CLIError(i18n.t("acidcli.release.only_allowed_to_run_in_pipeline"))

        archive_name = f"{self.__job.parent.parent.project}-{version.get_semver()}"

        self.__create_package(
            archive_name, self._parameter_value(self.__job, "input"), self._parameter_value(self.__job, "output")
        )

        self.__upload_package(archive_name, self._parameter_value(self.__job, "output"), version, environment)

    @function_debug
    def __create_package(self, archive_name, input_dir, output_dir):
        """Create package.

        Create the directory binary package.

        :param archive_name: Name of archive object
        :param input_dir: input directory
        :param output_dir: path to store archive object
        """
        shutil.make_archive(os.path.join(output_dir, archive_name), "zip", input_dir)

    @function_debug
    def __upload_package(self, archive_name, output_dir, version, environment):
        """Upload package.

        Upload the directory output package.

        :param archive_name: Name of archive object
        :param output_dir: path to store archive object
        :param version: version object
        :param environment: environment object
        """
        filename = os.path.join(output_dir, f"{archive_name}{'.zip'}")

        repository_url = self.__job.parent.parent.artifact_repository_url.format(
            "release" if version.is_release() else "snapshot"
        )
        url = f"{repository_url}{self.__job.parent.parent.project}/{archive_name}.zip"

        with open(filename, "rb") as file:
            upload = Upload(username=environment.technical_user, password=environment.technical_password)
            upload.upload_file(url, file.read())


# pylint: enable=too-few-public-methods
