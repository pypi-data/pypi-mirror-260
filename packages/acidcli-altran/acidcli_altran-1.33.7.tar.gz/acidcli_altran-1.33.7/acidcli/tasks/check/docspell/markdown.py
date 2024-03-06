# Copyright Capgemini Engineering B.V.

"""Markdown.

Markdown spelling implementation
"""
import i18n
from loguru import logger

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class MarkdownSpell(Executable):
    """MarkdownSpell."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check documentation spelling.

        Check documentation spelling for Markdown with mdspell

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["input", "output"])

        mdspell_results = self.__convert_mdspell_results(self.__run_mdspell())
        self.__print_readable_mdspell_results(mdspell_results)

        errors = len(mdspell_results)
        QualityGate.find_and_update_quality_gate(self.__job.qualitygates, "DocSpellErrors", errors, mandatory=True)

    @function_debug
    def __run_mdspell(self):
        """Run mdspell.

        Run mdspell command as subprocess for provided files.

        :return: immutable bytes object which contains the mdspell output
        """
        markdown_spell_command = [
            "mdspell",
            "--en-us",
            "--ignore-numbers",
            "--report",
            self._parameter_value(self.__job, "input"),
        ]

        process = Subprocess(markdown_spell_command, verbose=self._parameter_value(self.__job, "verbose"))
        mdspell_output = process.execute_pipe(
            self._parameter_value(self.__job, "output"), "mdspell", check_return_code=False
        )

        return mdspell_output.stdout

    @staticmethod
    @function_debug
    def __convert_mdspell_results(mdspell_results):
        """Convert mdspell results to a list.

        Parse the mdspell results bytes object and convert it into a list of
        mdspell errors with filename, linenumber, and the contents of that line

        :param mdspell_results: mdspell results

        :return: list of dictionaries containing filepath, line_number, and content
        """
        lines = list(filter(None, mdspell_results.decode("utf-8").split("\n")))
        converted_errors = []
        filepath = ""
        for line in lines:
            if "|" in line:
                split_line = line.split("|")
                line_number = int(split_line[0].strip())
                content = split_line[1].strip()
                item = {"filepath": filepath, "line_number": line_number, "content": content}
                converted_errors.append(item)
            else:
                filepath = line.strip()

        return converted_errors

    @staticmethod
    @function_debug
    def __print_readable_mdspell_results(mdspell_results):
        """Print readable mdspell results.

        Parse mdspell results and print user friendly output, with hyperlinks
        to the issue locations

        :param mdspell_results: list of dictionaries containing filepath, linenumber, and content
        """
        for entry in mdspell_results:
            logger.error(
                i18n.t(
                    "acidcli.clickable_path.file",
                    path=entry["filepath"],
                    line_number=entry["line_number"],
                    error_message=f'spelling error: "{entry["content"]}"',
                )
            )


# pylint: enable=too-few-public-methods
