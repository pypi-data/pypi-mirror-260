# Copyright Capgemini Engineering B.V.

"""Test.

Reusable transformations for testing
"""
import os.path

from xmltodict import parse as parse_xml
import i18n

from acidcli.exceptions import CLIError
from acidcli.facility.subprocess import Subprocess
from acidcli.facility.decorators import function_debug


# pylint: disable=too-few-public-methods
class JunitTransformation:
    """JunitTransformation."""

    @staticmethod
    @function_debug
    def __read_junit_test_report(report_file):
        """Read junit test report.

        Read the JUnit unit test results into a dictionary.

        :param report_file: path to junit test report
        :return: dictionary
        """
        with open(
            report_file,
            encoding="utf-8-sig",
        ) as input_file:
            doc = parse_xml(input_file.read())

        return doc

    @staticmethod
    @function_debug
    def __determine_junit_testsuites(junit_report):
        """Determine number JUnit test suites.

        Get all test suites as list from a report.

        :param junit_report: JUnit report to parse
        :return: array with test suites
        """
        try:
            test_suites = junit_report["testsuites"]["testsuite"]
            if not isinstance(test_suites, list):
                return [test_suites]
            return test_suites
        except TypeError:
            return []

    @function_debug
    def determine_number_of_tests(self, output):
        """Determine number of tests and failed tests.

        Parse JUnit test report number of tests.

        :param output: JUnit report path
        :return: parsed test dict
        """
        number_of_tests = {"total": 0, "failures": 0, "skipped": 0, "errors": 0}
        failed_tests = []

        junit_report = self.__read_junit_test_report(output)
        test_suites = self.__determine_junit_testsuites(junit_report)

        try:
            for test_suite in test_suites:
                number_of_tests["total"] += int(test_suite["@tests"])
                number_of_tests["failures"] += int(test_suite["@failures"])
                number_of_tests["skipped"] += int(test_suite["@skipped"])
                number_of_tests["errors"] += int(test_suite["@errors"])
        except KeyError as error:
            raise CLIError(i18n.t("junit_results_invalid", error=error)) from error

        try:
            for test_suite in test_suites:
                if int(test_suite["@errors"]) > 0 or int(test_suite["@failures"]) > 0:
                    test_cases = test_suite["testcase"]
                    if not isinstance(test_cases, list):
                        test_cases = [test_suite["testcase"]]

                    self.__pytest_find_failed_tests(failed_tests, test_cases)

        except KeyError as error:
            raise CLIError(
                f"Unable to read junit results, {error} key is not present.\n"
                f"Please make sure the junit results file is valid."
            ) from error

        number_of_tests["passed"] = (
            number_of_tests["total"]
            - number_of_tests["failures"]
            - number_of_tests["skipped"]
            - number_of_tests["errors"]
        )
        return {"number_of_tests": number_of_tests, "failed_tests": failed_tests}

    @staticmethod
    @function_debug
    def __pytest_find_failed_tests(failed_tests, test_cases):
        """Pytest find failed tests.

        Parse JUnit test report on failed tests Pytest style

        :param failed_tests: list of failed tests
        :param test_cases: all found test cases
        """
        for test_case in test_cases:
            if "failure" in test_case:
                testcase = "Unknown testcase"
                if "@name" in test_case:
                    testcase = test_case["@name"]

                message = "Unknown message"
                if "@message" in test_case["failure"]:
                    message = test_case["failure"]["@message"].replace("\n", "")

                text = "Unknown text"
                if "#text" in test_case["failure"]:
                    text = test_case["failure"]["#text"]

                failed_tests.append({"testcase": testcase, "message": message, "text": text})

    @staticmethod
    @function_debug
    def transform_nunit3_to_junit(verbose, nunit3_report, junit_report, output_directory):
        """run_nunit3_junit.

        Transform Nunit3 report to Junit
        :param nunit3_report: input report
        :param junit_report: output report
        """
        nunit3_to_junit_command = [
            "powershell",
            os.path.join(os.path.dirname(__file__), "nunit3_to_junit.ps1"),
            "-nunit3_input",
            nunit3_report,
            "-junit_output",
            junit_report,
        ]
        process = Subprocess(nunit3_to_junit_command, verbose=verbose)
        process.execute_pipe(output_directory, "nunit3_to_junit")


# pylint: enable=too-few-public-methods
