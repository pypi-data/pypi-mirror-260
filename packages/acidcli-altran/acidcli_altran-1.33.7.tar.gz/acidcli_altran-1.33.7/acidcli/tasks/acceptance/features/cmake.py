# Copyright Capgemini Engineering B.V..

"""Feature testing binaries.

Feature testing binaries using cmake
"""
import os

import xmltodict

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class CMake(Executable):
    """Acceptance Features CMake."""

    def __init__(self):
        """Initialize."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Execute.

        Build code and run acceptance features.

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["command", "input", "output"])

        self.__configure()
        self.__build()

        self.__start_runner()
        self.__invoke_tests()
        gcovr_output = self.__get_coverage_results()

        coverage_data = self.__get_metrics(gcovr_output)
        self.__update_qualitygates(coverage_data)

    @function_debug
    def __configure(self):
        """Configure.

        Configure CMake build.

        :return: cmake_configure output
        """
        input_param = self._parameter_value(self.__job, "input")
        command = ["cmake", f"-B{os.path.join(input_param, 'build')}", f"-H{input_param}"]

        process = Subprocess(command, verbose=self._parameter_value(self.__job, "verbose"))
        cmake_configure_output = process.execute_pipe(self._parameter_value(self.__job, "output"), "cmake_configure")
        return cmake_configure_output.stdout

    @function_debug
    def __build(self):
        """Build.

        Build the binaries.

        :return: cmake_build output
        """
        input_param = self._parameter_value(self.__job, "input")
        command_param = self._parameter_value(self.__job, "command")
        command = [
            "cmake",
            "--build",
            os.path.join(input_param, "build"),
            "--target",
            command_param.rsplit("/", 1)[-1],
        ]

        process = Subprocess(command, verbose=self._parameter_value(self.__job, "verbose"))
        cmake_build_output = process.execute_pipe(self._parameter_value(self.__job, "output"), "cmake_build")
        return cmake_build_output.stdout

    @function_debug
    def __start_runner(self):
        """Start Runner.

        Start the cucumber step definition runner in the background.
        """
        command_param = [self._parameter_value(self.__job, "command")]

        build_process = Subprocess(command_param, verbose=self._parameter_value(self.__job, "verbose"))
        build_process.execute_async()

    @function_debug
    def __invoke_tests(self):
        """Invoke Tests.

        Invoke the tests.

        :return: cucumber output
        """
        input_param = self._parameter_value(self.__job, "input")
        command = ["valgrind", "cucumber", input_param]

        process = Subprocess(command, verbose=self._parameter_value(self.__job, "verbose"))
        cucumber_output = process.execute_pipe(self._parameter_value(self.__job, "output"), "cucumber")
        return cucumber_output.stdout

    @function_debug
    def __get_coverage_results(self):
        """Get coverage results.

        Get the coverage results and write to file.

        :return: gcovr output
        """
        input_param = self._parameter_value(self.__job, "input")
        command = ["gcovr", "-r", input_param, "--xml"]

        process = Subprocess(command, verbose=self._parameter_value(self.__job, "verbose"))
        gcovr_output = process.execute_pipe(self._parameter_value(self.__job, "output"), "gcovr")
        return gcovr_output.stdout

    @function_debug
    def __get_metrics(self, gcovr_output):
        """Get metrics.

        Get the metrics from the coverage results.

        :param gcovr_output: gcovr output string
        :return: coverage_data
        """
        test_results_dict = xmltodict.parse(gcovr_output.decode("utf-8"))
        coverage_data = {
            "CoveredLinesPercentage": float(test_results_dict["coverage"]["@line-rate"]),
            "CoveredBranchesPercentage": float(test_results_dict["coverage"]["@branch-rate"]),
        }

        return coverage_data

    def __update_qualitygates(self, coverage_data):
        """Update qualitygates.

        Set Coverage quality gates.

        :param coverage_data: Coverage data dict.
        """
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            "LineCoveragePercentage",
            float(format(round(float(coverage_data["CoveredLinesPercentage"]) * 100, 2), "2f")),
            is_percentage=True,
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            "BranchCoveragePercentage",
            float(format(round(float(coverage_data["CoveredBranchesPercentage"]) * 100, 2), "2f")),
            is_percentage=True,
        )


# pylint: enable=too-few-public-methods
