# Copyright Capgemini Engineering B.V.

"""Versioning."""
import re

import i18n
import yaml
from loguru import logger

from acidcli.exceptions import VersionError


# pylint: disable=too-few-public-methods
class VersionYml:
    """Determine version based on YML file.

    Determines the version to build
    """

    __VERSION_FILE = ".version.yml"

    def __init__(self, pipeline_model, version_data):
        """Class initializer.

        Creates a VersionYml object that contains a Version instance

        :param pipeline_model: Pipeline model
        :param version_data: version data
        """
        version_yaml = self.__load_version_yaml(pipeline_model)

        try:
            self.version = Version(
                version_yaml["MAJOR"], version_yaml["MINOR"], version_yaml["PATCH"], version_data, pipeline_model
            )
        except KeyError as error:
            raise VersionError(
                i18n.t("acidcli.versioning.key_missing", yml_key=error),
            ) from error

        logger.info(
            i18n.t(
                "acidcli.versioning.determined_project_version",
                project_name=pipeline_model.project,
                version=self.version,
            )
        )

    def __load_version_yaml(self, pipeline_model):
        """Load the version variables from the version file.

        :param pipeline_model: Pipeline model
        :return: dict with version
        """
        if pipeline_model.version_yml:
            version_file = pipeline_model.version_yml
        else:
            version_file = self.__VERSION_FILE

        try:
            with open(version_file, "r", encoding="utf-8") as config:
                return yaml.safe_load(config)
        except FileNotFoundError as error:
            raise VersionError(
                i18n.t("acidcli.versioning.version_file_missing", version_file_path=str(error).split()[-1])
            ) from error


# pylint: disable=too-few-public-methods


class Version:
    """Class to handle business logic to determine the Semantic Version."""

    __default_branch = "latest"

    def __init__(self, major, minor, patch, version_data, pipeline_model):
        """Class initializer.

        Creates a version object that returns the Semantic Version

        :param major: Major version number
        :param minor: Minor version number
        :param patch: Patch version number
        :param version_data: version data
        :param pipeline_model: pipeline model
        """
        self.__major = major
        self.__minor = minor
        self.__patch = patch
        self.__pipeline = version_data.pipeline
        self.__ci = version_data.environment
        self.__pipeline_model = pipeline_model
        self.__version_type = "alpha"
        self.__build_number = version_data.build_number
        self.__pipeline_id = version_data.pipeline_number
        self.__ci_commit_branch = version_data.branch
        self.__ci_commit_tag = version_data.tag
        self.__ref_slug = version_data.ref_slug

        self.__set_version_type()

    def __set_version_type(self):
        """__set_version_type.

        Set the version type based on the type of branch/tag
        """
        if self.__ci_commit_branch and (self.__ci_commit_tag is None):
            self.__determine_version_type_on_branch(self.__ci_commit_branch)
        elif self.__ci_commit_tag:
            self.__determine_version_type_tag(self.__ci_commit_tag)
        else:
            logger.debug(i18n.t("acidcli.versioning.no_branch_or_tag"))

    def __determine_version_type_tag(self, tag):
        """__determine_version_type_tag.

        Validates tag and sets the version type to release

        :param tag: Tag placed on commit
        """
        self.__version_type = "release"
        pattern = re.compile("^[0-9]+[.][0-9]+[.][0-9]+$")
        if pattern.match(tag) is None:
            raise VersionError(i18n.t("acidcli.versioning.invalid_tag", tag=str(tag)))

        if tag != f"{self.__major}.{self.__minor}.{self.__patch}":
            raise VersionError(
                i18n.t(
                    "acidcli.versioning.different_tag",
                    tag=str(tag),
                    version=f"{self.__major}.{self.__minor}.{self.__patch}",
                )
            )

    def __determine_version_type_on_branch(self, branch):
        """__determine_version_type_on_branch.

        Set the version type to alpha, beta or rc based on the type of branch

        :param branch: Branch of commit
        """
        if self.__is_default_branch():
            self.__version_type = "beta"
        elif re.fullmatch(r"^release/[0-9]+[.][0-9]+[.][0-9]+$", branch):
            if branch != f"release/{self.__major}.{self.__minor}.{self.__patch}":
                raise VersionError(
                    i18n.t(
                        "acidcli.versioning.different_branch",
                        found_branch=str(branch),
                        expected_branch=f"release/{self.__major}.{self.__minor}.{self.__patch}",
                    )
                )

            self.__version_type = "rc"
        else:
            self.__version_type = "alpha"

    def get_pipeline_id(self):
        """Get pipeline id.

        :return: pipeline id.
        """
        return self.__pipeline_id

    def get_semver(self):
        """get_semver.

        Build and return the semantic version.

        :return: String containing the semantic version
        """
        if self.__version_type == "release":
            semver = f"{self.__major}.{self.__minor}.{self.__patch}"
        else:
            semver = (
                f"{self.__major}.{self.__minor}.{self.__patch}-"
                f"{self.__version_type}.{self.__build_number}+{self.__pipeline_id}"
            )

        return semver

    def get_assemblyversion(self):
        """get_assemblyversion.

        Build and return the semantic version in the assemblyversion for C#.

        :return: String containing the assemblyversion
        """
        if self.__version_type == "release":
            semver = f"{self.__major}.{self.__minor}.{self.__patch}"
        else:
            semver = f"{self.__major}.{self.__minor}.{self.__patch}.{self.__build_number}"

        return semver

    def get_version_major_minor(self):
        """get_version_major_minor.

        Build and return the version in the form of major.minor.

        :return: String containing the version
        """
        major_minor_version = f"{self.__major}.{self.__minor}"

        return major_minor_version

    def get_ref_slug(self):
        """Get ref slug.

        Get Ref slug.

        :return: Ref slug
        """
        return self.__ref_slug

    def is_release(self):
        """is_release.

        Returns true if release.
        """
        return self.__version_type == "release"

    def is_release_candidate(self):
        """is_release_candidate.

        Returns true if is release candidate.
        """
        return self.__version_type == "rc"

    def is_beta(self):
        """is_beta.

        Returns true if is beta candidate.
        """
        return self.__version_type == "beta"

    def is_alpha(self):
        """is_alpha.

        Returns true if is alpha candidate.
        """
        return self.__version_type == "alpha"

    def is_pipeline(self):
        """is_pipeline.

        Returns true if acidcli running from pipeline.
        """
        return self.__pipeline

    def runs_on_gitlab_ci(self):
        """runs_on_gitlab_ci.

        Returns true if acidcli running in Gitlab CI.
        """
        return self.__ci == "Gitlab"

    def runs_on_jenkins_ci(self):
        """runs_on_jenkins_ci.

        Returns true if acidcli running in Jenkins CI.
        """
        return self.__ci == "Jenkins"

    def __is_default_branch(self):
        """__is_default_branch.

        Returns true if acidcli running from pipeline and on default branch.

        When no default_branch is set, uses self.__default_branch
        """
        if self.__pipeline:
            if self.__pipeline_model.default_branch is not None:
                return self.__ci_commit_branch == self.__pipeline_model.default_branch
            return self.__ci_commit_branch == self.__default_branch

        return False

    def __str__(self):
        """__str__.

        Overload of the __str__ builtin for pretty printing.

        :return: String containing the semantic version
        """
        return self.get_semver()
