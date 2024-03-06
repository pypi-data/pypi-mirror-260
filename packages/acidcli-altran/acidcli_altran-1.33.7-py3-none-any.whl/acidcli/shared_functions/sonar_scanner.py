# Copyright Capgemini Engineering B.V..

"""SonarScanner.

Generic abstraction for working with the SonarScanner.
"""

import os
import re

import i18n
from loguru import logger

from acidcli.exceptions import CLIError
from acidcli.facility.subprocess import Subprocess


class SonarScanner:
    """SonarScanner."""

    @staticmethod
    def run(url, project_key, output, command_flags, verbose, versioning, environment, python_version=None):
        """Run.

        Runs the sonar scanner on Linux.

        :param url: SonarQube url
        :param project_key: SonarQube project key
        :param command_flags: Additional flags for sonar-scanner
        :param output: Folder where to persist logging
        :param verbose: Verbosity for running sonar-scanner
        :param versioning: Versioning object for deciding on context
        :param environment: Environment dataclass for authentication credentials
        :param python_version: Specify Python version to lower false positives
        :return: Subprocess CompletedProcess object of SonarScanner
        """
        project_version = versioning.get_semver()
        token = environment.technical_sonarqube_token

        if not versioning.is_pipeline() or token is None:
            raise CLIError(i18n.t("acidcli.pipeline.environment_variable_missing"))

        sonar_scanner_command = [
            "sonar-scanner",
            f"-Dsonar.projectKey={project_key}",
            f"-Dsonar.host.url={url}",
            "-Dsonar.qualitygate.wait=true",
            f"-Dsonar.projectVersion={project_version}",
        ]

        if python_version:
            sonar_scanner_command.append(f"-Dsonar.python.version={python_version}")

        backwards_compatible = os.environ.get("SONARQUBE_9")
        if backwards_compatible == "true":
            sonar_scanner_command.append(f"-Dsonar.login={token}")
        else:
            sonar_scanner_command.append(f"-Dsonar.token={token}")

        if command_flags:
            sonar_scanner_command.extend(command_flags)

        process = Subprocess(sonar_scanner_command, verbose=verbose, redacted=True)
        sonar_output = process.execute_pipe(output, "sonar_scanner", check_return_code=False)
        return sonar_output

    @staticmethod
    def parse_output(sonar_output):
        """Parse output.

        Handles the sonar scanner output.

        :param sonar_output: Subprocess CompletedProcess object of SonarScanner
        """
        if "You're not authorized to run analysis." in sonar_output.stdout.decode("utf-8"):
            raise CLIError(i18n.t("acidcli.sonarqube.unauthorized_exception"))

        re_search = re.search(r"View details on (.*)", sonar_output.stdout.decode("utf-8"))
        url = re_search.group(1).rstrip()

        if sonar_output.returncode != 0:
            raise CLIError(i18n.t("acidcli.sonarqube.quality_gate_failed", message=url))
        logger.info(i18n.t("acidcli.sonarqube.quality_gate_details", message=url))
