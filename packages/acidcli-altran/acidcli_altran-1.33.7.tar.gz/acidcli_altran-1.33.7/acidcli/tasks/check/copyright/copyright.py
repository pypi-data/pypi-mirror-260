# Copyright Capgemini Engineering B.V.

"""Copyright checker.

Language independent copyright checker
"""
import glob
import os
from itertools import chain
from os.path import join, isfile

import i18n

import acidcli.exceptions
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Copyright(Executable):
    """Copyright checker."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check copyright.

        Check language-independent copyright with custom implementation

        :param job: job model object with job configuration
        """
        self.__job = job
        self.__job.issues = []
        self._required_parameters_available(self.__job, ["output", "format"])
        self._required_list_parameters_available(self.__job, ["config"])

        missing_copyrights = {}

        for code_type in self.__job.parent.parent.code_locations:
            files_to_check = []
            for directory in code_type.directories:
                files_to_check.extend(
                    CopyrightFileChecker.files_with_extension(self._parameter_value(self.__job, "config"), directory)
                )

            copyright_errors = CopyrightFileChecker.files_without_copyright(
                files_to_check, self._parameter_value(self.__job, "format")
            )
            issues = CopyrightFileChecker.collect_issues(copyright_errors)
            self.__job.issues.append([code_type.name, issues])
            CopyrightFileChecker.save_report(
                join(self._parameter_value(self.__job, "output"), f"{code_type.name}_copyright_results.txt"),
                copyright_errors,
            )
            missing_copyrights[code_type.name] = len(copyright_errors)

        self.__update_quality_gates(missing_copyrights)

    @function_debug
    def __update_quality_gates(self, missing_copyrights):
        """Update quality gates.

        Update quality gates with corresponding input values.

        :param missing_copyrights: missing copyrights per code type.
        """
        for code_type, missing in missing_copyrights.items():
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates, f"{code_type}MissingCopyright", missing, mandatory=True
            )


class CopyrightFileChecker:
    """Search files for copyrights."""

    @staticmethod
    @function_debug
    def files_with_extension(extensions, search_directory):
        """Compile list of all files with extensions."""
        file_list = []

        for filename in chain(
            glob.iglob(os.path.normpath(os.path.join(search_directory, "**/*")), recursive=True),
            glob.iglob(os.path.normpath(os.path.join(search_directory, "**/.*")), recursive=True),
        ):
            for extension in extensions:
                if filename.endswith(extension) and isfile(filename):
                    file_list.append(filename)

        return file_list

    @staticmethod
    @function_debug
    def files_without_copyright(file_list, search_string):
        """Check if files contain search string at first line."""
        files_without_disclaimer = []

        for file in file_list:
            with open(file, "r", encoding="utf-8") as source_file:
                content = source_file.readlines()
                if not (len(content) and search_string in content[0]):
                    files_without_disclaimer.append(file)

        return files_without_disclaimer

    @staticmethod
    @function_debug
    def collect_issues(files_without_disclaimer):
        """Collect issues.

        Collect files without copyright disclaimer in the issue reporter.

        :param files_without_disclaimer: files that do now have a copyright disclaimer.
        :return: list of issues
        """
        issues = []
        for location in files_without_disclaimer:
            issues.append(
                {
                    "path": location,
                    "line_number": 1,
                    "message": i18n.t("acidcli.missing_copyright"),
                }
            )
        return issues

    @staticmethod
    @function_debug
    def save_report(report_location, files_without_disclaimer):
        """Save error messages to file."""
        try:
            with open(report_location, "w", encoding="utf-8") as output_file:
                for location in files_without_disclaimer:
                    output_file.write(
                        i18n.t(
                            "acidcli.clickable_path.file",
                            path=location,
                            line_number=1,
                            error_message=i18n.t("acidcli.missing_copyright"),
                        )
                    )
                    output_file.write("\n")
        except FileNotFoundError as error:
            raise acidcli.exceptions.CLIError(i18n.t("acidcli.process.file_not_found_error", file=error.filename))


# pylint: enable=too-few-public-methods
