# Copyright Capgemini Engineering B.V.

"""PMD code inspection.

Code inspection using PMD
"""
import json
import os
import re

import xmltodict

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import ProcessError
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class PmdSpotbugsGradle(Executable):
    """PmdSpotbugs for Gradle."""

    def execute(self, project_config, job_config):
        """Invoke Check codeinspection."""
        _PmdSpotbugs("Gradle").execute(project_config, job_config)


# pylint: disable=too-few-public-methods
class _PmdSpotbugs(Executable):
    """PmdSpotbugs."""

    def __init__(self, platform):
        """__init__."""
        self.__output = None
        self.__verbosity = None
        self.__config = None
        self.__platform = platform

    @print_job_info
    def execute(self, project_config, job_config):
        """Check codeinspection."""
        self.__verbosity = self._validate_parameter(job_config, "verbose")
        self.__output = self._validate_parameter(job_config, "output")
        self.__config = self._validate_parameter(job_config, "config")

        if self.__platform == "Gradle":
            self.__run_spotbugs_gradle()
        else:
            raise CLIError(f"{self.__platform} is a non valid platform for Check Codeinspection")

        for code_type in project_config.code_location:
            violation_counts = [
                0,  # Level 1
                0,  # Level 2
                0,  # Level 3
                0,  # Level 4
                0,  # Level 5
            ]

            for location_path in project_config.code_location[code_type]:
                location_name = re.sub(
                    "[^A-Za-z0-9]+", "_", location_path
                )  # location path into file safe name for unique file writing
                self.__run_pmd(location_path, location_name)
                violation_counts = self.__get_pmd_violations(location_name, violation_counts)

                violation_counts = self.__get_spotbugs_violations(location_path, violation_counts)

            self.__update_quality_gate(job_config.quality_gates, code_type, violation_counts)

    @function_debug
    def __run_pmd(self, location_path, location_name):
        pmd_command = [
            "pmd",
            "-dir",
            location_path,
            "-rulesets",
            self.__config,
            "-failOnViolation",
            "false",
            "-format",
            "json",
            "-reportfile",
            os.path.join(self.__output, f"pmd_{location_name}_result.json"),
        ]

        with open(
            os.path.join(self.__output, f"pmd_{location_name}_invocation.txt"), "w", encoding="utf-8"
        ) as pmd_output_file:
            try:
                process = Subprocess(
                    pmd_command,
                    stdout=pmd_output_file,
                    stderr=pmd_output_file,
                    verbose=self.__verbosity,
                )
                process.execute()
            except ProcessError as error:
                raise CLIError(error) from error

    @function_debug
    def __get_pmd_violations(self, location_name, violation_counts):
        with open(
            os.path.join(self.__output, f"pmd_{location_name}_result.json"), "r", encoding="utf-8"
        ) as pmd_result_file:
            for file in json.loads(pmd_result_file.read())["files"]:
                for violation in file["violations"]:
                    priority = int(violation["priority"])
                    violation_counts[priority - 1] = violation_counts[priority - 1] + 1

        return violation_counts

    @function_debug
    def __get_spotbugs_violations(self, location_path, violation_counts):
        with open(
            os.path.join(self.__output, f"{os.path.basename(os.path.normpath(location_path))}.xml"),
            "r",
            encoding="utf-8",
        ) as spotbug_input_file:
            spotbug_results = spotbug_input_file.read()
            spotbug_dict = xmltodict.parse(spotbug_results)

            if "BugInstance" in spotbug_dict["BugCollection"]:
                if isinstance(spotbug_dict["BugCollection"]["BugInstance"], list):
                    for bug in spotbug_dict["BugCollection"]["BugInstance"]:
                        priority = int(bug["@priority"])
                        violation_counts[priority - 1] = violation_counts[priority - 1] + 1
                if isinstance(spotbug_dict["BugCollection"]["BugInstance"], dict):
                    priority = int(spotbug_dict["BugCollection"]["BugInstance"]["@priority"])
                    violation_counts[priority - 1] = violation_counts[priority - 1] + 1

        return violation_counts

    @staticmethod
    @function_debug
    def __update_quality_gate(quality_gates, code_type, violation_counts):
        """__update_quality_gate."""
        for index, violation_count in enumerate(violation_counts):
            QualityGate.find_and_update_quality_gate(quality_gates, f"{code_type}Priority{index + 1}", violation_count)

    @function_debug
    def __run_spotbugs_gradle(self):
        """Run SpotBugs for Gradle platform."""
        pmd_command = [
            "gradle",
            "check",
            f"-PSPOTBUGS_PATH={self.__output}",
        ]

        with open(
            os.path.join(self.__output, "spotbugs_invocation.txt"), "w", encoding="utf-8"
        ) as spotbugs_output_file:
            try:
                process = Subprocess(
                    pmd_command,
                    stdout=spotbugs_output_file,
                    stderr=spotbugs_output_file,
                    verbose=self.__verbosity,
                )
                process.execute()
            except ProcessError as error:
                raise CLIError(error) from error


# pylint: enable=too-few-public-methods
