# Copyright Capgemini Engineering B.V.

"""Lizard.

Lizard complexity implementation
"""
import re
from os.path import join

import i18n
from loguru import logger
from xmltodict import parse as parse_xml

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate, QualityGateError
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Lizard(Executable):
    """Lizard."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check code complexity.

        Check code complexity  with lizard.

        :param job: job model object with job configuration.
        """
        self.__job = job
        self.__job.issues = []
        self._required_parameters_available(self.__job, ["output"])

        total_results = {}
        for code_type in self.__job.parent.parent.code_locations:
            lizard_results = self.__parse_lizard_results(
                parse_xml(self.__run_lizard(code_type.directories, code_type.name)), code_type.name
            )
            total_results.update(lizard_results)
            self.__write_readable_results_to_file(lizard_results, code_type.name)
            self.__collect_issues(lizard_results, code_type.name)
            self.__set_quality_gates(lizard_results, code_type.name)

    @function_debug
    def __run_lizard(self, directories, code_type):
        """Run lizard.

        Run lizard command as subprocess for provided directories.

        :param directories: list with directories that should be checked by lizard.
        :param code_type: string which generalizes the type of code found in provided directories.

        :return: immutable bytes object containing the lizard output.
        """
        complexity_command = [
            "lizard",
            "--xml",
        ]

        exclude_list = self._parameter_value(self.__job, "exclude")

        if exclude_list:
            for exclude_path in exclude_list:
                complexity_command.extend(["--exclude", exclude_path])

        complexity_command.extend(directories)

        process = Subprocess(complexity_command, verbose=self._parameter_value(self.__job, "verbose"))
        lizard_output = process.execute_pipe(self._parameter_value(self.__job, "output"), f"lizard_{code_type}")
        return lizard_output.stdout

    @function_debug
    def __parse_lizard_results(self, lizard_results, code_type):
        """Parse lizard results.

        Parse lizard results and sort measurements on measure type and code type.

        :param lizard_results: dictionary representing the lizard output.
        :param code_type: string which generalizes the type of code found in source directories of provided results.

        :return: dictionary containing measurements, sorted on measure type and code type
        """
        parsed_result = {code_type: {"function": [], "file": []}}

        for item in self.__get_file_results_in_list(lizard_results["cppncss"]["measure"][0].get("item")):
            result = {
                "Name": item["@name"],
                "NR.": item["value"][0],
                "NCSS": item["value"][1],
                "CCN": item["value"][2],
            }
            parsed_result[code_type]["function"].append(result)

        for item in self.__get_file_results_in_list(lizard_results["cppncss"]["measure"][1].get("item")):
            result = {
                "Name": item["@name"],
                "NR.": item["value"][0],
                "NCSS": item["value"][1],
                "CCN": int(item["value"][2]) / int(item["value"][3]) if int(item["value"][3]) != 0 else 0,
                "Functions": item["value"][3],
            }
            parsed_result[code_type]["file"].append(result)

        if not parsed_result[code_type]["file"]:
            logger.warning(i18n.t("acidcli.no_code_files", code_type=code_type))
        return parsed_result

    @function_debug
    def __set_quality_gates(self, lizard_results, code_type):
        """Set quality gates.

        Update quality gates with the max CNN found in a single function,
        and update quality gates with the max CNN found in a single file.

        :param lizard_results: the results that will be scanned for the max CNN.
        :param code_type: string which generalizes the type of code found in in source directories of provided results.
        """
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            f"{code_type}MaxCCNFunction",
            self.__get_max_ccn_from_list(lizard_results, code_type, "function"),
            mandatory=True,
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            f"{code_type}AvgCCNFile",
            self.__get_max_ccn_from_list(lizard_results, code_type, "file"),
        )

    @staticmethod
    @function_debug
    def __get_max_ccn_from_list(lizard_results, code_type, measure):
        """Get max CNN from list.

        Scan the results and return the max CNN,
        where code type and measure are used as filters.

        :param code_type: sets which code type should be scanned.
        :param measure: sets which measure type should be scanned.

        :return: max CNN found
        """
        if len(lizard_results[code_type][measure]) == 0:
            return 0
        return int(max(int(item["CCN"]) for item in lizard_results[code_type][measure]))

    @function_debug
    def __write_readable_results_to_file(self, lizard_results, code_type):
        """Write readable results to file.

        Persist provided results to a file in a human-readable format.

        :param lizard_results: results that should be persisted in a readable format.
        :param code_type: string which generalizes the type of code found in in source directories of provided results.
        """
        filepath = join(self._parameter_value(self.__job, "output"), f"{code_type}_complexity.txt")

        with open(filepath, "w", encoding="utf-8") as output_file:
            output_file.write("Cyclomatic Complexity\n")
            output_file.write("Average Cyclomatic Complexity  file\n")
            output_file.write(f"{'Nr.':5} {'Filename':150} {'NCSS':6} {'CCN':5} {'Functions':5}\n")
            for item in lizard_results[code_type]["file"]:
                output_file.write(
                    f"{item['NR.'][:5]:5} "
                    f"{item['Name'][:150]:150} "
                    f"{item['NCSS']:6} "
                    f"{item['CCN']:.2f}  "
                    f"{item['Functions']:5}\n"
                )
            output_file.write("\n\n")
            output_file.write("Cyclomatic Complexity Per function\n")
            output_file.write(f"{'Nr.':5} {'Filename':150} {'NCSS':6} {'CCN':5}\n")
            for item in lizard_results[code_type]["function"]:
                output_file.write(f"{item['NR.'][:5]:5} {item['Name'][:150]:150} {item['NCSS']:6} {item['CCN']:5}\n")

    @function_debug
    def __collect_issues(self, lizard_results, code_type):
        """Collect issues.

        Collect the QualityGateErrors within the results in the issuereporter.

        :param lizard_results: Lizard complexity results.
        :param code_type: string which generalizes the type of code found in in source directories of provided results.
        """
        issues = []
        for item in lizard_results[code_type]["file"]:
            try:
                QualityGate.find_quality_gate(self.__job.qualitygates, f"{code_type}AvgCCNFile").compare(
                    comparison_value=int(item["CCN"])
                )
            except QualityGateError:
                issues.append(
                    {
                        "path": item["Name"],
                        "line_number": 1,
                        "message": f"violates {code_type}AvgCCNFile quality gate with: {int(item['CCN'])}",
                    }
                )
        for item in lizard_results[code_type]["function"]:
            try:
                QualityGate.find_quality_gate(self.__job.qualitygates, f"{code_type}MaxCCNFunction").compare(
                    comparison_value=int(item["CCN"])
                )
            except QualityGateError:
                re_search = re.search(r"at (.*):(\d*)", item["Name"])
                issues.append(
                    {
                        "path": re_search.group(1),
                        "line_number": int(re_search.group(2)),
                        "message": f"violates {code_type}MaxCCNFunction quality gate with: {int(item['CCN'])}",
                    }
                )
        self.__job.issues.append([code_type, issues])

    @staticmethod
    def __get_file_results_in_list(file_results):
        if isinstance(file_results, list):
            return file_results
        if file_results:
            return [file_results]
        return []


# pylint: enable=too-few-public-methods
