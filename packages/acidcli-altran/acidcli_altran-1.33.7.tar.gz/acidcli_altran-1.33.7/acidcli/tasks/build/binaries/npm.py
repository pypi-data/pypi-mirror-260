# Copyright Capgemini Engineering B.V.

"""Building binaries.

Building binaries using npm
"""
import os
import re

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import ProcessError
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Npm(Executable):
    """Npm."""

    @print_job_info
    def execute(self, project_config, job_config):
        """Build binaries."""
        self.__set_version(job_config)
        self.__build_project(job_config)
        self.__arm_quality_gates(job_config)

    @function_debug
    def __set_version(self, job_config):
        """Adjust the version info of the npm project."""
        npm_version_command = ["npm", "version", "--no-git-tag-version",
                               str(self._validate_parameter(job_config, "version")),
                               "--allow-same-version"]

        try:
            process = Subprocess(npm_version_command,
                                 verbose=self._validate_parameter(job_config, 'verbose'))
            process.execute()
        except ProcessError as error:
            raise CLIError(error) from error

    @function_debug
    def __build_project(self, job_config):
        """Build the npm project."""
        npm_install_command = ["npm", "run"]
        npm_install_command.extend(self._validate_parameter(job_config, "command").split(" "))

        with open(
                os.path.join(self._validate_parameter(job_config, "output"), "npm_build.log"), "w", encoding="utf-8"
        ) as output_file:
            try:
                process = Subprocess(npm_install_command, stdout=output_file, stderr=output_file,
                                     verbose=self._validate_parameter(job_config, 'verbose'))
                process.execute()
            except ProcessError as error:
                raise CLIError(error) from error

    @function_debug
    def __arm_quality_gates(self, job_config):
        """Arm the quality gates."""
        with open(
                os.path.join(self._validate_parameter(job_config, "output"), "npm_install.log"), encoding="utf-8"
        ) as input_file:
            npm_install = input_file.read()

            low_vulnerabilities_count = 0
            low_vulnerabilities_search = re.search(r"([0-9]+) low", npm_install)
            if low_vulnerabilities_search:
                low_vulnerabilities_count = int(low_vulnerabilities_search.group(1))

            QualityGate.find_and_update_quality_gate(
                job_config.quality_gates, "LowVulnerabilities",
                low_vulnerabilities_count,
            )

            moderate_vulnerabilities_count = 0
            moderate_vulnerabilities_search = re.search(r"([0-9]+) moderate", npm_install)
            if moderate_vulnerabilities_search:
                moderate_vulnerabilities_count = int(moderate_vulnerabilities_search.group(1))

            QualityGate.find_and_update_quality_gate(
                job_config.quality_gates, "ModerateVulnerabilities",
                moderate_vulnerabilities_count,
            )

            high_vulnerabilities_count = 0
            high_vulnerabilities_search = re.search(r"([0-9]+) high", npm_install)
            if high_vulnerabilities_search:
                high_vulnerabilities_count = int(high_vulnerabilities_search.group(1))

            QualityGate.find_and_update_quality_gate(
                job_config.quality_gates, "HighVulnerabilities",
                high_vulnerabilities_count,
            )

            critical_vulnerabilities_count = 0
            critical_vulnerabilities_search = re.search(r"([0-9]+) critical", npm_install)
            if critical_vulnerabilities_search:
                critical_vulnerabilities_count = int(critical_vulnerabilities_search.group(1))

            QualityGate.find_and_update_quality_gate(
                job_config.quality_gates, "CriticalVulnerabilities",
                critical_vulnerabilities_count,
            )


# pylint: enable=too-few-public-methods
