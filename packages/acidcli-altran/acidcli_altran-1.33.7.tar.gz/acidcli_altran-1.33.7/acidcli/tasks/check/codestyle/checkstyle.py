# Copyright Capgemini Engineering B.V..

"""CheckStyle.

Java code style implementation.
"""
import os

import xmltodict
from loguru import logger

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import ProcessError, Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class CheckStyle(Executable):
    """CheckStyle."""

    def __init__(self):
        """Initialize."""
        self.__config = None
        self.__output = None
        self.__verbose = None

    @print_job_info
    def execute(self, project_config, job_config):
        """Execute."""
        self.__config = self._validate_parameter(job_config, "config")
        self.__output = self._validate_parameter(job_config, "output")
        self.__verbose = self._validate_parameter(job_config, "verbose")

        for code_type in project_config.code_location:
            locations = " ".join(project_config.code_location[code_type])
            filename = f"{code_type}.xml"
            self._run_checkstyle(filename, locations)
            check_dict = self._get_checkstyle_dict(filename)
            issues_per_severity_level = self._parse_checkstyle(check_dict)
            self._check_quality_gates(issues_per_severity_level, code_type, job_config.quality_gates)

    @function_debug
    def _run_checkstyle(self, results_file, locations):
        """Run checkstyle tool."""
        checkstyle_command = [
            "checkstyle",
            f"-c={self.__config}",
            f"-o={os.path.join(self.__output, results_file)}",
            "-f=xml",
            locations,
        ]

        try:
            with open(os.path.join(self.__output, "checkstyle.txt"), "w", encoding="utf-8") as output_file:
                process = Subprocess(checkstyle_command, stdout=output_file, verbose=self.__verbose)
                process.execute()
        except ProcessError as error:
            logger.warning(error)
        except FileNotFoundError as exception:
            raise CLIError(
                f"Unable to open ('{exception.filename}') and write results.\n"
                f"Please use preconditions to enforce: ['OutputDirectoryExists', 'OutputDirectoryIsEmpty']."
            ) from exception

    @function_debug
    def _get_checkstyle_dict(self, results_file):
        """Convert checkstyle results into a dictionary."""
        with open(os.path.join(self.__output, results_file), "r", encoding="utf-8") as input_file:
            check_results = input_file.read()
            check_results_dict = xmltodict.parse(check_results)

            return check_results_dict

    @staticmethod
    @function_debug
    def _parse_checkstyle(check_results_dict):
        """Parse checkstyle results."""
        issues_per_severity_level = {
            "ERROR": 0,
            "WARNING": 0,
        }

        file_list = CheckStyle._get_dict_item_as_list(check_results_dict, ["checkstyle", "file"])

        for file in file_list:
            issue_list = CheckStyle._get_dict_item_as_list(file, ["error"])
            for issue in issue_list:
                if issue["@severity"] == "error":
                    issues_per_severity_level["ERROR"] += 1
                elif issue["@severity"] == "warning":
                    issues_per_severity_level["WARNING"] += 1

        return issues_per_severity_level

    @staticmethod
    @function_debug
    def _check_quality_gates(issues_per_severity_level, code_type, quality_gates):
        """Check Quality Gates."""
        QualityGate.find_and_update_quality_gate(
            quality_gates,
            f"{code_type}CodeStyleWarnings",
            issues_per_severity_level["WARNING"],
        )
        QualityGate.find_and_update_quality_gate(
            quality_gates,
            f"{code_type}CodeStyleErrors",
            issues_per_severity_level["ERROR"],
            mandatory=True,
        )

    @staticmethod
    @function_debug
    def _get_dict_item_as_list(dictionary, keys):
        """Get a dictionary item with the given keys as list."""
        node = dictionary

        for key in keys:
            if key not in node:
                return []
            node = node[key]

        if isinstance(node, dict):
            return [node]

        if isinstance(node, list):
            return node

        return []


# pylint: enable=too-few-public-methods
