# Copyright Capgemini Engineering B.V.

"""Test Maven.

Test Maven project
"""
from re import findall

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable
from acidcli.quality_gate import QualityGate


# pylint: disable=too-few-public-methods
class Maven(Executable):
    """Test Maven."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Test Maven."""
        self.__job = job
        self._required_parameters_available(self.__job, ["output", "test_settings_path", "test_pom_path", "index"])

        publish_output = self.__test_maven()
        number_of_tests = self.__determine_number_of_tests(publish_output)
        self.__set_qualitygates(self.__job.qualitygates, number_of_tests)

    @function_debug
    def __test_maven(self):
        """Run maven test.

        -e Produce execution error messages
        -U Forces a check for missing releases and updated snapshots on remote repositories
        -B Run in non-interactive (batch) mode (disables output color; supresses download progress)
        -fae Fail at end enabled
        -Dorg.slf4j.simpleLogger.log.org.apache.maven.cli.transfer=warn Supresses download INFO messages
        """
        test_command = [
            "mvn",
            "verify",
            "-s",
            self._parameter_value(self.__job, "test_settings_path"),
            "-f",
            self._parameter_value(self.__job, "test_pom_path"),
            "-e",
            "-U",
            "-B",
            "-fae",
            "-Dorg.slf4j.simpleLogger.log.org.apache.maven.cli.transfer=warn",
        ]

        process = Subprocess(test_command, verbose=self._parameter_value(self.__job, "verbose"))
        publish_output = process.execute_pipe(
            self._parameter_value(self.__job, "output"),
            "maven_test.log",
        )

        return publish_output

    @staticmethod
    @function_debug
    def __determine_number_of_tests(publish_output):
        """Determine number of tests."""
        captures = findall(b"Results:[\r\n]+[\r\n]+Tests run: ([0-9]*)", publish_output.stdout)
        number_of_tests = 0

        for capture in captures:
            number_of_tests = number_of_tests + int(capture)

        return number_of_tests

    @staticmethod
    @function_debug
    def __set_qualitygates(quality_gates, number_of_tests):
        """_set_qualitygates.

        Update Quality Gates
        :param quality_gates: list with set quality gates
        :param number_of_tests: number of tests
        """
        QualityGate.find_and_update_quality_gate(quality_gates, "NumberOfTests", number_of_tests, mandatory=False)


# pylint: enable=too-few-public-methods
