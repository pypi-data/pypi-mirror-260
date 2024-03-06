# Copyright Capgemini Engineering B.V.

"""Cppcheck code inspection.

Code inspection using cppcheck and clang
"""
import re
import os
from collections import OrderedDict
from os.path import join
from glob import glob

import i18n
from xmltodict import parse as parse_xml
from bs4 import BeautifulSoup as bs

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Cppcheck(Executable):
    """Cppcheck."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check codeinspection.

        Check codeinspection for C/C++.

        :param job: job model object with job configuration
        """
        self.__job = job
        self.__job.issues = []
        tool = self._parameter_value(job, "tool")
        bugs, errors = self.__run_tools(tool)

        self.__update_qualitygates(bugs, errors, tool)

    @function_debug
    def __run_tools(self, tool):
        """__run_tools.

        Run tool based on Tool selected.

        :param tool: Tool to run
        :return: found bugs and found errors
        """
        errors = None
        bugs = None
        if tool == "cppcheck" or tool is None:
            self._required_list_parameters_available(self.__job, ["library"])
            libraries = self._parameter_value(self.__job, "library")
            cppcheck_results = self.__cppcheck_code(libraries)
            errors = self.__cppcheck_collect_issues(cppcheck_results)

        if tool == "clang" or tool is None:
            self._required_parameters_available(self.__job, ["output"])
            clang_results = self.__clang_code().decode("utf-8")
            bugs = self.__parse_clang_bugs(clang_results)
            self.__clang_collect_issues(bugs)

        if tool not in ["clang", "cppcheck", None]:
            raise CLIError(
                i18n.t(
                    "acidcli.parameter.invalid_value",
                    task=self.__class__.__name__,
                    parameter="tool",
                    received_value=tool,
                    allowed_values=["cppcheck, clang", None],
                )
            )
        return bugs, errors

    @function_debug
    def __update_qualitygates(self, bugs, errors, tool):
        """__update_qualitygates.

        Update qualitygates for codeinspection.
        Only set CodeInspectionErrors if tool is cppcheck.
        Only set CodeInspectionBugs if tool is clang.

        :param bugs: bugs count
        :param errors: error count
        :param tool: which tool(s) have been executed
        """
        if tool == "cppcheck":
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates, "CodeInspectionErrors", errors, mandatory=True
            )
        if tool == "clang":
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates, "CodeInspectionBugs", bugs, mandatory=True
            )
        if tool is None:
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates, "CodeInspectionErrors", errors, mandatory=True
            )
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates, "CodeInspectionBugs", bugs, mandatory=True
            )

    @function_debug
    def __clang_code(self):
        """Clang clode.

        Check code in C and CPP language using Clang.

        :return: clang tool output
        """
        cwd = os.getcwd()
        if self.__job.language == "CPP":
            self._required_parameters_available(self.__job, ["input", "target"])
            self.__make_and_enter_build_directory()
            self.__configure_build(cwd)
            clang_command = self.__get_clang_command_cpp(cwd)
            clang_output = self.__execute_clang_pipe(clang_command, cwd)
            os.chdir(cwd)
        elif self.__job.language == "C":
            clang_command = self.__get_clang_command_c()
            clang_output = self.__execute_clang_pipe(clang_command, cwd)
        else:
            raise CLIError(i18n.t("acidcli.clang_unexpected_language", language=self.__job.language))
        return clang_output

    @function_debug
    def __make_and_enter_build_directory(self):
        """Make and enter the build directory.

        Make the output/build directory and enter it.
        """
        build_folder = join(self._parameter_value(self.__job, "output"), "build")
        os.mkdir(build_folder)
        os.chdir(build_folder)

    @function_debug
    def __configure_build(self, cwd):
        """Configure CMake build.

        Use cmake to configure the build configuration for the binaries.

        :param cwd: base working directory
        :return: output of building the configuration
        """
        configure_command = ["scan-build", "cmake", join(cwd, self._parameter_value(self.__job, "input"))]
        process = Subprocess(configure_command, verbose=self._parameter_value(self.__job, "verbose"))
        configure_build = process.execute_pipe(join(cwd, self._parameter_value(self.__job, "output")), "cmake_config")
        return configure_build.stdout

    @function_debug
    def __get_clang_command_c(self):
        """Get clang command for C.

        The clang command if the language is c.

        :return: the clang command to be used in Subprocess
        """
        clang_command = ["scan-build", "-o", self._parameter_value(self.__job, "output"), "make"]
        return clang_command

    @function_debug
    def __get_clang_command_cpp(self, cwd):
        """Get clang command for CPP.

        The clang command if the language is cpp.

        :param cwd: base working directory
        :return: the clang command to be used in Subprocess
        """
        clang_command = [
            "scan-build",
            "-o",
            join(cwd, self._parameter_value(self.__job, "output")),
            "cmake",
            "--build",
            ".",
            "--target",
            self._parameter_value(self.__job, "target"),
        ]
        return clang_command

    @function_debug
    def __execute_clang_pipe(self, clang_command, cwd):
        """Execute clang pipe.

        Execute the pipe with the correct clang command.

        :param clang_command: clang command to be executed
        :param cwd: base working directory
        :return: clang tool output
        """
        process = Subprocess(clang_command, verbose=self._parameter_value(self.__job, "verbose"))
        clang_output = process.execute_pipe(join(cwd, self._parameter_value(self.__job, "output")), "clang")
        return clang_output.stdout

    @function_debug
    def __cppcheck_code(self, libraries):
        """Cpp check code.

        Check CPP code

        :param libraries: libraries to check
        :return: cppcheck tool output
        """
        make_test_command = ["cppcheck", "--enable=all", "--xml-version=2", "--xml", "--suppress=missingIncludeSystem"]

        for code_location in self.__job.parent.parent.code_locations:
            make_test_command.extend(code_location.directories)

        for library_path in libraries:
            make_test_command.extend(["-I", library_path])

        process = Subprocess(make_test_command, verbose=self._parameter_value(self.__job, "verbose"))
        cppcheck_output = process.execute_pipe(self._parameter_value(self.__job, "output"), "cppcheck")

        return cppcheck_output.stdout

    @function_debug
    def __cppcheck_collect_issues(self, cppcheck_results):
        """Collect issues.

        Collect cppcheck issues for issue reporter.

        :param cppcheck_results: Cpp check results.
        :return: amount of Cpp check errors
        """
        cppcheck_input_data = parse_xml(cppcheck_results)
        errors = cppcheck_input_data["results"]["errors"]
        issues = []

        if isinstance(errors, (OrderedDict, dict)):
            for error in errors["error"]:
                try:
                    if isinstance(error["location"], list):
                        issues.append(
                            {
                                "path": error["location"][0]["@file"],
                                "line_number": int(error["location"][0]["@line"]),
                                "message": f"{error['@id']}: {error['@verbose']}",
                            }
                        )
                    else:
                        issues.append(
                            {
                                "path": error["location"]["@file"],
                                "line_number": int(error["location"]["@line"]),
                                "message": f"{error['@id']}: {error['@verbose']}",
                            }
                        )
                except KeyError:
                    issues.append(
                        {
                            "path": "?",
                            "line_number": 1,
                            "message": f"{error['@id']}: {error['@verbose']}",
                        }
                    )
            self.__job.issues.append(["combined", issues])
            return len(errors["error"])
        return 0

    @function_debug
    def __clang_collect_issues(self, bugs):
        """Collect issues.

        Collect clang issues for issue reporter.

        :param bugs: amount of clang errors
        """
        if bugs == 0:
            return
        issues = []
        try:
            clang_html = glob(join(self._parameter_value(self.__job, "output"), "*", "index.html"))[0]
        except IndexError as exc:
            raise CLIError("Bug report not found") from exc
        with open(clang_html, encoding="utf-8") as clang_results:
            clang_input_data = bs(clang_results, "html.parser")
            table = clang_input_data.find("table", {"class": "sortable"})
            table_body = table.find("tbody")
            rows = table_body.findAll("tr")
            for row in rows:
                errors = row.findAll("td")
                issues.append(
                    {
                        "path": errors[2].get_text(),
                        "line_number": int(errors[4].get_text()),
                        "message": f"{errors[0].get_text()}: {errors[1].get_text()}",
                    }
                )
        self.__job.issues.append(["combined", issues])

    @function_debug
    def __parse_clang_bugs(self, clang_results):
        """__parse_bugs.

        Parse bugs for Clang

        :param clang_results: Clang results text.
        :return: amount of clang errors
        """
        if re.search(r"scan-build: No bugs found.", clang_results):
            return 0

        bug_search = re.search(r"scan-build: (\d+) bug", clang_results)
        if bug_search:
            return int(bug_search.group(1))

        raise CLIError("Unexpected result for Clang Bugs")


# pylint: enable=too-few-public-methods
