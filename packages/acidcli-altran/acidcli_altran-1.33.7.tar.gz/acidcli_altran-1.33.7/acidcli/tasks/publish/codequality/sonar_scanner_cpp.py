# Copyright Capgemini Engineering B.V..

"""SonarScannerCPP.

Scan C and CPP projects for SonarQube.
"""
import i18n

from acidcli.exceptions import CLIError
from acidcli.tasks.executable import Executable
from acidcli.facility.decorators import print_job_info
from acidcli.facility.subprocess import Subprocess
from acidcli.shared_functions.sonar_scanner import SonarScanner


# pylint: disable=too-few-public-methods
class SonarScannerCpp(Executable):
    """SonarScannerCpp."""

    def __init__(self):
        """Init."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """execute.

        Publish C/CPP to SonarQube using SonarScanner.
        """
        self.__job = job
        if self.__job.parent.parent.sonarqube_url is None:
            raise CLIError(
                i18n.t(
                    "acidcli.parameter.missing",
                    task=self.__class__.__name__,
                    parameter="sonarqube_url",
                )
            )

        if self.__job.parent.parent.sonarqube_project_key is None:
            raise CLIError(
                i18n.t(
                    "acidcli.parameter.missing",
                    task=self.__class__.__name__,
                    parameter="sonarqube_project_key",
                )
            )

        self._required_parameters_available(self.__job, ["command", "target", "output", "sources"])
        self.__build_binaries()
        self.__run_build_wrapper()
        sonarqube_result = self.__run_sonar_scanner()
        SonarScanner.parse_output(sonarqube_result)

    def __run_sonar_scanner(self):
        """Run sonar scanner.

        Runs the sonar scanner.

        :return: the output of the sonar scanner
        """
        sonar_scanner_flags = [
            f"-Dsonar.sources={self._parameter_value(self.__job, 'sources')}",
            f"-Dsonar.cfamily.build-wrapper-output={self._parameter_value(self.__job, 'output')}",
        ]
        if self._parameter_value(self.__job, "config"):
            sonar_scanner_flags.extend(self._parameter_value(self.__job, "config"))

        sonarqube_result = SonarScanner.run(
            self.__job.parent.parent.sonarqube_url,
            self.__job.parent.parent.sonarqube_project_key,
            self._parameter_value(self.__job, "output"),
            sonar_scanner_flags,
            self._parameter_value(self.__job, "verbose"),
            self._parameter_value(self.__job, "version"),
            self._parameter_value(self.__job, "environment"),
        )
        return sonarqube_result

    def __run_build_wrapper(self):
        """Run build wrapper.

        Runs SonarQube build wrapper with make.

        :return: stdout of build wrapper
        """
        build_wrapper_command = [
            "build-wrapper-linux-x86-64",
            "--out-dir",
            self._parameter_value(self.__job, "output"),
            "cmake",
            "--build",
            ".",
            "--target",
            self._parameter_value(self.__job, "target"),
        ]

        process = Subprocess(build_wrapper_command, verbose=self._parameter_value(self.__job, "verbose"))
        run_build_wrapper = process.execute_pipe(self._parameter_value(self.__job, "output"), "build_wrapper")
        return run_build_wrapper.stdout

    def __build_binaries(self):
        """Build the binaries.

        Use cmake to build the binaries
        """
        build_command = ["cmake", self._parameter_value(self.__job, "command")]

        process = Subprocess(build_command, verbose=self._parameter_value(self.__job, "verbose"), redacted=True)
        build_binaries = process.execute_pipe(self._parameter_value(self.__job, "output"), "cmake_build")
        return build_binaries.stdout


# pylint: enable=too-few-public-methods
