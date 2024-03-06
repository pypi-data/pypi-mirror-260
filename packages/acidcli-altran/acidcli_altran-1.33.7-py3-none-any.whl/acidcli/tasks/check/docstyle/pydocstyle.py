# Copyright Capgemini Engineering B.V.

"""Pydocstyle.

Python documentation style implementation
"""
import i18n
from loguru import logger


from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable
from acidcli.exceptions import CLIError


# pylint: disable=too-few-public-methods
class PyDocStyle(Executable):
    """PyDocStyle."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check doc style.

        Check doc style for Python with pydocstyle.

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["input", "output"])

        docstyle_output = self.__run_pydocstyle()

        issues = self.__parse_docstyle(docstyle_output)
        actual_number_of_issues = self.__check_fatal_errors(issues)
        self.__check_quality_gates(actual_number_of_issues)

    @function_debug
    def __run_pydocstyle(self):
        """Run pydocstyle.

        Run pydocstyle command as subprocess.

        :return: decoded pydocstyle command output
        """
        input_argument = self._parameter_value(self.__job, "input")
        docstyle_command = [
            "pydocstyle",
            "--count",
            input_argument,
        ]

        process = Subprocess(docstyle_command, verbose=self._parameter_value(self.__job, "verbose"))
        docstyle_output = process.execute_pipe(
            self._parameter_value(self.__job, "output"), "pydocstyle", check_return_code=False
        )

        return docstyle_output.stdout.decode("utf-8")

    @function_debug
    def __parse_docstyle(self, docstyle_output):
        """Parse docstyle.

        Extract issues from pydocstyle output. Collect errors in issue reporter.

        :param docstyle_output: decoded pydocstyle output.
        :return: number of issues per type.
        """
        issues = []
        issues_per_type = {
            "Warning": 0,
            "DocstyleEntry": 0,
            "NumberOfRecords": int,
        }

        path = line_number = function = ""
        lines = docstyle_output.splitlines()
        for line in lines:
            if line.startswith("WARNING: "):
                logger.error(line)
                issues_per_type["Warning"] += 1
            elif not line.startswith(" "):
                split_line = line.split(":")
                if len(split_line) == 1:
                    number_of_issues = int(split_line[0])
                    issues_per_type["NumberOfRecords"] = number_of_issues
                else:
                    path = split_line[0]
                    function_line_number_split = split_line[1].split(" ", 1)
                    line_number = function_line_number_split[0]
                    function = function_line_number_split[1]
            else:
                issues.append(
                    {
                        "path": path,
                        "line_number": line_number,
                        "message": f"{function} -> {line.strip()}",
                    }
                )
                issues_per_type["DocstyleEntry"] += 1

        self.__job.issues = [["combined", issues]]
        return issues_per_type

    @staticmethod
    @function_debug
    def __check_fatal_errors(issues):
        """Check for fatal errors in docsyle output.

        Check fatal errors in the output of docstyle. When warnings found, raise a CLIError.

        :param issues: structure with all docstyle warnings and errors
        :returns the total amount of docstyle warnings and issues
        """
        number_of_warnings = issues["Warning"]
        actual_number_of_issues = number_of_warnings + issues["DocstyleEntry"]
        number_of_records = issues["NumberOfRecords"]
        if number_of_warnings > 0:
            raise CLIError(i18n.t("acidcli.pydocstyle_parse_output_file_failed_warnings_detected"))
        if number_of_records != actual_number_of_issues:
            raise CLIError(
                i18n.t(
                    "acidcli.pydocstyle_parse_output_file_number_of_issues_mismatch",
                    expected=number_of_records,
                    found=actual_number_of_issues,
                )
            )
        return actual_number_of_issues

    @function_debug
    def __check_quality_gates(self, number_of_issues):
        """Check Quality Gates.

        Update Quality Gates.

        :param number_of_issues: int with number of issues
        """
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            "DocStyleErrors",
            number_of_issues,
            mandatory=True,
        )


# pylint: enable=too-few-public-methods
