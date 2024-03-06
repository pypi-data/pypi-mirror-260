# Copyright Capgemini Engineering B.V.

"""Gherkin.

Gherkin linting implementation
"""
import os
import json

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class GherkinLint(Executable):
    """GherkinLint."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check gherkin_lint.

        Check gherkin_lint for Python with gherkin.

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["input", "output", "config"])

        gherkin_output = self.__run_gherkinlint()
        errors = self.__parse_gherkinlint_results(gherkin_output)
        self.__collect_issues(errors)
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, "FeatureLintErrors", len(errors), mandatory=True
        )

    @function_debug
    def __run_gherkinlint(self):
        """Run gherkin_lint.

        Run gherkin_lint command as subprocess.

        :return: decoded gherkin_lint command output
        """
        input_argument = self._parameter_value(self.__job, "input")
        config = self._parameter_value(self.__job, "config")
        gherkin_command = [
            "gherkin-lint",
            "-f",
            "json",
            "-c",
            config,
            input_argument,
        ]

        process = Subprocess(gherkin_command, verbose=self._parameter_value(self.__job, "verbose"))
        gherkin_output = process.execute_pipe(
            self._parameter_value(self.__job, "output"), "gherkin-lint", check_return_code=False
        )

        return gherkin_output.stdout.decode("utf-8")

    @staticmethod
    @function_debug
    def __parse_gherkinlint_results(gherkin_output):
        """Parse gherkin_lint.

        Extract issues from gherkin_lint output.

        :param gherkin_output: decoded gherkin_lint output.
        :return: issues.
        """
        errors = []

        data = json.loads(gherkin_output)

        for featurefile in data:
            filepath = featurefile["filePath"]
            for error in featurefile["errors"]:
                error["filepath"] = filepath
                errors.append(error)

        return errors

    @function_debug
    def __collect_issues(self, issues):
        """Collect issues.

        Collect gherkin_lint results in issue reporter.

        :param issues: array containing issues.
        """
        reported_issues = []
        for issue in issues:
            path = os.path.join(".", os.path.relpath(issue["filepath"]))
            reported_issues.append(
                {
                    "path": path,
                    "line_number": int(issue["line"]),
                    "message": f"{issue['rule']}: {issue['message']}",
                }
            )
        self.__job.issues = [["combined", reported_issues]]


# pylint: enable=too-few-public-methods
