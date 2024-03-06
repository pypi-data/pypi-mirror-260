# Copyright Capgemini Engineering B.V.

"""Coverage.

Testing units using Coverage and pytest
"""
import os.path
from loguru import logger
import i18n

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.junit_transformation import JunitTransformation
from acidcli.quality_gate import QualityGate
from acidcli.shared_functions.coverage import Coverage
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Pytest(Executable):
    """Pytest."""

    __JUNIT_RESULT_FILENAME = "junit_results.xml"

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Test units.

        Run unit tests using coverage and pytest.

        :param job: job model object with job configuration.
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["config", "output"])
        output = self._parameter_value(self.__job, "output")
        verbose = self._parameter_value(self.__job, "verbose")

        # unit_test_run = self.__run_unit_tests()
        # self.__check_if_unit_tests_invocation_successful(unit_test_run)

        coverage = Coverage()
        coverage.export_html_report(output, verbose=verbose)
        coverage.export_xml_report(output, verbose=verbose)

        coverage_results = coverage.read_coverage_xml_results(output)
        coverage.print_coverage_results(coverage_results)

        parsed_results = JunitTransformation().determine_number_of_tests(
            os.path.join(output, self.__JUNIT_RESULT_FILENAME)
        )

        for failure in parsed_results["failed_tests"]:
            logger.error(i18n.t("acidcli.error_code_with_message", error=failure["message"], message=failure["text"]))

        coverage_percentages = Coverage.calculate_coverage_percentages(coverage_results)
        self.__update_quality_gates(coverage_percentages, parsed_results["number_of_tests"])

    @function_debug
    def __run_unit_tests(self):
        """Run unit tests.

        Run unittests using coverage and pytest.
        """
        command = [
            "pytest",
            "-o",
            "junit_family=xunit2",
            f"--junitxml={os.path.join(self._parameter_value(self.__job, 'output'), self.__JUNIT_RESULT_FILENAME)}",
        ]
        return Coverage.run_module(
            command,
            self._parameter_value(self.__job, "output"),
            verbose=self._parameter_value(self.__job, "verbose"),
            config=self._parameter_value(self.__job, "config"),
            check_return_code=False,
        )

    @staticmethod
    @function_debug
    def __check_if_unit_tests_invocation_successful(unit_test_run):
        """Check if unit tests invocation successful.

        Fail when one of the following exit code:

        Exit code 2
        Test execution was interrupted by the user

        Exit code 3
        Internal error happened while executing tests

        Exit code 4
        pytest command line usage error

        Reference: https://docs.pytest.org/en/7.1.x/reference/exit-codes.html

        :param unit_test_run: test execution object.
        """
        if unit_test_run.returncode in [2, 3, 4]:
            raise CLIError(i18n.t("acidcli.test_units.test_run_failed"))

    @function_debug
    def __update_quality_gates(self, coverage_percentages, number_of_tests):
        """Update quality gates.

        Update quality gates with corresponding input values.

        :param coverage_percentages: line, branch, and total coverage percentages.
        :param number_of_tests: number of tests.
        """
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, "CoveragePercentage", coverage_percentages["total"], is_percentage=True
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, "LineCoveragePercentage", coverage_percentages["line"], is_percentage=True
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, "BranchCoveragePercentage", coverage_percentages["branch"], is_percentage=True
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, "NumberOfFailedTests", number_of_tests["failures"], mandatory=True
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, "NumberOfPassedTests", number_of_tests["passed"], mandatory=False
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, "NumberOfSkippedTests", number_of_tests["skipped"], mandatory=True
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, "NumberOfErroredTests", number_of_tests["errors"], mandatory=True
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, "NumberOfTests", number_of_tests["total"], mandatory=False
        )


# pylint: enable=too-few-public-methods
