# Copyright Capgemini Engineering B.V.

"""Testing binaries.

Testing binaries using npm
"""

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Npm(Executable):
    """Npm."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Test units.

        Run unit tests for projects using npm

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["output"])
        self._required_list_parameters_available(self.__job, ["command"])

        self.__test_project()

    @function_debug
    def __test_project(self):
        """Test the npm project.

        Run npm command as subprocess with the given command value.

        :return: immutable bytes object containing the npm run output.
        """
        npm_test_command = ["npm", "run"]
        npm_test_command.extend(self._parameter_value(self.__job, "command"))

        process = Subprocess(npm_test_command, verbose=self._parameter_value(self.__job, "verbose"))
        npm_output = process.execute_pipe(self._parameter_value(self.__job, "output"), "npm")
        return npm_output.stdout


# pylint: enable=too-few-public-methods
