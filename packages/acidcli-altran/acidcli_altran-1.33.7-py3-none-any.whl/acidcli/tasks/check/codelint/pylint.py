# Copyright Capgemini Engineering B.V.

"""Python linting.

Source code linter for Python
"""
from json import loads
from os.path import join

import i18n

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess, ProcessError
from acidcli.tasks.executable import Executable
from acidcli.quality_gate import QualityGate


# pylint: disable=too-few-public-methods
class PythonLint(Executable):
    """PythonLint."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check code linting.

        Check code linting for Python with pylint

        :param job: job model object with job configuration
        """
        self.__job = job
        self.__job.issues = []
        self._required_parameters_available(self.__job, ["config", "output"])

        pylint_metrics = {}

        for code_type in self.__job.parent.parent.code_locations:
            pylint_metrics[code_type.name] = {
                "error": {"value": 0, "mandatory": True},
                "warning": {"value": 0, "mandatory": False},
                "refactor": {"value": 0, "mandatory": False},
                "convention": {"value": 0, "mandatory": False},
            }
            pylint_results_with_color_characters = self.__run_pylint(code_type.name, code_type.directories)
            pylint_results_with_color_characters = pylint_results_with_color_characters.replace(b"\x1b[0m", b"")
            pylint_results = loads(pylint_results_with_color_characters)

            for entry in pylint_results:
                if entry["type"] == "fatal":
                    raise ProcessError(i18n.t("acidcli.pylint_error", error=entry["message"]))

            self.__collect_issues(pylint_results, code_type.name)
            self.__write_parseable_pylint_results(
                pylint_results, self._parameter_value(self.__job, "output"), code_type.name
            )
            self.__calculate_pylint_metrics(pylint_metrics[code_type.name], pylint_results)
            self.__add_quality_gate_input_values(code_type.name, pylint_metrics[code_type.name])

    @function_debug
    def __run_pylint(self, code_type, files):
        """Run pylint.

        Run pylint command as subprocess for provided files.

        :param code_type: identifier to disable rules based on code type
        :param files: list of files or directories to be scanned
        """
        pylint_command = [
            "pylint",
            f"--rcfile={self._parameter_value(self.__job, 'config')}",
            "--output-format=json",
        ]

        if code_type.lower() == "test":
            pylint_command.append("--disable=C0114,C0115,C0116,R0903,R0904")

        pylint_command.extend(files)

        process = Subprocess(pylint_command, verbose=self._parameter_value(self.__job, "verbose"))
        pylint_output = process.execute_pipe(
            self._parameter_value(self.__job, "output"), "pylint", check_return_code=False
        )

        return pylint_output.stdout

    @function_debug
    def __collect_issues(self, pylint_results, code_type):
        """Collect issues.

        Collect pylint results in issuereporter.

        :param pylint_results: pylint results in dictionary
        :param code_type: location where the issues have been found
        """
        issues = []
        for entry in sorted(pylint_results, key=lambda t: t["message-id"]):
            issues.append(
                {
                    "path": entry["path"],
                    "line_number": int(entry["line"]),
                    "message": f"{entry['type']} [{entry['message-id']}({entry['symbol']})] {entry['message']}",
                }
            )
        self.__job.issues.append([code_type, issues])

    @staticmethod
    @function_debug
    def __write_parseable_pylint_results(pylint_results, output_directory, codetype):
        """Write parseable pylint results.

        Write the pylint results to a file in the output folder

        :param pylint_results: List of elements with the pylint results
        :param output_directory: directory where the output file is placed
        :param codetype: code type to set the quality gates for
        """
        previous_module = ""

        with open(join(output_directory, f"parseable_{codetype}.results"), "w", encoding="utf-8") as file:
            for entry in sorted(pylint_results, key=lambda t: t["module"]):
                if entry["module"] != previous_module:
                    file.write(f"************* Module {entry['module']}\n")
                    previous_module = entry["module"]

                file.write(
                    f"{entry['path']}:{entry['line']}: "
                    f"[{entry['message-id']}({entry['symbol']}), {entry['obj']}] {entry['message']}\n"
                )

    @staticmethod
    @function_debug
    def __calculate_pylint_metrics(pylint_metrics, pylint_results):
        """Calculate code lint metrics summary.

        Parse code lint results and calculate metrics summary stored into metrics dictionary.

        :param pylint_metrics: pylint metrics summary dictionary
        :param pylint_results: pylint results in dictionary
        """
        for entry in pylint_results:
            try:
                pylint_metrics[entry["type"]]["value"] += 1
            except KeyError:
                pylint_metrics[entry["type"]] = {"value": 1, "mandatory": False}

    @function_debug
    def __add_quality_gate_input_values(self, code_type, pylint_metrics):
        """Add quality gate input values.

        Update quality gates with corresponding input values.

        :param code_type: code type to set the quality gates for
        :param pylint_metrics: pylint metrics summary
        """
        for metric, collection in pylint_metrics.items():
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates,
                f"{code_type}Lint{metric.capitalize()}",
                collection["value"],
                mandatory=collection["mandatory"],
            )


# pylint: enable=too-few-public-methods
