# Copyright Capgemini Engineering B.V.

"""Python vulnerability checker.

Vulnerability checker for Python
"""
import os
from json import loads

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable
from acidcli.quality_gate import QualityGate


# pylint: disable=too-few-public-methods
class Bandit(Executable):
    """Bandit."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check code security.

        Check code vulnerabilities for Python with bandit

        :param job: job model object with job configuration
        """
        self.__job = job
        self.__job.issues = []
        self._required_parameters_available(self.__job, ["output"])

        bandit_metrics = {}

        for code_type in self.__job.parent.parent.code_locations:
            bandit_metrics[code_type.name] = {"high": 0, "medium": 0, "low": 0, "undefined": 0, "skipped": 0}
            bandit_results = loads(self.__run_bandit(code_type.name, code_type.directories))

            self.__collect_issues(bandit_results, code_type.name)
            self.__populate_bandit_metrics(bandit_metrics[code_type.name], bandit_results)
            self.__add_quality_gate_input_values(code_type.name, bandit_metrics[code_type.name])

    @function_debug
    def __run_bandit(self, code_type, files):
        """Run bandit.

        Run bandit command as subprocess for provided files.

        :param code_type: identifier to disable rules based on code type
        :param files: list of files or directories to be scanned
        """
        bandit_command = [
            "bandit",
            "--format",
            "json",
            "--recursive",
            "--quiet",
        ]

        if code_type.lower() == "test":
            bandit_command.append("--skip")
            bandit_command.append("B101")

        for file in files:
            bandit_command.append(os.path.normpath(file))

        process = Subprocess(bandit_command, verbose=self._parameter_value(self.__job, "verbose"))
        bandit_output = process.execute_pipe(
            self._parameter_value(self.__job, "output"), "bandit", check_return_code=False
        )

        return bandit_output.stdout

    @function_debug
    def __collect_issues(self, bandit_results, code_type):
        """Collect issues.

        Collect bandit results in issuereporter.

        :param bandit_results: bandit results in dictionary
        :param code_type: code location where the issues have been found
        """
        issues = []
        for entry in sorted(bandit_results["results"], key=lambda t: t["test_id"]):
            issues.append(
                {
                    "path": entry["filename"],
                    "line_number": int(entry["line_number"]),
                    "message": f"[{entry['issue_severity']} ({entry['test_id']})] {entry['issue_text']}",
                }
            )
        self.__job.issues.append([code_type, issues])

    @staticmethod
    @function_debug
    def __populate_bandit_metrics(bandit_metrics, bandit_results):
        """Populate metrics summary.

        Parse vulnerability results and create summary in metrics dictionary

        :param bandit_metrics: bandit metrics summary dictionary
        :param bandit_results: bandit results in dictionary
        """
        bandit_metrics["high"] = int(bandit_results["metrics"]["_totals"]["SEVERITY.HIGH"])
        bandit_metrics["medium"] = int(bandit_results["metrics"]["_totals"]["SEVERITY.MEDIUM"])
        bandit_metrics["low"] = int(bandit_results["metrics"]["_totals"]["SEVERITY.LOW"])
        bandit_metrics["undefined"] = int(bandit_results["metrics"]["_totals"]["SEVERITY.UNDEFINED"])
        bandit_metrics["skipped"] = int(bandit_results["metrics"]["_totals"]["nosec"])

    @function_debug
    def __add_quality_gate_input_values(self, code_type, bandit_metrics):
        """Add quality gate input values.

        Update quality gates with corresponding input values.

        :param code_type: code type to set the quality gates for
        :param bandit_metrics: bandit metrics summary dictionary
        """
        for metric in bandit_metrics:
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates,
                f"{code_type}Vulnerability{metric.capitalize()}",
                bandit_metrics[metric],
            )


# pylint: enable=too-few-public-methods
