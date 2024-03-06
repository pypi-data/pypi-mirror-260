# Copyright Capgemini Engineering B.V.

"""SonarScannerMSBuild code quality.

CodeQuality checks by Sonar Scanner for MSBuild
"""
import os
from shutil import copy, copytree
import re

import i18n
from loguru import logger

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess, ProcessError
from acidcli.tasks.executable import Executable
from acidcli.facility.dotcover import DotCover


# pylint: disable=too-few-public-methods
class SonarScannerMSBuild(Executable):
    """SonarScannerMSBuild."""

    __COVERAGE_FILENAME = "CoverageParameters.xml"
    __REPORT_FILENAME = "unittest"
    __NUNIT3_RESULT_FILENAME = "TestResult.xml"
    __MSTEST_RESULT_FILENAME = "TestResult.trx"
    __VALID_PLATFORMS = ["NUnit", "MSTest"]
    __RESULT_FILENAME = "unittest"

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Execute.

        publish code to SonarQube.

        :param job: Job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["type", "input", "output", "unittests", "matching_pattern"])

        self.__validate_configuration()

        versioning = self._parameter_value(self.__job, "version")
        environment = self._parameter_value(self.__job, "environment")

        project_version = versioning.get_semver()
        token = environment.technical_sonarqube_token

        if not versioning.is_pipeline() or token is None:
            raise CLIError(i18n.t("acidcli.pipeline.environment_variable_missing"))

        backwards_compatible = os.environ.get("SONARQUBE_9")
        if backwards_compatible == "true":
            login_parameter = f"/d:sonar.login={token}"
        else:
            login_parameter = f"/d:sonar.token={token}"

        if self._parameter_as_bool(self.__job, "unittests"):
            self.__execute_sonarqube_with_unittests(project_version, login_parameter)
        else:
            self.__start_sonarscanner(project_version, login_parameter)

            self.__csharp_build_binaries()

        self.__end_sonarscanner(login_parameter)
        if self._parameter_value(self.__job, "ndepend_configuration"):
            self.__run_ndepend()

    def __execute_sonarqube_with_unittests(self, project_version, login_parameter):
        """Execute SonarQube with unittests.

        Execute sonarqube with unittests.

        :param project_version: project version
        :param login_parameter: SonarQube token
        """
        if self.__job.platform == "NUnit":
            path = os.path.join(self._parameter_value(self.__job, "output"), self.__NUNIT3_RESULT_FILENAME)
            self.__start_sonarscanner(
                project_version,
                login_parameter,
                f"/d:sonar.cs.nunit.reportsPaths={path}",
            )
        elif self.__job.platform == "MSTest":
            path = os.path.join(self._parameter_value(self.__job, "output"), self.__MSTEST_RESULT_FILENAME)
            self.__start_sonarscanner(project_version, login_parameter, f"/d:sonar.cs.vstest.reportsPaths={path}")

        self.__csharp_build_binaries()

        files = DotCover().collect_test_files(
            self.__get_test_locations(self.__job.parent.parent.code_locations),
            self._parameter_value(self.__job, "type"),
            self._parameter_value(self.__job, "matching_pattern"),
        )

        if self.__job.platform == "NUnit":
            DotCover.run_tests(
                files,
                self.__COVERAGE_FILENAME,
                self._parameter_value(self.__job, "output"),
                self.__RESULT_FILENAME,
                self._parameter_value(self.__job, "verbose"),
            )
        elif self.__job.platform == "MSTest":
            DotCover.run_tests(
                files,
                self.__COVERAGE_FILENAME,
                self._parameter_value(self.__job, "output"),
                self.__RESULT_FILENAME,
                self._parameter_value(self.__job, "verbose"),
                f"/logger:trx;LogFileName={self.__MSTEST_RESULT_FILENAME}",
            )

        self.__create_report()

    @function_debug
    def __validate_configuration(self):
        """Validate configuration.

        Checks if the configuration is valid.
        """
        if self.__job.platform not in self.__VALID_PLATFORMS:
            raise CLIError(
                i18n.t(
                    "acidcli.test_units.invalid_test_platform",
                    platform=self.__job.platform,
                    language="C#",
                )
            )

        if "test" not in [location.name for location in self.__job.parent.parent.code_locations]:
            raise CLIError(i18n.t("acidcli.test_units.no_code_location"))

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

    @function_debug
    def __start_sonarscanner(self, project_version, login_parameter, test_platform_arg=None):
        """Start Sonarscanner.

        Starts SonarScanner for MSBuild.

        :param project_version: project version
        :param login_parameter: sonarqube token parameter
        :param test_platform_arg: Test reports path argument for SonarScanner
        """
        reports_path = os.path.join(self._parameter_value(self.__job, "output"), f"{self.__REPORT_FILENAME}.html")
        command = [
            "SonarScanner.MSBuild.exe",
            "begin",
            f"/k:{self.__job.parent.parent.sonarqube_project_key}",
            f"/d:sonar.host.url={self.__job.parent.parent.sonarqube_url}",
            login_parameter,
            f"/v:{project_version}",
            "/d:sonar.exclusions=**/GeneratedCode/**",
            "/d:sonar.qualitygate.wait=true",
        ]

        if test_platform_arg is not None:
            command.extend(
                [
                    "/d:sonar.msbuild.testProjectPattern=.*(Tests?|SystemTestLib|TestUtil)\\.(cs|vb)proj$",
                    f"/d:sonar.cs.dotcover.reportsPaths={reports_path}",
                    test_platform_arg,
                ]
            )

        if self._parameter_value(self.__job, "ndepend_configuration"):
            path = os.path.join(os.getcwd(), self._parameter_value(self.__job, "ndepend_configuration"))
            command.append(f"/d:sonar.cs.ndepend.projectPath={path}")
        else:
            command.append("/d:sonar.cs.ndepend.skip=true")

        self.__run_command(command)

    @function_debug
    def __create_report(self):
        """Create report.

        Create DotCover Report.
        """
        source_path = os.path.join(self._parameter_value(self.__job, "output"), f"{self.__REPORT_FILENAME}.dcvr")
        output_path = os.path.join(self._parameter_value(self.__job, "output"), f"{self.__REPORT_FILENAME}.html")
        command = [
            "dotcover",
            "report",
            f"/Source={source_path}",
            "/ReportType=HTML",
            f"/Output={output_path}",
        ]

        self.__run_command(command)

    @function_debug
    def __end_sonarscanner(self, login_parameter):
        """End Sonarscanner.

        End SonarScanner for MSBuild.

        :param login_parameter: sonarqube login parameter
        """
        command = ["SonarScanner.MSBuild.exe", "end", login_parameter]

        sonar_output = self.__run_command(command, False)
        if "You're not authorized to run analysis." in sonar_output.stdout.decode("utf-8"):
            raise CLIError(i18n.t("acidcli.sonarqube.unauthorized_exception"))

        re_search = re.search(r"View details on (.*)", sonar_output.stdout.decode("utf-8"))
        url = re_search.group(1).rstrip()

        if sonar_output.returncode != 0:
            raise CLIError(i18n.t("acidcli.sonarqube.quality_gate_failed", message=url))
        logger.info(i18n.t("acidcli.sonarqube.quality_gate_details", message=url))

    @function_debug
    def __run_ndepend(self):
        """Run ndepend.

        Run NDepend specific for HTML output.
        """
        command = [
            "NDepend.Console.exe",
            os.path.join(os.getcwd(), self._parameter_value(self.__job, "ndepend_configuration")),
        ]
        try:
            self.__run_command(command)
        except ProcessError as error:
            if "NDepend analysis done." not in error.command_output:
                raise error

        copytree(
            os.path.join(os.getcwd(), "NDependOut/NDependReportFiles/"),
            os.path.join(self._parameter_value(self.__job, "output"), "NDepend/NDependReportFiles/"),
        )
        copy(
            os.path.join(os.getcwd(), "NDependOut/NDependReport.html"),
            os.path.join(self._parameter_value(self.__job, "output"), "NDepend/"),
        )

    @function_debug
    def __run_command(self, command, check_return_code=True):
        """Run command.

        Run generic function for running a command.

        :param command: Command to execute
        :param check_return_code: Check the return code
        :return: sonar command output
        """
        process = Subprocess(command, verbose=self._parameter_value(self.__job, "verbose"), redacted=True)
        sonar_output = process.execute_pipe(
            self._parameter_value(self.__job, "output"), "sonar_scanner", check_return_code=check_return_code
        )
        return sonar_output

    @function_debug
    def __csharp_build_binaries(self):
        """Csharp build binaries.

        Build CSharp binaries.

        :return: process stdout
        """
        binaries_build_command = [
            "MSBuild",
            "/nr:false",
            "/t:Rebuild",
            f"/property:Configuration={self._parameter_value(self.__job, 'type')}",
            "/m",
            self._parameter_value(self.__job, "input"),
        ]

        process = Subprocess(
            binaries_build_command, verbose=self._parameter_value(self.__job, "verbose"), redacted=True
        )
        msbuild_output = process.execute_pipe(self._parameter_value(self.__job, "output"), "msbuild")

        return msbuild_output.stdout

    @staticmethod
    @function_debug
    def __get_test_locations(code_locations):
        """Get test locations.

        Get directories for test locations.

        :param code_locations: code locations to search trough
        :return: test code locations
        """
        return [location.directories for location in code_locations if location.name == "test"][0]


# pylint: enable=too-few-public-methods
