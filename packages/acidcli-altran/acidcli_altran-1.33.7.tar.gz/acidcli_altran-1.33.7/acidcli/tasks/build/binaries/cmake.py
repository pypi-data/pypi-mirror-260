# Copyright Capgemini Engineering B.V.

"""Building binaries.

Building binaries using cmake
"""
import os

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import ProcessError
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class CMake(Executable):
    """CMake."""

    def __init__(self):
        """Initialize."""
        self.__job = None
        self.__cwd = os.getcwd()

    @print_job_info
    def execute(self, job):
        """Run cmake compilation.

        Run c/c++ code compilation with cmake

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(job, ["command", "input", "output"])

        if not os.path.isdir(os.path.join(self._parameter_value(self.__job, "input"), "build")):
            os.mkdir(os.path.join(self._parameter_value(self.__job, "input"), "build"))

        os.chdir(os.path.join(self._parameter_value(self.__job, "input"), "build"))

        self.__configure_build()
        self.__build_binaries()

        os.chdir(self.__cwd)

    @function_debug
    def __configure_build(self):
        """Configure CMake build.

        Use cmake to configure the build configuration for the binaries
        """
        configure_command = [
            "cmake",
            os.path.join(self.__cwd, self._parameter_value(self.__job, "input"))
        ]

        try:
            process = Subprocess(configure_command, verbose=self._parameter_value(self.__job, "verbose"))
            process.execute_pipe(
                os.path.join(self.__cwd, self._parameter_value(self.__job, "output")),
                "cmake_config.txt"
            )

        except ProcessError as error:
            raise CLIError(error) from error

    @function_debug
    def __build_binaries(self):
        """Build the binaries.

        Use cmake to build the binaries
        """
        build_command = [
            "cmake",
            "--build",
            ".",
            "--target",
            self._parameter_value(self.__job, "command")
        ]

        try:
            process = Subprocess(build_command, verbose=self._parameter_value(self.__job, "verbose"))
            process.execute_pipe(
                os.path.join(self.__cwd, self._parameter_value(self.__job, "output")),
                "cmake_build.txt"
            )
        except ProcessError as error:
            raise CLIError(error) from error


# pylint: enable=too-few-public-methods
