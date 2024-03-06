# Copyright Capgemini Engineering B.V.

"""Pycodestyle.

Python code style implementation
"""
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class PyCodeStyle(Executable):
    """PyCodeStyle."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check code style.

        Check code style for Python with pycodestyle.

        :param job: job model object with job configuration
        """
        self.__job = job
        self.__job.issues = []
        self._required_parameters_available(self.__job, ["config", "output"])

        issues = {}
        for code_type in self.__job.parent.parent.code_locations:
            codestyle_output = self.__run_pycodestyle(code_type.directories)
            issues_per_severity_level = self.__parse_codestyle(codestyle_output)
            issues[code_type.name] = issues_per_severity_level
            self.__collect_issues(issues_per_severity_level, code_type.name)

        self.__update_quality_gates(issues)

    @function_debug
    def __run_pycodestyle(self, directories):
        """Run pycodestyle.

        Run pycodestyle command as subprocess for provided files.

        :param directories: list of directories to be scanned
        :return: decoded pycodestyle command output
        """
        codestyle_command = [
            "pycodestyle",
            f"--config={self._parameter_value(self.__job, 'config')}",
        ]
        codestyle_command.extend(directories)

        process = Subprocess(codestyle_command, verbose=self._parameter_value(self.__job, "verbose"))
        codestyle_output = process.execute_pipe(
            self._parameter_value(self.__job, "output"), "pycodestyle", check_return_code=False
        )

        return codestyle_output.stdout.decode("utf-8")

    @staticmethod
    @function_debug
    def __parse_codestyle(codestyle_output):
        """Parse codestyle.

        extract issues from pycodestyle output.

        :param codestyle_output: decoded pycodestyle output.
        :return: issues per severity.
        """
        issues_per_severity_level = {
            "Error": [],
            "Warning": [],
        }

        for line in codestyle_output.splitlines():
            split_line = line.split(":")
            trailing = ":".join(split_line[3:])
            code = trailing[1:5]
            message = trailing[6:]
            issue = {"path": split_line[0], "line": split_line[1], "code": code, "message": message}
            if code.startswith("E"):
                issues_per_severity_level["Error"].append(issue)
            else:
                issues_per_severity_level["Warning"].append(issue)

        return issues_per_severity_level

    @function_debug
    def __collect_issues(self, issues_per_severity, code_type):
        """Collect issues.

        Collect pycodestyle results in issuereporter.

        :param issues_per_severity: dictionary containing issues per severity.
        :param code_type: location where the issues have been found
        """
        reported_issues = []
        for issues in issues_per_severity.values():
            for issue in issues:
                reported_issues.append(
                    {
                        "path": issue["path"],
                        "line_number": int(issue["line"]),
                        "message": f"{issue['code']} {issue['message']}",
                    }
                )
        self.__job.issues.append([code_type, reported_issues])

    @function_debug
    def __update_quality_gates(self, issues_per_code_type):
        """Update quality gates.

        Update quality gates with corresponding input values.

        :param issues_per_code_type:  issues per code_type.
        """
        for code_type, issues in issues_per_code_type.items():
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates,
                f"{code_type}CodeStyleWarning",
                len(issues["Warning"]),
            )
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates,
                f"{code_type}CodeStyleError",
                len(issues["Error"]),
                mandatory=True,
            )


# pylint: enable=too-few-public-methods
