# Copyright Capgemini Engineering B.V.

"""Doxygen.

Doxygen build codedocumentation implementation
"""
from os import remove

from acidcli.facility.decorators import print_job_info, function_debug
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Doxygen(Executable):
    """Pandoc."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Build codedocumentation.

        Build codedocumentation with Doxygen

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["title", "config", "output"])
        self.__prepare_doxygen_file()
        self.__run_doxygen()
        self.__cleanup_doxygen_config_file()

    @function_debug
    def __run_doxygen(self):
        """Run doxygen.

        Run doxygen command as subprocess
        """
        doxygen_command = ["doxygen", f'{self._parameter_value(self.__job, "config")}_acidcli']
        process = Subprocess(doxygen_command, verbose=self._parameter_value(self.__job, "verbose"))
        process.execute_pipe(
            self._parameter_value(self.__job, "output"), "doxygen"
            )

    @function_debug
    def __prepare_doxygen_file(self):
        """Prepare doxygen file.

        Generate values in a doxygen config file
        """
        with open(f'{self._parameter_value(self.__job, "config")}_acidcli', "w+", encoding="utf-8") as file:
            content = f"""
@INCLUDE = {self._parameter_value(self.__job, 'config')}
PROJECT_NAME = \"{self._parameter_value(self.__job, 'title')}"
OUTPUT_DIRECTORY = {self._parameter_value(self.__job, 'output')}
PROJECT_NUMBER = {self._parameter_value(self.__job, 'version')}
"""
            file.write(content)

    @function_debug
    def __cleanup_doxygen_config_file(self):
        """Cleanup doxygen config file.

        Removes generated doxygen file
        """
        remove(f'{self._parameter_value(self.__job, "config")}_acidcli')
