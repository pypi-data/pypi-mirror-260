# Copyright Capgemini Engineering B.V.

"""Cohesion checker.

Python cohesion checker
"""
from collections import defaultdict

from loguru import logger

from acidcli.facility import Subprocess
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate, QualityGateError
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Cohesion(Executable):
    """Python cohesion checker."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check cohesion.

        Check cohesion for python with cohesion.

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["output"])

        results_per_code_type = {}

        for code_type in self.__job.parent.parent.code_locations:
            results = {"meetsQualityGate": [], "failsQualityGate": []}
            for directory in code_type.directories:
                cohesion_output = self.__run_cohesion(directory)
                parsed_cohesion_output = self.__parse_cohesion_output(code_type.name, cohesion_output)
                results["meetsQualityGate"].extend(parsed_cohesion_output["meetsQualityGate"])
                results["failsQualityGate"].extend(parsed_cohesion_output["failsQualityGate"])
            results_per_code_type[code_type.name] = results

        self.__print_cohesion_table(results_per_code_type)
        average_per_code_type = self.__calculate_average_cohesion(results_per_code_type)
        self.__update_quality_gates(results_per_code_type, average_per_code_type)

    @function_debug
    def __run_cohesion(self, directory):
        """Run cohesion.

        Run cohesion command as subprocess for provided files.

        :param directory: directory to be scanned.
        :return: decoded cohesion output.
        """
        cohesion_command = [
            "cohesion",
            "--directory",
            directory,
        ]

        process = Subprocess(cohesion_command, verbose=self._parameter_value(self.__job, "verbose"))
        cohesion_output = process.execute_pipe(
            self._parameter_value(self.__job, "output"), "cohesion", check_return_code=False
        )
        return cohesion_output.stdout.decode("utf-8")

    @function_debug
    def __parse_cohesion_output(self, code_type, cohesion_output):
        """Parse cohesion output.

        Parse cohesion output, extracting the cohesion for each class.

        :param code_type: type of code which is currently checked.
        :param cohesion_output: decoded cohesion output.
        :return: cohesion per class, split on code_type and quality gate conformity.
        """
        quality_gate = QualityGate.find_quality_gate(
            self.__job.qualitygates, f"{code_type}MinimalClassCohesionPercentage"
        )
        results = defaultdict(list)
        current_result = {}
        for line in cohesion_output.splitlines():
            line = line.strip()
            if line.startswith("File:"):
                current_result["file"] = line[6:]
            elif line.startswith("Class:"):
                end = line.find("(") - 1
                current_result["class"] = line[7:end]
                start = line.find("(") + 1
                end = line[7:].find(":") + 7
                current_result["line"] = line[start:end]
            elif line.startswith("Total:"):
                cohesion = float(line[7:][:-1])
                current_result["cohesion"] = cohesion
                try:
                    quality_gate.compare(cohesion)
                    results["meetsQualityGate"].append(current_result.copy())
                except QualityGateError:
                    results["failsQualityGate"].append(current_result.copy())
        return results

    @staticmethod
    @function_debug
    def __print_cohesion_table(results_per_code_type):
        """Print cohesion table.

        Print cohesion summaries table to the terminal.

        :param results_per_code_type: class cohesion results, split on code type.
        """
        file_column_width = 0
        class_column_width = 0
        cohesion_column_width = 8
        for results in results_per_code_type.values():
            for result in results["failsQualityGate"]:
                file_column_width = max(file_column_width, len(result["file"]) + len(result["line"]) + 2)
                class_column_width = max(class_column_width, len(result["class"]))
        table_width = file_column_width + class_column_width + cohesion_column_width

        logger.info(
            f"{'File':<{file_column_width}}{'class':<{class_column_width}}{'cohesion':>{cohesion_column_width}}"
        )

        for code_type, results in results_per_code_type.items():
            print_code_type = f"      {code_type}      "
            logger.info(f"{print_code_type:-^{table_width}}")
            for result in results["failsQualityGate"]:
                location = f"{result['file']}:{result['line']}"
                cohesion = f"{result['cohesion']}%"
                logger.info(
                    f"{location:<{file_column_width}}"
                    f"{result['class']:<{class_column_width}}"
                    f"{cohesion:>{cohesion_column_width}}"
                )

        logger.info(f"{'':-^{table_width}}")

    @staticmethod
    @function_debug
    def __calculate_average_cohesion(results_per_code_type):
        """Calculate average cohesion.

        Calculate the average cohesion per code type.

        :param results_per_code_type: class cohesion results, split on code type.
        :return: average cohesion, split on code type.
        """
        average_per_code_type = {}
        for code_type, results in results_per_code_type.items():
            cumulative_cohesion = 0
            for result in results["meetsQualityGate"]:
                cumulative_cohesion += result["cohesion"]
            for result in results["failsQualityGate"]:
                cumulative_cohesion += result["cohesion"]
            class_count = len(results["meetsQualityGate"]) + len(results["failsQualityGate"])
            average_per_code_type[code_type] = cumulative_cohesion / class_count if class_count else 0
        return average_per_code_type

    @function_debug
    def __update_quality_gates(self, results_per_code_type, average_per_code_type):
        """Update quality gates.

        Update quality gates with corresponding input values.

        :param results_per_code_type: class cohesion results, split on code type.
        :param average_per_code_type: average cohesion, split on code type.
        """
        for code_type, average_cohesion in average_per_code_type.items():
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates,
                f"{code_type}AverageCohesionPercentage",
                average_cohesion,
                is_percentage=True,
            )
        for code_type, results in results_per_code_type.items():
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates, f"{code_type}MinimalClassCohesionPercentage", 100, is_percentage=True
            )
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates,
                f"{code_type}CohesionViolations",
                len(results["failsQualityGate"]),
            )


# pylint: enable=too-few-public-methods
