# Copyright Capgemini Engineering B.V.

"""CSharpUnits.

Testing units using DotCover and NUnit
"""
import json
import os

import i18n
import xmltodict
from loguru import logger

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.dotcover import DotCover
from acidcli.facility.junit_transformation import JunitTransformation
from acidcli.quality_gate import QualityGate
from acidcli.tasks.executable import Executable
from acidcli.facility.subprocess import Subprocess


# pylint: disable=too-few-public-methods
class CSharpUnits(Executable):
    """CSharpUnits."""

    __NUNIT_RESULT_FILENAME = "TestResult.xml"
    __JUNIT_RESULT_FILENAME = "junit_results.xml"
    __MSTEST_RESULT_FILENAME = "TestResult.trx"
    __RESULT_FILENAME = "test"
    __VALID_PLATFORMS = ["NUnit", "MSTest"]

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """execute.

        Run unit tests with our without coverage for NUnit and MSTest.

        :param job: job model object with job configuration.
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["type", "config", "output", "coverage", "matching_pattern"])

        if "test" not in [location.name for location in self.__job.parent.parent.code_locations]:
            raise CLIError(i18n.t("acidcli.test_units.no_code_location"))

        if self.__job.platform not in self.__VALID_PLATFORMS:
            raise CLIError(
                i18n.t(
                    "acidcli.test_units.invalid_test_platform",
                    platform=self.__job.platform,
                    language="C#",
                )
            )

        files = DotCover().collect_test_files(
            self.__get_test_locations(self.__job.parent.parent.code_locations),
            self._parameter_value(self.__job, "type"),
            self._parameter_value(self.__job, "matching_pattern"),
        )

        self.__execute_tests(files)

        if self.__job.platform == "NUnit":
            parsed_results = self.__parse_nunit_results()
        elif self.__job.platform == "MSTest":
            parsed_results = self.__parse_trx_results()

        for failure in parsed_results["failed_tests"]:
            logger.error(
                i18n.t(
                    "acidcli.test_units.failed_test",
                    testcase=failure["testcase"],
                    error=failure["message"],
                    message=failure["text"],
                )
            )

        self.__update_number_tests_quality_gate(parsed_results["number_of_tests"])

    @function_debug
    def __execute_tests(self, files):
        """Execute tests.

        Execute tests based on coverage and type.

        :param files: Test files.
        """
        if self._parameter_as_bool(self.__job, "coverage"):
            self.__execute_dotcover_tests(files)
        else:
            self.__remove_coverage_quality_gate()
            if self.__job.platform == "MSTest":
                self.__execute_mstest_tests(files)
            elif self.__job.platform == "NUnit":
                self.__execute_nunit_tests(files)

    @function_debug
    def __execute_dotcover_tests(self, files):
        """Execute tests using DotCover.

        Execute the tests and create reports.

        :param files: files to test.
        """
        runner_args = (
            f"/logger:trx;LogFileName={self.__MSTEST_RESULT_FILENAME}" if self.__job.platform == "MSTest" else None
        )

        DotCover.run_tests(
            files,
            self._parameter_value(self.__job, "config"),
            self._parameter_value(self.__job, "output"),
            self.__RESULT_FILENAME,
            self._parameter_value(self.__job, "verbose"),
            runner_args,
        )

        DotCover.create_report(
            self._parameter_value(self.__job, "output"),
            "json",
            "json",
            self.__RESULT_FILENAME,
            self.__RESULT_FILENAME,
            self._parameter_value(self.__job, "verbose"),
        )
        DotCover.create_report(
            self._parameter_value(self.__job, "output"),
            "html",
            "html",
            self.__RESULT_FILENAME,
            "index",
            self._parameter_value(self.__job, "verbose"),
        )
        DotCover.create_report(
            self._parameter_value(self.__job, "output"),
            "xml",
            "xml",
            self.__RESULT_FILENAME,
            self.__RESULT_FILENAME,
            self._parameter_value(self.__job, "verbose"),
        )

        DotCover.create_report(
            self._parameter_value(self.__job, "output"),
            "DetailedXML",
            "xml",
            self.__RESULT_FILENAME,
            f"{self.__RESULT_FILENAME}_detailed",
            self._parameter_value(self.__job, "verbose"),
        )

        coverage_data = self.__get_coverage_from_json_report()

        DotCover.create_cobertura_report(
            self._parameter_value(self.__job, "output"),
            f"{self.__RESULT_FILENAME}_detailed",
            self._parameter_value(self.__job, "verbose"),
        )

        self.__update_coverage_quality_gates(float(format(round(float(coverage_data["CoveragePercent"]), 2), "2f")))

    @function_debug
    def __execute_mstest_tests(self, files):
        """Execute mstest tests.

        Execute mstest tests using vstest console

        :param files: files to test.
        """
        mstest_command = ["vstest.console"]
        mstest_command.extend(files)
        mstest_command.append(f"/logger:trx;LogFileName={self.__MSTEST_RESULT_FILENAME}")
        mstest_command.append(f"/ResultsDirectory:{self._parameter_value(self.__job, 'output')}")

        process = Subprocess(mstest_command, verbose=self._parameter_value(self.__job, "verbose"))
        process.execute_pipe(
            self._parameter_value(self.__job, "output"),
            "mstest_execute",
            check_return_code=False,
        )

    @function_debug
    def __execute_nunit_tests(self, files):
        """Execute Nunit tests.

        Run tests using NUnit.

        :param files: files to tests
        """
        nunit_command = ["nunit3-console"]
        nunit_command.extend(files)
        nunit_command.extend(["--work", self._parameter_value(self.__job, "output")])
        nunit_command.extend(["--result", self.__NUNIT_RESULT_FILENAME])

        process = Subprocess(nunit_command, verbose=self._parameter_value(self.__job, "verbose"))
        process.execute_pipe(
            self._parameter_value(self.__job, "output"),
            "nunit_execute",
            check_return_code=False,
        )

    @function_debug
    def __parse_nunit_results(self):
        """Parse nunit results.

        Transform and parse test results

        :return: parsed test dict
        """
        JunitTransformation.transform_nunit3_to_junit(
            self._parameter_value(self.__job, "verbose"),
            os.path.join(self._parameter_value(self.__job, "output"), self.__NUNIT_RESULT_FILENAME),
            os.path.join(self._parameter_value(self.__job, "output"), self.__JUNIT_RESULT_FILENAME),
            self._parameter_value(self.__job, "output"),
        )
        parsed_results = JunitTransformation().determine_number_of_tests(
            os.path.join(self._parameter_value(self.__job, "output"), self.__JUNIT_RESULT_FILENAME)
        )
        return parsed_results

    @function_debug
    def __parse_trx_results(self):
        """Read nr of tests from trx.

        Read the number of tests from rtx file.
        """
        number_of_tests = {}
        failed_tests = []

        with open(
            os.path.join(self._parameter_value(self.__job, "output"), self.__MSTEST_RESULT_FILENAME),
            mode="r",
            encoding="utf-8-sig",
        ) as trx:
            trx_results_dict = xmltodict.parse(trx.read())

            if "ResultSummary" not in trx_results_dict["TestRun"]:
                raise CLIError(i18n.t("acidcli.test_units.invalid_trx_file"))

            number_of_tests["total"] = int(trx_results_dict["TestRun"]["ResultSummary"]["Counters"]["@total"])
            number_of_tests["passed"] = int(trx_results_dict["TestRun"]["ResultSummary"]["Counters"]["@passed"])
            number_of_tests["failures"] = int(trx_results_dict["TestRun"]["ResultSummary"]["Counters"]["@failed"])
            number_of_tests["skipped"] = number_of_tests["total"] - int(
                trx_results_dict["TestRun"]["ResultSummary"]["Counters"]["@executed"]
            )

            for result in trx_results_dict["TestRun"]["Results"]["UnitTestResult"]:
                if result["@outcome"] == "Failed":
                    error_info = result["Output"]["ErrorInfo"]
                    text = error_info["StackTrace"] if "StackTrace" in error_info else ""
                    message = error_info["Message"].replace("&#xD", "")
                    failed_tests.append({"testcase": "Unknown", "message": message, "text": text})

            return {"number_of_tests": number_of_tests, "failed_tests": failed_tests}

    @staticmethod
    @function_debug
    def __get_test_locations(code_locations):
        """Get test locations.

        Get directories for test locations.

        :param code_locations: code locations to search trough
        """
        return [location.directories for location in code_locations if location.name == "test"][0]

    @function_debug
    def __get_coverage_from_json_report(self):
        """Get coverage from json report.

        Read the coverage data from the json report file.
        """
        filename = f"{self.__RESULT_FILENAME}.json"

        with open(
            os.path.join(self._parameter_value(self.__job, "output"), filename),
            encoding="utf-8-sig",
        ) as input_file:
            return json.loads(input_file.read())

    @function_debug
    def __update_coverage_quality_gates(self, coverage_percentage):
        """Update quality gates.

        Update quality gates with corresponding input values.

        :param coverage_percentage: coverage percentage.
        """
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            "CoveragePercentage",
            coverage_percentage,
            is_percentage=True,
        )

    @function_debug
    def __remove_coverage_quality_gate(self):
        """Remove Coverage quality gate.

        Remove Coverage quality gate if present.
        """
        coverage_quality_gate = QualityGate.find_quality_gate(self.__job.qualitygates, "CoveragePercentage")
        if coverage_quality_gate is not None:
            QualityGate.remove_quality_gate(self.__job.qualitygates, coverage_quality_gate)

    @function_debug
    def __update_number_tests_quality_gate(self, number_of_tests):
        """Update number of tests quality gate.

        Update number of tests in the quality gate.

        :param number_of_tests: number of tests.
        """
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, "NumberOfFailedTests", number_of_tests["failures"], mandatory=True
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            "NumberOfPassedTests",
            number_of_tests["passed"],
            mandatory=False,
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            "NumberOfSkippedTests",
            number_of_tests["skipped"],
            mandatory=True,
        )
        if "errors" in number_of_tests:
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates,
                "NumberOfErroredTests",
                number_of_tests["errors"],
                mandatory=True,
            )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            "NumberOfTests",
            number_of_tests["total"],
            mandatory=False,
        )


# pylint: enable=too-few-public-methods
