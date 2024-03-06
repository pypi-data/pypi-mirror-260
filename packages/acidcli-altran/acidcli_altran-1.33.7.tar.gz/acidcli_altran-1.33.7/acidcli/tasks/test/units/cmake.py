# Copyright Capgemini Engineering B.V..

"""Testing binaries.

Testing binaries using cmake
"""
import os

from loguru import logger
import i18n

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import ProcessError, Subprocess
from acidcli.tasks.executable import Executable
from acidcli.facility.junit_transformation import JunitTransformation
from acidcli.shared_functions.coverage import Coverage
from acidcli.shared_functions.valgrind import Valgrind


# pylint: disable=too-few-public-methods
class CMake(Executable):
    """CMake."""

    __COVERAGE_FILE_NAME = "coverage.xml"
    __JUNIT_RESULT_FILENAME = "junit_results.xml"
    __VALGRIND_FILENAME = "valgrind.xml"

    def __init__(self):
        """Initialize."""
        self.__job = None
        self.__cwd = None

    @print_job_info
    def execute(self, job):
        """Run cmake tests.

        Run c++ code tests with cmake

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(job, ["command", "input", "output"])

        self.__cwd = os.getcwd()

        # Create build directory if needed.
        if not os.path.isdir(os.path.join(self._parameter_value(self.__job, "input"), "build")):
            os.mkdir(os.path.join(self._parameter_value(self.__job, "input"), "build"))

        os.chdir(os.path.join(self._parameter_value(self.__job, "input"), "build"))

        self.__configure()
        self.__build()

        os.chdir(self.__cwd)

        self.__invoke_tests()
        valgrind = Valgrind()
        valgrind_file = valgrind.read_valgrind_xml_results_file(
            os.path.join(self._parameter_value(self.__job, "output"), self.__VALGRIND_FILENAME)
        )
        valgrind_result = valgrind.parse_valgrind(valgrind_file)

        self.__get_coverage_results()
        coverage = Coverage()
        coverage_results = coverage.read_coverage_xml_results(self._parameter_value(self.__job, "output"))
        coverage.print_coverage_results(coverage_results, path_prefix=self._parameter_value(self.__job, "input"))

        parsed_results = JunitTransformation().determine_number_of_tests(
            os.path.join(self._parameter_value(self.__job, "output"), self.__JUNIT_RESULT_FILENAME)
        )

        for failure in parsed_results["failed_tests"]:
            logger.error(i18n.t("acidcli.error_code_with_message", error=failure["message"], message=failure["text"]))

        coverage_percentages = Coverage.calculate_coverage_percentages(coverage_results)
        self.__update_quality_gates(coverage_percentages, parsed_results["number_of_tests"], valgrind_result)

    @function_debug
    def __configure(self):
        """Configure CMake build.

        Use cmake to configure the build configuration for the tests
        """
        command = ["cmake", os.path.join(self.__cwd, self._parameter_value(self.__job, "input"))]

        try:
            process = Subprocess(command, verbose=self._parameter_value(self.__job, "verbose"))
            process.execute_pipe(
                os.path.join(self.__cwd, self._parameter_value(self.__job, "output")),
                "cmake_config",
            )

        except ProcessError as error:
            raise CLIError(error) from error

    @function_debug
    def __build(self):
        """Build the binaries.

        Use cmake to build the test binaries
        """
        command = ["cmake", "--build", ".", "--target", self._parameter_value(self.__job, "command")]

        try:
            process = Subprocess(command, verbose=self._parameter_value(self.__job, "verbose"))
            process.execute_pipe(
                os.path.join(self.__cwd, self._parameter_value(self.__job, "output")),
                "cmake_build",
            )

        except ProcessError as error:
            raise CLIError(error) from error

    @function_debug
    def __invoke_tests(self):
        """Invoke the tests.

        Use valgrind to run the test executable
        """
        junit_file_path = os.path.join(self._parameter_value(self.__job, "output"), self.__JUNIT_RESULT_FILENAME)
        command = [
            "valgrind",
            "--leak-check=full",
            "--xml=yes",
            f"--xml-file={os.path.join(self._parameter_value(self.__job, 'output'), self.__VALGRIND_FILENAME)}",
            os.path.join(
                self._parameter_value(self.__job, "input"),
                "build",
                "test",
                self._parameter_value(self.__job, "command"),
            ),
            f"--gtest_output=xml:{junit_file_path}",
        ]

        try:
            process = Subprocess(command, verbose=self._parameter_value(self.__job, "verbose"))
            process.execute_pipe(
                os.path.join(self.__cwd, self._parameter_value(self.__job, "output")),
                "valgrind",
            )
        except ProcessError as error:
            raise CLIError(error) from error

    @function_debug
    def __get_coverage_results(self):
        """Get the coverage results.

        Get the coverage results, parse them and write to file.
        """
        command = ["gcovr", "-r", self._parameter_value(self.__job, "input"), "--xml"]

        try:
            process = Subprocess(command, verbose=self._parameter_value(self.__job, "verbose"))
            gcov_data = process.execute_pipe(
                os.path.join(self.__cwd, self._parameter_value(self.__job, "output")),
                self.__COVERAGE_FILE_NAME,
            )
            with open(
                os.path.join(self._parameter_value(self.__job, "output"), self.__COVERAGE_FILE_NAME),
                "w+",
                encoding="utf-8",
            ) as file:
                file.write(gcov_data.stdout.decode("utf-8"))

        except ProcessError as error:
            raise CLIError(error) from error

    @function_debug
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
            mandatory=False,
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            "IndirectlyLostBytes",
            valgrind_results["Leak_IndirectlyLost"]["bytes"],
            mandatory=False,
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            "PossiblyLostBytes",
            valgrind_results["Leak_PossiblyLost"]["bytes"],
            mandatory=False,
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            "StillReachableBytes",
            valgrind_results["Leak_StillReachable"]["bytes"],
            mandatory=False,
        )


# pylint: enable=too-few-public-methods
