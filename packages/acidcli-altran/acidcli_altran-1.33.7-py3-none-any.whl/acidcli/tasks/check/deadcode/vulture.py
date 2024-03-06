# Copyright Capgemini Engineering B.V.

"""Vulture.

Python check deadcode implementation
"""

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable
from acidcli.quality_gate import QualityGate


# pylint: disable=too-few-public-methods
class Vulture(Executable):
    """Vulture."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check dead code.

        Check dead code for Python with vulture.

        :param job: job model object with job configuration.
        """
        self.__job = job
        self.__job.issues = []
        self._required_parameters_available(self.__job, ["output"])

        vulture_results = {}
        for code_type in self.__job.parent.parent.code_locations:
            vulture_output = self.__run_vulture(code_type.directories)
            errors = self.__parse_vulture_output(vulture_output)
            self.__collect_issues(errors, code_type.name)
            vulture_results[code_type.name] = len(errors)

        self.__update_quality_gate_input_value(vulture_results)

    @function_debug
    def __run_vulture(self, directories):
        """Run vulture.

        Run vulture command as subprocess for provided files.

        :param directories: list of files or directories to be scanned
        :return: decoded vulture output
        """
        vulture_command = ["vulture"]
        vulture_command.extend(directories)
        if whitelist := self._parameter_value(self.__job, "config"):
            vulture_command.append(whitelist)

        process = Subprocess(vulture_command, verbose=self._parameter_value(self.__job, "verbose"))
        vulture_output = process.execute_pipe(
            self._parameter_value(self.__job, "output"), "vulture", check_return_code=False
        )

        return vulture_output.stdout.decode("utf-8")

    @staticmethod
    @function_debug
    def __parse_vulture_output(vulture_output):
        """Parse vulture output.

        Parse vulture output and extract amount of errors found.

        :param vulture_output: decoded vulture output.
        :return: found errors as dictionary.
        """
        errors = []

        for line in vulture_output.splitlines():
            line_parts = line.split(":")
            error = {"path": line_parts[0], "line": line_parts[1], "message": line_parts[2]}
            errors.append(error)

        return errors

    @function_debug
    def __collect_issues(self, errors, code_type):
        """Collect issues.

        Collect deadcode errors in issuereporter.

        :param errors: deadcode errors.
        :param code_type: location where the issues have been found
        """
        issues = []
        for error in errors:
            issues.append(
                {
                    "path": error["path"],
                    "line_number": int(error["line"]),
                    "message": error["message"],
                }
            )
        self.__job.issues.append([code_type, issues])

    @function_debug
    def __update_quality_gate_input_value(self, vulture_results):
        """Update quality gate input value.

        Update quality gates with corresponding input value.

        :param vulture_results: amount of errors found by vulture per code_type.
        """
        for code_type, amount_of_errors in vulture_results.items():
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates,
                f"{code_type}DeadcodeErrors",
                amount_of_errors,
                mandatory=True,
            )


# pylint: enable=too-few-public-methods
