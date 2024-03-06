# Copyright Capgemini Engineering B.V.

"""Publish P2.

Publish P2 artifacts to the artifact store
"""
import json
import os
import pathlib
import re
import shutil
from urllib.parse import urlsplit

import requests
from loguru import logger
import i18n

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import ProcessError
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable

_TEMP_REPOSITORY_DOWNLOAD_DIRECTORY = os.path.join(os.getcwd(), "tmp", "acidcli-downloaded-repository")


# pylint: disable=too-few-public-methods
class PublishP2(Executable):
    """Publish P2."""

    def __init__(self):
        """__init__."""
        self.__username = None
        self.__password = None
        self.__current_branch = None
        self.__release_settings_path = os.path.join("/", "etc", "mde-release-settings.xml")
        self.__release_pom_path = os.path.join("/", "etc", "mde-release-pom.xml")
        self.__repository_path = ""
        self.__version = None
        self.__repository = None
        self.__output = None
        self.__verbose = None

    @print_job_info
    def execute(self, project_config, job_config):
        """Create and upload the P2 artifacts."""
        self.__version = self._validate_parameter(job_config, "version")
        self.__output = self._validate_parameter(job_config, "output")
        self.__verbose = self._validate_parameter(job_config, "verbose")
        self.__repository = self._validate_parameter(job_config, "repository")

        if self._validate_parameter(job_config, "repository_path", optional=True):
            self.__repository_path = f"{self._validate_parameter(job_config, 'repository_path', optional=True)}/"
        if self._validate_parameter(job_config, "release_settings_path", optional=True):
            self.__release_settings_path = self._validate_parameter(job_config, "release_settings_path", optional=True)
        if self._validate_parameter(job_config, "release_pom_path", optional=True):
            self.__release_pom_path = self._validate_parameter(job_config, "release_pom_path", optional=True)

        if not self.__version.is_pipeline():
            raise CLIError(i18n.t("acidcli.release.only_allowed_to_run_in_pipeline"))

        environment = self._validate_parameter(job_config, "environment")

        self.__username = environment.technical_user
        self.__password = environment.technical_password
        self.__current_branch = self.__version.get_ref_slug()

        publish, release = self.__get_context()

        if release:
            remote_repository_url = project_config.artifact_repository_url.format(
                self.__repository, self.__repository_path, release
            )
            remote_repository_path = f"{self.__repository_path}{release}/repository/"
            logger.info(f"Releasing to: {remote_repository_url}")
        elif publish:
            remote_repository_url = project_config.artifact_repository_url.format(
                self.__repository, self.__repository_path, publish
            )
            remote_repository_path = f"{self.__repository_path}{publish}/repository/"
            logger.info(f"Publishing to: {remote_repository_url}")

        splitted_artifact_url = urlsplit(project_config.artifact_repository_url)
        api_artifact_url = (
            f"{splitted_artifact_url.scheme}://{splitted_artifact_url.hostname}"
            f"/service/rest/v1/assets?repository={self.__repository}"
        )
        absolute_repository_project = pathlib.Path(
            os.path.join(os.getcwd(), self._validate_parameter(job_config, "repository_project"), "target")
        ).as_uri()[7:]

        try:
            shutil.rmtree(_TEMP_REPOSITORY_DOWNLOAD_DIRECTORY)
        except FileNotFoundError:
            logger.debug(f"Can not remove: {_TEMP_REPOSITORY_DOWNLOAD_DIRECTORY}")

        self.__download_artifacts(api_artifact_url, remote_repository_path, _TEMP_REPOSITORY_DOWNLOAD_DIRECTORY)

        maven_arguments = [
            f"-Dacidcli.repository.remoteUri={remote_repository_url}",
            f"-Dacidcli.repository.localDir={absolute_repository_project}",
            f"-Dacidcli.repository.localUri=file://{absolute_repository_project}",
            f"-Dacidcli.p2.mergeDir={_TEMP_REPOSITORY_DOWNLOAD_DIRECTORY}",
        ]

        self.__run_publish(maven_arguments)

    @function_debug
    def __get_context(self):
        """Get context of current commit."""
        publish = self.__current_branch
        release = None

        if self.__version.is_release():
            release = self.__version.get_version_major_minor()

        return publish, release

    @function_debug
    def __download_artifacts(self, source_url, download_path, download_location, download_pattern=".*"):
        """Download from Nexus mirror."""
        fetch_results = True
        continuation_token = None
        requests_data = None

        while fetch_results:
            if continuation_token is not None:
                requests_data = {"continuationToken": continuation_token}

            items = json.loads(
                requests.get(
                    source_url, auth=(self.__username, self.__password), params=requests_data, timeout=30
                ).content
            )

            if items["continuationToken"] is None:
                fetch_results = False
            else:
                continuation_token = items["continuationToken"]

            for item in items["items"]:
                item_path = item["path"]
                if item_path.startswith(download_path):
                    len_download_path = len(download_path)
                    item_path = item_path[len_download_path:]
                    if re.match(download_pattern, item_path):
                        path = os.path.join(download_location, item_path)
                        try:
                            os.makedirs(pathlib.Path(path).parent)
                        except FileExistsError:
                            logger.debug(f"Cannot create directory: {pathlib.Path(path).parent}, already exists")

                        with open(path, "wb") as output_file:
                            download_file = requests.get(
                                item["downloadUrl"], auth=(self.__username, self.__password), timeout=30
                            )
                            output_file.write(download_file.content)

    @function_debug
    def __run_publish(self, maven_arguments):
        """Run P2 publish.

        -e Produce execution error messages
        -U Forces a check for missing releases and updated snapshots on remote repositories
        -B Run in non-interactive (batch) mode (disables output color; supresses download progress)
        -Dorg.slf4j.simpleLogger.log.org.apache.maven.cli.transfer=warn Supresses download INFO messages
        """
        publish_command = [
            "mvn",
            "deploy",
            "-s",
            self.__release_settings_path,
            "-f",
            self.__release_pom_path,
            *maven_arguments,
            "-e",
            "-U",
            "-B",
            "-Dorg.slf4j.simpleLogger.log.org.apache.maven.cli.transfer=warn",
        ]

        with open(
            os.path.join(self.__output, "maven_publish.log"), "w", encoding="utf-8"
        ) as maven_publish_output_file:
            try:
                process = Subprocess(
                    publish_command,
                    stdout=maven_publish_output_file,
                    stderr=maven_publish_output_file,
                    verbose=self.__verbose,
                    redacted=True,
                )
                process.execute()
            except ProcessError as error:
                raise CLIError(error) from error


# pylint: enable=too-few-public-methods
