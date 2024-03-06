# Copyright Capgemini Engineering B.V.

"""Publish Nuget.

Publish Nuget packages to the artifact store
"""
import glob
import os
from urllib.parse import urlparse
import i18n

from loguru import logger

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess
from acidcli.facility.upload import Upload
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class PublishNuget(Executable):
    """Publish Nuget."""

    def __init__(self):
        """Initialize publish Nuget."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Publish Nuget package.

        Create and upload the Nuget package.

        :param job: job model object with job configuration
        """
        self.__job = job
        environment = self._parameter_value(self.__job, "environment")

        self._required_parameters_available(self.__job, ["output"])
        self._required_list_parameters_available(self.__job, ["names"])
        if self.__job.parent.parent.artifact_repository_url is None:
            raise CLIError(i18n.t("acidcli.release.make_sure_artifact_repository_url_is_defined"))

        version = self._parameter_value(self.__job, "version")
        if not version.is_pipeline():
            raise CLIError(i18n.t("acidcli.release.only_allowed_to_run_in_pipeline"))

        project_names = self._parameter_value(self.__job, "names")
        for project_name in project_names:
            self.__create_package(project_name)
        for project_name in project_names:
            self.__upload_package(project_name, environment)

    @function_debug
    def __create_package(self, project_name):
        """Create the Nuget package.

        :param project_name: create the nuget package of this project
        """
        version = self._parameter_value(self.__job, "version")
        output = self._parameter_value(self.__job, "output")
        build_type = self._parameter_value(self.__job, "type")

        create_package_command = [
            "nuget",
            "pack",
            project_name,
            "-Properties",
            f"Configuration={build_type}",
            "-Version",
            version.get_semver(),
            "-OutputDirectory",
            os.path.join(output, project_name),
        ]

        process = Subprocess(
            create_package_command, verbose=self._parameter_value(self.__job, "verbose"), redacted=True
        )
        process.execute_pipe(output, "nuget")

    @function_debug
    def __upload_package(self, project_name, environment):
        """Upload the Nuget package.

        :param project_name: upload the nuget package of this project
        :param environment: environment object
        """
        version = self._parameter_value(self.__job, "version")

        url = self.__job.parent.parent.artifact_repository_url.format(
            "release" if version.is_release() else "snapshot"
        )
        output = self._parameter_value(self.__job, "output")

        packages = glob.glob(os.path.join(output, project_name, "*.nupkg"))

        if len(packages) < 1:
            raise CLIError(i18n.t("acidcli.publish_nuget_pages.no_nuget_package_found"))
        if len(packages) > 1:
            raise CLIError(
                i18n.t(
                    "acidcli.publish_nuget_pages.found_more_than_one_nuget_package", number_of_packages=len(packages)
                )
            )

        package_to_publish = packages[0]

        url_parsed = urlparse(url)

        try:
            repository = url_parsed.path.split("/")[2]
        except IndexError as artifact_path_error:
            raise CLIError(i18n.t("acidcli.publish_nuget_pages.unable_to_parse_artifact_url")) from artifact_path_error

        nexus_url = i18n.t(
            "acidcli.nexus_url",
            scheme=url_parsed.scheme,
            hostname=url_parsed.hostname,
            repository=repository,
            folder=project_name,
        )
        with open(package_to_publish, "rb") as file:
            files = {"package": (package_to_publish, file)}

            upload = Upload(username=environment.technical_user, password=environment.technical_password)
            upload.upload_nuget_package(url, files)

        logger.info(
            i18n.t(
                "acidcli.clickable_path.simple_url",
                name=os.path.basename(package_to_publish),
                url=nexus_url,
                error_message="Successfully published",
            ),
        )


# pylint: enable=too-few-public-methods
