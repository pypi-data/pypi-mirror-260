# Copyright Capgemini Engineering B.V.

"""Building binaries.

Building binaries using MSBuild
"""
import copy
from json import loads
import os
import glob
import re
import shutil

from collections import Counter
from loguru import logger

import i18n

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess, ProcessError
from acidcli.exceptions import CLIError
from acidcli.tasks.executable import Executable
from acidcli.quality_gate import QualityGate


# pylint: disable=too-few-public-methods
class CSharp(Executable):
    """CSharp Build Binaries."""

    __ERROR_LOG = "ErrorLog.json"

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Build the binaries."""
        self.__job = job
        self._required_parameters_available(self.__job, ["input", "type", "output"])

        self.__build_binaries()
        error_logs = self.__find_error_logs()
        identifiers, structured_error_output = self.__process_error_output(copy.deepcopy(error_logs))
        self.__copy_error_output(copy.deepcopy(error_logs))
        self.__collect_issues(structured_error_output)
        self.__update_quality_gates(identifiers)

    @function_debug
    def __build_binaries(self):
        """Run MSBuild to build the binaries.

        Build C# binaries.

        """
        binaries_build_command = ["MSBuild", "/nr:false",
                                  f"/property:Configuration={self._parameter_value(self.__job, 'type')}", "/m",
                                  f"/property:ErrorLog={self.__ERROR_LOG}"]

        if self._parameter_value(self.__job, "platform"):
            binaries_build_command.append(f"/p:Platform={self._parameter_value(self.__job, 'platform')}")

        binaries_build_command.append(self._parameter_value(self.__job, "input"))

        try:
            process = Subprocess(binaries_build_command, verbose=self._parameter_value(self.__job, "verbose"))
            process.execute_pipe(self._parameter_value(self.__job, "output"), "msbuild")
        except ProcessError as error:
            errors = self.__parse_command_output_error(error.command_output)
            raise CLIError(i18n.t("acidcli.build_csharp_error", errors=errors)) from error

    @staticmethod
    @function_debug
    def __parse_command_output_error(stdout):
        """Parse command output error.

        Parse errors from MSBuild.
        The lines in between "Build FAILED", and "x Warning(s)" are parsed.
        The lines with the "->" symbol are skipped, so only the errors are shown.

        :param: stdout: stdout to search.
        :return: String with found errors.
        """
        found_errors = []
        stdout_lines = stdout.splitlines()
        relevant_output = False
        for line in stdout_lines:
            if "Warning(s)" in line:
                relevant_output = False
            if relevant_output and "error" in line:
                found_errors.append(line.strip())
            if "Build FAILED" in line:
                relevant_output = True
        return "\n".join(found_errors).strip()

    @function_debug
    def __find_error_logs(self):
        """__find_error_logs.

        find all errorlog files.

        :return: list of errorlog file path.
        """
        error_logs = glob.glob(os.path.join(".", "**", self.__ERROR_LOG), recursive=True)

        return error_logs

    @staticmethod
    @function_debug
    def __process_error_output(error_logs):
        """Process error output.

        Parse all errors logs.

        Sort found errors by ruleId and then startLine number.

        :return: dict of compiler type occurrences, dict containing structured error output.
        """
        logger.debug(f"Log file count: {len(error_logs)}")

        results = []
        identifiers = []

        for error_log in error_logs:
            with open(error_log, "r", encoding="UTF-8") as raw_error_log:
                error_log = loads(raw_error_log.read())

            for run in error_log["runs"]:
                for entry in run["results"]:
                    if "suppressionStates" in entry:
                        continue

                    # Remove duplicate ending sentence dot
                    if entry["message"].endswith("."):
                        entry["message"] = entry["message"][:-1]

                    if "locations" in entry:
                        # Replace absolute path with relative path
                        entry["locations"][0]["resultFile"]["uri"] = \
                            entry["locations"][0]["resultFile"]["uri"].replace(
                            f"file:///{os.getcwd()}/".replace("\\", "/"), "").replace("/", "\\")

                    results.append(entry)
                    identifier = re.search("([A-Z]+)", entry["ruleId"]).group()
                    identifiers.append(identifier)

        identifiers = Counter(identifiers)

        sorted_results = sorted(results,
                                key=lambda x: (
                                    x["ruleId"],
                                    x.get("locations",
                                          [
                                              {"resultFile": {"region": {"startLine": 0}}}
                                          ])
                                    [0]["resultFile"]["region"]["startLine"]
                                ))

        return identifiers, sorted_results

    @function_debug
    def __copy_error_output(self, error_logs):
        """Copy error output.

        Copy all error logs to output folder.

        :param structured_error_output: dict containing structured error output.
        """
        for error_log in error_logs:
            error_log_lower = error_log.replace("\\", "_")
            dest = os.path.join(self._parameter_value(self.__job, "output"), error_log_lower)

            shutil.copyfile(error_log, dest)

    @function_debug
    def __collect_issues(self, structured_error_output):
        """Collect issues.

        Collect issues for issue reporter.

        :param structured_error_output: dict containing structured error output.
        """
        issues = []
        for result in structured_error_output:
            if "locations" in result:
                issues.append(
                    {
                        "path": result["locations"][0]["resultFile"]["uri"],
                        "line_number": int(result["locations"][0]["resultFile"]["region"]["startLine"]),
                        "message": f"{result['ruleId']} {result['message']}",
                    })
            else:
                issues.append(
                    {
                        "path": "?",
                        "line_number": 1,
                        "message": f"{result['ruleId']} {result['message']}",
                    })

        self.__job.issues = [['combined', issues]]

    @function_debug
    def __update_quality_gates(self, identifiers):
        """Update quality gates.

        Update all quality gate values.

        :param identifiers: dict containing counts of compiler identifiers.
        """
        existing_keys = []
        for identifier, count in identifiers.items():
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates, f"buildWarnings{identifier}", count, mandatory=True)
            existing_keys.append(f"buildWarnings{identifier}")

        for quality_gate in [quality_gate for quality_gate in self.__job.qualitygates if
                             quality_gate.metric not in existing_keys]:
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates, quality_gate.metric, 0, mandatory=True)

# pylint: enable=too-few-public-methods
