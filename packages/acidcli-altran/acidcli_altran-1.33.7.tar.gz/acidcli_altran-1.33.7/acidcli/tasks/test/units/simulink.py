# Copyright Capgemini Engineering B.V.

"""Simulink.

Testing units using Simulink
"""

from os.path import join

from shutil import copytree
import i18n

from acidcli.facility.decorators import print_job_info, function_debug
from acidcli.tasks.executable import Executable
from acidcli.facility.subprocess import Subprocess
from acidcli.exceptions import CLIError


# pylint: disable=too-few-public-methods
class Simulink(Executable):
    """Simulink."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Test units.

        Run unit tests for simulink.

        :param job: job model object with job configuration.
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["output"])
        self.__test_units()
        self.__copy_results_to_output()

    @function_debug
    def __test_units(self):
        """Run test units command for simulink.

        Test Units Simulink.

        :return: Process object.
        """
        if "test" not in [location.name for location in self.__job.parent.parent.code_locations]:
            raise CLIError(i18n.t("acidcli.test_units.no_code_location"))
        test_folder = self.__get_test_locations(self.__job.parent.parent.code_locations)
        test_folder_string = "'" + "', '".join(test_folder) + "'"

        simulink_test_command = [
            "matlab",
            "-nodesktop",
            "-batch",
            f'"addpath(genpath(pwd)); runtests({test_folder_string}); exit;"',
        ]
        process = Subprocess(simulink_test_command, verbose=self._parameter_value(self.__job, "verbose"))
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
    def __copy_results_to_output(self):
        """Copy results to output.

        Copy the test results to the output folder.
        """
        if "test" not in [location.name for location in self.__job.parent.parent.code_locations]:
            raise CLIError(i18n.t("acidcli.test_units.no_code_location"))
        test_folders = self.__get_test_locations(self.__job.parent.parent.code_locations)
        for folder in test_folders:
            copytree(
                join(folder, "slcov_output/"), join(self._parameter_value(self.__job, "output")), dirs_exist_ok=True
            )


# pylint: enable=too-few-public-methods
