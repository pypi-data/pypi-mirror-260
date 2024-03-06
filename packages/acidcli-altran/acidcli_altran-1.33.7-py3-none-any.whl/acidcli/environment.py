# Copyright Capgemini Engineering B.V.

"""Acidcli environment data.

Environments variables of different CI environments are abstracted into a dataclass with a common layout.

Currently Gitlab CI and Jenkins is supported.

Orchestrates the loading of non versioning related environment variable data into a EnvironmentData dataclass.
Orchestrates the version class to load versioning related environment variable data.
"""
from dataclasses import dataclass
import os
from re import sub
from datetime import datetime, timezone
from typing import Optional

from acidcli.versioning import VersionYml


@dataclass
class VersioningData:
    """Versioning data dataclass."""

    environment: Optional[str] = None
    pipeline: Optional[bool] = False
    tag: Optional[str] = None
    branch: Optional[str] = None
    ref_slug: Optional[str] = None
    pipeline_number: Optional[int] = 0
    build_number: Optional[int] = 0


@dataclass
class EnvironmentData:
    """Environment data dataclass."""

    technical_user: Optional[str] = None
    technical_password: Optional[str] = None
    technical_tenant: Optional[str] = None
    technical_api_key: Optional[str] = None
    technical_sonarqube_token: Optional[str] = None


# pylint: disable=too-few-public-methods
class EnvironmentLoader:
    """EnvironmentLoader.

    Orchestrates loading of versioning and non versioning environment data
    """

    environment = None
    version = None

    def __init__(self, pipeline_model):
        """Init.

        Orchestrates creation of version object and EnvironmentData dataclass.

        :param pipeline_model: pipeline model
        """
        if self.__runs_on_local():
            self.version = VersionYml(pipeline_model, self.__get_local_versioning_data()).version
        elif self.__runs_on_gitlab_ci():
            self.version = VersionYml(pipeline_model, self.__get_gitlab_ci_versioning_data()).version
        elif self.__runs_on_jenkins_ci():
            self.version = VersionYml(pipeline_model, self.__get_jenkins_ci_versioning_data()).version

        self.environment = self.__get_environment_data()

    @staticmethod
    def __get_local_versioning_data():
        """Get local versioning data.

        Gets the following properties from the Gitlab CI environment:

        environment: `Local` for local environment
        pipeline: False
        tag: None
        branch: None
        ref_slug: None
        pipeline_number: 0
        build_number: 0

        :return: versioning_data dict when running in Gitlab CI environment
        """
        versioning_data = VersioningData(
            environment="Local",
        )

        return versioning_data

    def __get_gitlab_ci_versioning_data(self):
        """Get gitlab ci versioning data.

        Gets the following properties from the Gitlab CI environment:

        environment: `Gitlab` for Gitlab environment
        pipeline: True
        tag: None if no tag placed, otherwise tag value is returned
        branch: None if tag is placed, otherwise branch value is returned
        ref_slug: see __get_versioning_ref_slug() docstring
        pipeline_number: increasing number, unique over the whole Gitlab instance. `0` if not found
        build_number: increasing number unique over a single project. `0` if not found

        :return: versioning_data dict when running in Gitlab CI environment
        """
        versioning_data = VersioningData(environment="Gitlab", pipeline=True, tag=os.environ.get("CI_COMMIT_TAG"))

        if not versioning_data.tag:
            versioning_data.branch = os.environ.get("CI_COMMIT_REF_NAME")

        versioning_data.ref_slug = self.__get_versioning_ref_slug(os.environ.get("CI_COMMIT_REF_NAME"))

        versioning_data.pipeline_number = int(os.environ.get("CI_PIPELINE_ID", 0))

        versioning_data.build_number = int(os.environ.get("CI_PIPELINE_IID", 0))

        return versioning_data

    def __get_jenkins_ci_versioning_data(self):
        """Get jenkins ci versioning data.

        Gets the following properties from the Jenkins CI environment:

        environment: `Jenkins` for Gitlab environment
        pipeline: True
        tag: None if no tag placed, otherwise tag value is returned
        branch: None if tag is placed, otherwise branch value is returned
        ref_slug: see __get_versioning_ref_slug() docstring
        pipeline_number: increasing number where each new branch starts counting from 1 again. `0` if not found
        build_number: timestamp in the `yyyymmddhhmmss` format. UTC time. `0` if not found

        Timestamp is divided by 1000 since fromtimestamp() can only handle epoch in seconds, not epoch in milliseconds.
        Datetime is forced to UTC timezone. Datetime object is timezone aware, the string resulting from strftime()
        not.
        Therefore, if UTC timezone is not forced and the server timezone changes, it will be impossible to parse all
        build_numbers string back to datetime objects. By forcing UTC timezone, all strftime() results will always be
        in UTC format.

        :return: versioning_data dict when running in Jenkins CI environment
        """
        versioning_data = VersioningData(environment="Jenkins", pipeline=True, tag=os.environ.get("TAG_NAME"))

        if not versioning_data.tag:
            versioning_data.branch = os.environ.get("BRANCH_NAME")

        versioning_data.ref_slug = self.__get_versioning_ref_slug(os.environ.get("BRANCH_NAME"))

        versioning_data.pipeline_number = int(os.environ.get("BUILD_ID", 0))

        if "BUILD_START_TIMESTAMP" in os.environ:
            versioning_data.build_number = os.environ.get("BUILD_START_TIMESTAMP")
            timestamp = int(versioning_data.build_number)
            date_time = datetime.fromtimestamp(timestamp / 1000.0, tz=timezone.utc)
            versioning_data.build_number = int(date_time.strftime("%Y%m%d%H%M%S"))
        else:
            versioning_data.build_number = 0

        return versioning_data

    @staticmethod
    def __get_environment_data():
        """Get environment data.

        Gets the following properties from the environment data:

        technical_user: env TECHNICAL_USER
        technical_password: env TECHNICAL_PASSWORD
        technical_tenant: env TECHNICAL_TENANT
        technical_api_key: env TECHNICAL_API_KEY
        technical_sonarqube_token: env TECHNICAL_SONARQUBE_TOKEN

        :return: environment_data dict
        """
        environment_data = EnvironmentData(
            technical_user=os.environ.get("TECHNICAL_USER"),
            technical_password=os.environ.get("TECHNICAL_PASSWORD"),
            technical_tenant=os.environ.get("TECHNICAL_TENANT"),
            technical_api_key=os.environ.get("TECHNICAL_API_KEY"),
            technical_sonarqube_token=os.environ.get("TECHNICAL_SONARQUBE_TOKEN"),
        )

        return environment_data

    @staticmethod
    def __runs_on_local():
        """Run on locally.

        Checks if running locally.

        :return: True if running on local, otherwise False
        """
        if os.environ.get("CI") == "true":
            return False

        return True

    @staticmethod
    def __runs_on_gitlab_ci():
        """Run on jenkins ci.

        Checks if running on Jenkins CI.

        :return: True if running on Jenkins CI, otherwise False
        """
        if os.environ.get("CI") == "true" and os.environ.get("GITLAB_CI") == "true":
            return True

        return False

    @staticmethod
    def __runs_on_jenkins_ci():
        """Run on jenkins ci.

        Checks if running on Jenkins CI.

        :return: True if running on Jenkins CI, otherwise False
        """
        if os.environ.get("CI") == "true" and os.environ.get("JENKINS_URL") is not None:
            return True

        return False

    @staticmethod
    def __get_versioning_ref_slug(ref):
        """Get versioning ref slug.

        Ref slug is lowercase, shortened to 63 chars and everything except 0-9 and a-z replaced with `-`.
        No leading/trailing `-` chars

        Use in URL and hostnames.

        :param ref: ref to convert to slug
        :return: ref converted to slug
        """
        slug = None

        if ref:
            slug = ref[0:63]
            slug = slug.lower()
            slug = sub("[^a-z0-9]", "-", slug)
            slug = slug.strip("-")

        return slug


# pylint: disable=too-few-public-methods
