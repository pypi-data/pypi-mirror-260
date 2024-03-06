# Copyright Capgemini Engineering B.V.

"""Testing binaries.

Testing binaries using make
"""
from os.path import join

from loguru import logger
import i18n

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable
from acidcli.shared_functions.coverage import Coverage
from acidcli.shared_functions.valgrind import Valgrind
from acidcli.quality_gate import QualityGate
from acidcli.facility.junit_transformation import JunitTransformation


# pylint: disable=too-few-public-methods
class Make(Executable):
    """Make."""

    __VALGRIND_FILENAME = "valgrind.xml"
    __JUNIT_RESULT_FILENAME = "junit_results.xml"

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Make test units.

        Run C code tests with make.

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["input", "output"])
        self._required_list_parameters_available(self.__job, ["command"])
        self.__make_tests()

        self.__valgrind_invoke_tests()
        valgrind = Valgrind()
        valgrind_file = valgrind.read_valgrind_xml_results_file(
            join(self._parameter_value(self.__job, "output"), self.__VALGRIND_FILENAME)
        )
        valgrind_result = valgrind.parse_valgrind(valgrind_file)

        coverage_output = self.__collect_tests()
        coverage_xml = Coverage.read_coverage_xml_results_string(coverage_output)
        Coverage.print_coverage_results(coverage_xml)
        coverage_result = Coverage.calculate_coverage_percentages(coverage_xml)

        parsed_results = JunitTransformation().determine_number_of_tests(
            join(self._parameter_value(self.__job, "output"), self.__JUNIT_RESULT_FILENAME)
        )

        for failure in parsed_results["failed_tests"]:
            logger.error(i18n.t("acidcli.error_code_with_message", error=failure["message"], message=failure["text"]))

        self.__update_quality_gates(coverage_result, parsed_results["number_of_tests"], valgrind_result)

    @function_debug
    def __make_tests(self):
        """Make tests.

        Use make to build the tests.
        """
        make_test_command = ["make"]
        make_test_command.extend(self._parameter_value(self.__job, "command"))

        process = Subprocess(make_test_command, verbose=self._parameter_value(self.__job, "verbose"))
        make_test_output = process.execute_pipe(self._parameter_value(self.__job, "output"), "make_test")
        return make_test_output.stdout

    @function_debug
    def __valgrind_invoke_tests(self):
        """Valgrind invoke tests.

        Use valgrind to invoke the tests.
        """
        junit_file_path = join(self._parameter_value(self.__job, "output"), self.__JUNIT_RESULT_FILENAME)
        valgrind_test_command = [
            "valgrind",
            "--leak-check=full",
            "--xml=yes",
            f"--xml-file={join(self._parameter_value(self.__job, 'output'), self.__VALGRIND_FILENAME)}",
            self._parameter_value(self.__job, "input"),
            f"--gtest_output=xml:{junit_file_path}",
        ]

        process = Subprocess(valgrind_test_command, verbose=self._parameter_value(self.__job, "verbose"))
        valgrind_test_output = process.execute_pipe(self._parameter_value(self.__job, "output"), "valgrind_test")
        return valgrind_test_output.stdout.decode("utf-8")

    @function_debug
    def __collect_tests(self):
        """Collect tests.

        Collect coverage results.
        """
        gcovr_test_command = ["gcovr", "-r", ".", "--xml"]

        process = Subprocess(gcovr_test_command, verbose=self._parameter_value(self.__job, "verbose"))
        gcovr_test_output = process.execute_pipe(self._parameter_value(self.__job, "output"), "gcovr_test")

        return gcovr_test_output.stdout.decode("utf-8")

    def __update_quality_gates(self, coverage_percentages, number_of_tests, valgrind_results):
        """Update quality gates.

        Update quality gates with corresponding input values.

        :param coverage_percentages: line, branch, and total coverage percentages.
        :param number_of_tests: number of tests.
        :param valgrind_results: Number of memory leaks in bytes and blocks.
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
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            "DefinitivelyLostBytes",
            valgrind_results["Leak_DefinitelyLost"]["bytes"],
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            "IndirectlyLostBytes",
            valgrind_results["Leak_IndirectlyLost"]["bytes"],
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            "PossiblyLostBytes",
            valgrind_results["Leak_PossiblyLost"]["bytes"],
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            "StillReachableBytes",
            valgrind_results["Leak_StillReachable"]["bytes"],
        )


# pylint: enable=too-few-public-methods
