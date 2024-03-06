# Copyright Capgemini Engineering B.V.

"""Markdown.

Markdown linting implementation
"""
import i18n
from loguru import logger

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class MarkdownLint(Executable):
    """MarkdownLint."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check documentation linting.

        Check documentation linting for markdown with mdl

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["config", "input", "output"])

        mdl_results = self.__convert_mdl_results(self.__run_mdl())
        self.__print_readable_mdl_results(mdl_results)

        errors = len(mdl_results)

        QualityGate.find_and_update_quality_gate(self.__job.qualitygates, "DocLintErrors", errors, mandatory=True)

    @function_debug
    def __run_mdl(self):
        """Run mdl.

        Run mdl command as subprocess for provided files.

        :return: immutable bytes object which contains the mdl output
        """
        lint_markdown_command = [
            "mdl",
            "--style",
            self._parameter_value(self.__job, "config"),
            self._parameter_value(self.__job, "input"),
        ]

        process = Subprocess(lint_markdown_command, verbose=self._parameter_value(self.__job, "verbose"))
        markdownlint_output = process.execute_pipe(
            self._parameter_value(self.__job, "output"), "markdownlint", check_return_code=False
        )

        return markdownlint_output.stdout

    @staticmethod
    @function_debug
    def __convert_mdl_results(mdl_results):
        """Convert mdl results  to a list.

        Parses the mdl results bytes object and convert it into a list of
        mdl errors with filename, linenumber, and error description

        :param mdl_results: mdl results

        :return: list of dictionaries containing filepath, line_number, and description
        """
        lines = list(filter(None, mdl_results.decode("utf-8").splitlines()))
        converted_errors = []

        for line in lines[:-1]:
            if "Further documentation is available for these failures:" in line:
                break
            split_line = line.split(":")

            description = split_line[-1].strip()
            line_number = int(split_line[-2])
            filepath = "".join(split_line[:-2])

            item = {"filepath": filepath, "line_number": line_number, "description": description}
            converted_errors.append(item)

        return converted_errors

    @staticmethod
    @function_debug
    def __print_readable_mdl_results(mdl_results):
        """Print readable mdl results.

        Parse mdl results and print user friendly output, with hyperlinks
        to the issue locations

        :param mdl_results: list of dictionaries containing filepath, line_number, and description
        """
        for result in sorted(mdl_results, key=lambda x: (x["filepath"], x["line_number"])):
            logger.error(
                i18n.t(
                    "acidcli.clickable_path.file",
                    path=result["filepath"],
                    line_number=result["line_number"],
                    error_message=result["description"],
                )
            )


# pylint: enable=too-few-public-methods
