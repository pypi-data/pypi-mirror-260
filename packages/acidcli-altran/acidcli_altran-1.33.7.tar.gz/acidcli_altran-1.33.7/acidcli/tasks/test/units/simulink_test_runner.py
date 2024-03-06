# Copyright Capgemini Engineering B.V.

"""Simulink test runner.

Testing units using Simulink test runner
"""
import os
import i18n
from loguru import logger

from acidcli.facility.junit_transformation import JunitTransformation
from acidcli.facility.decorators import print_job_info, function_debug
from acidcli.tasks.executable import Executable
from acidcli.facility.subprocess import Subprocess
from acidcli.exceptions import CLIError
from acidcli.quality_gate import QualityGate


# pylint: disable=too-few-public-methods
class SimulinkTestRunner(Executable):
    """Simulink."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Test units.

        Run unit tests for simulink using test runner.

        :param job: job model object with job configuration.
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["output"])

        self.__test_units()
        parsed_results = JunitTransformation().determine_number_of_tests(
            os.path.join(self._parameter_value(self.__job, "output"), "junit_results.xml")
        )

        for failure in parsed_results["failed_tests"]:
            logger.error(i18n.t("acidcli.error_code_with_message", error=failure["message"], message=failure["text"]))

        self.__update_quality_gates(parsed_results["number_of_tests"])

    @function_debug
    def __test_units(self):
        """Run test units command for simulink using test runner.

        Test Units Simulink using test runner.

        :return: Process object.
        """
        if "test" not in [location.name for location in self.__job.parent.parent.code_locations]:
            raise CLIError(i18n.t("acidcli.test_units.no_code_location"))
        test_folder = self.__get_test_locations(self.__job.parent.parent.code_locations)
        test_folder_string = "'" + "', '".join(test_folder) + "'"
        matlab_batch_command = [
            "addpath(genpath(pwd));",
            "import matlab.unittest.TestRunner;",
            "import matlab.unittest.TestSuite;",
            "import matlab.unittest.plugins.XMLPlugin;",
            f"suite = TestSuite.fromFolder({test_folder_string});",
            "runner = TestRunner.withNoPlugins;",
            f"xmlFile = '{self._parameter_value(self.__job, 'output')}/junit_results.xml';",
            "p = XMLPlugin.producingJUnitFormat(xmlFile); runner.addPlugin(p); runner.run(suite); exit;",
        ]
        simulink_test_runner_command = ["matlab", "-nodesktop", "-batch", f'"{" ".join(matlab_batch_command)}"']
        process = Subprocess(simulink_test_runner_command, verbose=self._parameter_value(self.__job, "verbose"))
        return process.execute_pipe(self._parameter_value(self.__job, "output"), "simulink_test")

    @staticmethod
    @function_debug
    def __get_test_locations(code_locations):
        """Get test locations.

        Get directories for test locations.

        :param code_locations: code locations to search trough
        """
        return [location.directories for location in code_locations if location.name == "test"][0]

    @function_debug
    def __update_quality_gates(self, number_of_tests):
        """Update quality gates.

        Update quality gates with corresponding input values.

        :param number_of_tests: number of tests.
        """
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
