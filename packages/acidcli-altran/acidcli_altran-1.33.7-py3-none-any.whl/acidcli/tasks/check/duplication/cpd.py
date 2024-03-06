# Copyright Capgemini Engineering B.V.

"""Copy paste detection.

Generic copy paste detection implementation
"""
import os
from pathlib import Path

from xmltodict import parse as parse_xml

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class CopyPasteDetection(Executable):
    """CopyPasteDetection."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check code duplication.

        Check code duplication for various languages with cpd.

        :param job: job model object with job configuration.
        """
        self.__job = job
        self.__job.issues = []
        self._required_parameters_available(self.__job, ["minimum_tokens", "output"])

        duplications = {}

        for code_type in self.__job.parent.parent.code_locations:
            duplications[code_type.name] = 0
            cpd_results = parse_xml(self.__run_pmd_cpd(code_type.directories, code_type.name))
            duplicates = self.__determine_duplicates(cpd_results)

            for duplicate in duplicates:
                duplications[code_type.name] += self.__determine_occurrences_per_duplicate(duplicate)

            self.__set_qualitygates(code_type.name, duplications[code_type.name])
            self.__collect_issues(code_type.name, duplicates)

    @function_debug
    def __run_pmd_cpd(self, directories, code_type):
        """Run pmd-cpd.

        Run pmd-cpd as subprocess.

        :param directories: locations that should be scanned for copy pasting.
        :param code_type: string which generalizes the type of code found in provided directories.
        :return: immutable bytes object containing the cpd output.
        """
        duplication_command = [
            "cpd",
            "--minimum-tokens",
            f"{self._parameter_value(self.__job, 'minimum_tokens')}",
            "--language",
            self.__job.language,
            "--format",
            "xml",
            "--dir",
        ]
        duplication_command.extend(directories)

        process = Subprocess(duplication_command, verbose=self._parameter_value(self.__job, "verbose"))
        cpd_output = process.execute_pipe(
            self._parameter_value(self.__job, "output"), f"cpd_{code_type}", check_return_code=False
        )

        return cpd_output.stdout

    @staticmethod
    @function_debug
    def __determine_duplicates(cpd_results):
        """Determine duplications.

        Determine duplications in the provided list.

        :param cpd_results: dictionary with cpd_results.
        :return: list with duplications.
        """
        try:
            issue_types = cpd_results["pmd-cpd"]["duplication"]
            if not isinstance(issue_types, list):
                return [issue_types]
            return issue_types
        except TypeError:
            return []
        except KeyError:
            return []

    @staticmethod
    @function_debug
    def __determine_occurrences_per_duplicate(duplication):
        """Determine occurrences per duplicate.

        Determine how many times a single code fragment has been duplicated.

        :param duplication: list containing all locations of a duplicated code fragment.
        :return: duplication count.
        """
        try:
            issue_types = duplication["file"]
            return len(issue_types) - 1
        except KeyError:
            return 0

    @function_debug
    def __set_qualitygates(self, code_type, duplications):
        """Set quality gates.

        Update Quality Gates.

        :param code_type: code type in which duplications are found.
        :param duplications: number of duplications.
        """
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, f"{code_type}DuplicationErrors", duplications
        )

    @function_debug
    def __collect_issues(self, code_type, duplications):
        """Collect issues.

        Collect duplicated code fragments in the issuereporter.

        :param code_type: code type in which duplications are found.
        :param duplications: duplications which should be printed.
        """
        issues = []
        current_work_dir = Path(os.getcwd())

        for duplicate in duplications:
            if "file" in duplicate:
                for index_files, file in enumerate(duplicate["file"]):
                    absolute_file_path = Path(file["@path"])
                    relative_file_path = str(absolute_file_path).replace(str(current_work_dir), "")[1:]

                    issues.append(
                        {
                            "path": relative_file_path,
                            "line_number": int(file["@line"]),
                            "message": f"Part ({index_files + 1})/({len(duplicate['file'])}) "
                            f"for {code_type}Duplication",
                        }
                    )
        self.__job.issues.append([code_type, issues])


# pylint: enable=too-few-public-methods
