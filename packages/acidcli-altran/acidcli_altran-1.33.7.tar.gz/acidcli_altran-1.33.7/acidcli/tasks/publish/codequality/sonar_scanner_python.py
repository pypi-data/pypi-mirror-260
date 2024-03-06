# Copyright Capgemini Engineering B.V.

"""SonarScanner code quality.

CodeQuality checks by sonar scanner
"""

import i18n

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import print_job_info
from acidcli.tasks.executable import Executable
from acidcli.shared_functions.sonar_scanner import SonarScanner


# pylint: disable=too-few-public-methods
class SonarScannerPython(Executable):
    """SonarScannerPython."""

    def __init__(self):
        """Init."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check code quality.

        Publish Python to SonarQube using SonarScanner.
        """
        self.__job = job
        if self.__job.parent.parent.sonarqube_url is None:
            raise CLIError(
                i18n.t(
                    "acidcli.parameter.missing",
                    task=self.__class__.__name__,
                    parameter="sonarqube_url",
                )
            )

        if self.__job.parent.parent.sonarqube_project_key is None:
            raise CLIError(
                i18n.t(
                    "acidcli.parameter.missing",
                    task=self.__class__.__name__,
                    parameter="sonarqube_project_key",
                )
            )

        if self._parameter_value(self.__job, "python_version"):
            python_version = self._parameter_value(self.__job, "python_version")
        else:
            python_version = "3.7,3.8,3.9,3.10,3.11"

        sonarqube_result = SonarScanner.run(
            self.__job.parent.parent.sonarqube_url,
            self.__job.parent.parent.sonarqube_project_key,
            self._parameter_value(self.__job, "output"),
            self._parameter_value(self.__job, "config"),
            self._parameter_value(self.__job, "verbose"),
            self._parameter_value(self.__job, "version"),
            self._parameter_value(self.__job, "environment"),
            python_version=python_version,
        )
        SonarScanner.parse_output(sonarqube_result)


# pylint: enable=too-few-public-methods
