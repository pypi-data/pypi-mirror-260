# Copyright Capgemini Engineering B.V.

"""Format Python.

Code formatting using Black
"""
import re

import i18n
from loguru import logger

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Black(Executable):
    """Black."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check python format.

        Check format for python with black.

        :param job: job model object with job configuration.
        """
        self.__job = job
        self.__job.issues = []
        self._required_parameters_available(self.__job, ["output"])

        is_pipeline = self._parameter_value(self.__job, "version").is_pipeline()
        reformat_count_per_code_type = {}

        for code_type in self.__job.parent.parent.code_locations:
            black_output = self.__run_black(code_type.directories, code_type.name)
            reformat_count_per_code_type[code_type.name] = self.__get_reformat_count(black_output, is_pipeline)
            self.__collect_issues(black_output, code_type.name)
            if not is_pipeline:
                logger.info(
                    i18n.t(
                        "acidcli.files_formatted",
                        files_count=reformat_count_per_code_type[code_type.name],
                    )
                )
                reformat_count_per_code_type[code_type.name] = 0
            self.__update_quality_gate(code_type.name, reformat_count_per_code_type[code_type.name])

    @function_debug
    def __run_black(self, directories, code_type):
        """Run black.

        Run black command as subprocess for provided directories.

        :param directories: list with directories that should be formatted by black.
        :param code_type: string which generalizes the type of code found in provided directories.
        :return: decoded black output.
        """
        black_command = ["black"]
        black_command.extend(directories)

        if self._parameter_value(self.__job, "version").is_pipeline():
            logger.info(i18n.t("acidcli.pipeline.format_check"))
            black_command.append("--diff")
        else:
            logger.info(i18n.t("acidcli.pipeline.format_fix"))

        process = Subprocess(black_command, verbose=self._parameter_value(self.__job, "verbose"))
        black_output = process.execute_pipe(self._parameter_value(self.__job, "output"), f"black_{code_type}")
        return black_output.stdout.decode("utf-8")

    @staticmethod
    @function_debug
    def __get_reformat_count(black_output, is_pipeline):
        """Get Reformat count.

        Extract the reformat count from the black output.

        :param black_output: decoded black output.
        :return: amount of files reformatted by black.
        """
        regex_remote = r"(\d*) file[s]? would be reformatted"
        regex_local = r"(\d*) file[s]? reformatted"
        capture = re.search(regex_remote if is_pipeline else regex_local, black_output)
        if capture:
            return int(capture.group(1))
        return 0

    @function_debug
    def __update_quality_gate(self, code_type, reformat_counts):
        """Update quality gate.

        Update quality gate with corresponding input value.

        :param code_type: code type to set the quality gates for.
        :param reformat_counts: amount of files reformatted by black.
        """
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, f"{code_type}ReformatErrors", reformat_counts
        )

    @function_debug
    def __collect_issues(self, black_output, code_type):
        """Collect issues.

        Collect format errors in issuereporter.

        :param black_output: decoded black output.
        :param code_type: location where the issues have been found
        """
        issues = []
        captures = re.findall("would reformat (.*)", black_output)
        for capture in captures:
            issues.append({"path": capture, "line_number": 1, "message": i18n.t("acidcli.format_needed")})
        self.__job.issues.append([code_type, issues])
