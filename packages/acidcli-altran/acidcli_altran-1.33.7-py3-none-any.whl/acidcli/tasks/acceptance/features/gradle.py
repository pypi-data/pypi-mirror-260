# Copyright Capgemini Engineering B.V..

"""Gradle acceptance testing.

Acceptance testing of the Gradle skeleton using Cucumber tool.
"""
import os

import xmltodict

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import ProcessError, Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Gradle(Executable):
    """Gradle."""

    def __init__(self):
        """Initialize Gradle."""
        self.__output = None
        self.__verbose = None

    @print_job_info
    def execute(self, project_config, job_config):
        """Execute acceptance feature tests."""
        self.__output = self._validate_parameter(job_config, "output")
        self.__verbose = self._validate_parameter(job_config, "verbose")

        self.__run_tests()
        raw_coverage_data = self.__read_coverage_data()
        coverage_data = self.__create_basic_metrics(raw_coverage_data)
        coverage_data = self.__create_derivative_metrics(coverage_data)

        QualityGate.find_and_update_quality_gate(
            job_config.quality_gates,
            "CoveragePercentage",
            float(format(round(float(coverage_data["CoveragePercent"]) * 100, 2), "2f")),
            is_percentage=True,
        )

    @function_debug
    def __run_tests(self):
        """Run feature tests."""
        with open(os.path.join(self.__output, "gradle_cucumber.log"), "w", encoding="utf-8") as output_file:
            try:
                process = Subprocess(
                    ["gradle", "cucumber", f"-PCOVERAGE_DIR={self.__output}"],
                    stdout=output_file,
                    stderr=output_file,
                    verbose=self.__verbose,
                )
                process.execute()
            except ProcessError as error:
                raise CLIError(error) from error

    @function_debug
    def __read_coverage_data(self):
        """Read the coverage data from the Jacoco coverage report."""
        file = os.path.join(self.__output, "test", "jacocoTestReport.xml")
        try:
            with open(file, encoding="utf-8") as report_input_file:
                test_results = report_input_file.read()
                test_results_dict = xmltodict.parse(test_results)
                return test_results_dict["report"]["counter"]
        except FileNotFoundError as error:
            raise CLIError(f"Test report file '{file}' not found") from error
        except KeyError as error:
            raise CLIError("Test report file does not contain expected coverage data") from error

    @staticmethod
    @function_debug
    def __create_basic_metrics(coverage_data):
        """Create the basic coverage metrics."""
        covered_lines = missed_lines = covered_branches = missed_branches = 0

        for item in coverage_data:
            if item["@type"] == "LINE":
                covered_lines = int(item["@covered"])
                missed_lines = int(item["@missed"])
            if item["@type"] == "BRANCH":
                covered_branches = int(item["@covered"])
                missed_branches = int(item["@missed"])

        return {
            "CoveredLines": covered_lines,
            "UncoveredLines": missed_lines,
            "CoveredBranches": covered_branches,
            "UncoveredBranches": missed_branches,
        }

    @staticmethod
    @function_debug
    def __create_derivative_metrics(coverage_data):
        """Create and add coverage metrics that can be derived from existing ones."""
        coverage_data["TotalLines"] = coverage_data["CoveredLines"] + coverage_data["UncoveredLines"]
        coverage_data["TotalBranches"] = coverage_data["CoveredBranches"] + coverage_data["UncoveredBranches"]

        if coverage_data["TotalLines"] == 0:
            coverage_data["CoveragePercent"] = 0.0
        else:
            coverage_data["CoveragePercent"] = float(
                format(float(coverage_data["CoveredLines"] / (coverage_data["TotalLines"])), ".2f")
            )

        return coverage_data


# pylint: enable=too-few-public-methods
