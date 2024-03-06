# Copyright Capgemini Engineering B.V..

"""Coverage.

Generic abstraction for working with coverage.
"""
from os.path import join, isfile

import i18n
from loguru import logger
from xmltodict import parse as parse_xml

from acidcli.exceptions import CLIError
from acidcli.facility import Subprocess, ProcessError


class Coverage:
    """Coverage."""

    @classmethod
    def run_module(cls, module_command, output_directory, verbose=0, config=None, check_return_code=True):
        """Run module through coverage.

        Run given module using coverage run to measure coverage.

        :param module_command: Command to execute module.
        :param output_directory: Location to persist output files.
        :param verbose: Optional verbosity for executing command.
        :param config: Optional config to include in command.
        :returns: Command execution object.
        """
        arguments = ["--branch", "-m"]
        arguments.extend(module_command)
        return cls.__execute_coverage_command(
            "run", arguments, output_directory, verbose=verbose, config=config, check_return_code=check_return_code
        )

    @classmethod
    def export_html_report(cls, output_directory, verbose=0, config=None):
        """Export HTML coverage report.

        Export HTML coverage report to specified output directory.

        :param output_directory: Location to persist output files.
        :param verbose: Optional verbosity for executing command.
        :param config: Optional config to include in command.
        :returns: Output from ran command.
        """
        arguments = ["-d", "{}".format(join(output_directory, "coverage_html"))]
        try:
            return cls.__execute_coverage_command(
                "html", arguments, output_directory, verbose=verbose, config=config
            ).stdout
        except ProcessError as e:
            raise CLIError("Generating coverage html report failed. Run coverage before generating reports.") from e

    @classmethod
    def export_xml_report(cls, output_directory, verbose=0, config=None):
        """Export XML coverage report.

        Export XML coverage report to specified output directory.

        :param output_directory: Location to persist output files.
        :param verbose: Optional verbosity for executing command.
        :param config: Optional config to include in command.
        :returns: Output from ran command.
        """
        arguments = ["-o", "{}".format(join(output_directory, "coverage.xml"))]
        try:
            return cls.__execute_coverage_command(
                "xml", arguments, output_directory, verbose=verbose, config=config
            ).stdout
        except ProcessError as e:
            raise CLIError("Generating coverage xml report failed. Run coverage before generating reports.") from e

    @classmethod
    def combine(cls, output_directory, verbose=0, config=None):
        """Combine.

        Combine coverage data into a single data file.

        :param output_directory: Location to persist output files.
        :param verbose: Optional verbosity for executing command.
        :param config: Optional config to include in command.
        :returns: Output from ran command.
        """
        try:
            return cls.__execute_coverage_command(
                "combine", [], output_directory, verbose=verbose, config=config
            ).stdout
        except ProcessError as e:
            raise CLIError("Combining coverage data failed. Only combine data after running in parallel mode.") from e

    @staticmethod
    def __execute_coverage_command(
        command, arguments, output_directory, verbose=0, config=None, check_return_code=True
    ):
        """Run coverage command.

        Run coverage command with additional arguments.

        :param command: The coverage command to run.
        :param arguments: Arguments to add to coverage command.
        :param output_directory: Location to persist log files.
        :param verbose: Optional verbosity for executing command.
        :param config: Optional config to include in command.
        :returns: Command execution object.
        """
        coverage_command = ["coverage", command]
        if config:
            coverage_command.append("--rcfile={}".format(config))
        coverage_command.extend(arguments)
        process = Subprocess(coverage_command, verbose=verbose)
        return process.execute_pipe(output_directory, "coverage_xml", check_return_code=check_return_code)

    def read_coverage_xml_results(self, output_directory):
        """Read coverage results.

        Load coverage results from exported XML file and convert into dictionary.

        :param output_directory: Location to persist log files.
        :returns: Dictionary containing coverage results.
        """
        file_path = join(output_directory, "coverage.xml")
        if not isfile(file_path):
            raise CLIError("Coverage xml report not found at {}.".format(file_path))
        with open(file_path) as input_file:
            coverage_result = self.read_coverage_xml_results_string(input_file.read())
        return coverage_result

    @staticmethod
    def read_coverage_xml_results_string(data):
        """Read coverage results.

        Load coverage results from exported XML file and convert into dictionary.

        :param data: decoded coverage xml file.
        :returns: Dictionary containing coverage results.
        """
        coverage_result = parse_xml(data, dict_constructor=dict)
        return coverage_result

    @classmethod
    def print_coverage_results(cls, coverage_results, path_prefix=None):
        """Print coverage results.

        Print coverage results in a table with clickable links.

        :param coverage_results: coverage results containing info about each tested file.
        :param path_prefix: Path to prepend to file path in cobertura report
        """
        skipped_files = 0
        files_to_print = []
        folders = coverage_results["coverage"]["packages"]["package"]
        if not isinstance(folders, list):
            folders = [folders]
        for folder in folders:
            files = folder["classes"]["class"]
            if not isinstance(files, list):
                files = [files]
            for file in files:
                if file["@line-rate"] == "1" and file["@branch-rate"] == "1":
                    skipped_files += 1
                else:
                    files_to_print.append(cls.__prepare_file_for_printing(file, path_prefix))

        cls.__print_coverage_table(
            files_to_print,
            skipped_files,
            float(coverage_results["coverage"]["@line-rate"]),
            float(coverage_results["coverage"]["@branch-rate"]),
        )

    @classmethod
    def __prepare_file_for_printing(cls, file, path_prefix=None):
        """Prepare file for printing.

        Parse given file and return it in a printable format.

        :param file: file as loaded from the exported xml.
        :param path_prefix: Path to prepend to file path in cobertura report
        :returns: printable file as tuple, containing "filepath", "line_coverage", "branch_coverage", and "missing".
        """
        missing_streaks = cls.__get_missing_lines(file)
        missing_coverage = []
        for missing in missing_streaks:
            missing_coverage.append("".join(missing))
        if path_prefix:
            file["@filename"] = path_prefix + file["@filename"]
        file_to_print = {
            "filepath": "{}:{}".format(file["@filename"], missing_streaks[0][0]),
            "line_coverage": float(file["@line-rate"]),
            "branch_coverage": float(file["@branch-rate"]),
            "missing": " ".join(filter(None, missing_coverage)),
        }
        return file_to_print

    @classmethod
    def __get_missing_lines(cls, file):
        """Get missing lines.

        Parse file and return lines that are not completely covered

        :param file: file as loaded from the exported xml.
        """
        current_streak = []
        missing_streaks = []
        lines = file["lines"]["line"]
        if not isinstance(lines, list):
            lines = [lines]
        for line in lines:
            if line["@hits"] == "0":
                if current_streak:
                    current_streak[1] = "-"
                    current_streak[2] = line["@number"]
                else:
                    current_streak = [line["@number"], "", ""]
            else:
                if current_streak:
                    missing_streaks.append(current_streak)
                    current_streak = []
                branch_coverage = cls.__get_branch_coverage(line)
                if branch_coverage:
                    missing_streaks.append(branch_coverage)

        missing_streaks.append(current_streak)
        return missing_streaks

    @staticmethod
    def __get_branch_coverage(line):
        """Get branch coverage.

        Get branch coverage for line.

        :param: Line as loaded from the exported xml.
        :returns: if uncovered, List containing uncovered line(s), else None
        """
        if "@condition-coverage" in line:
            if "100%" not in line["@condition-coverage"]:
                return [line["@number"], "", ""]
        elif "@missing-branches" in line:
            missing_branches = filter(None, line.get("@missing-branches", "").split(","))
            for branch in missing_branches:
                return [line["@number"], "->", branch]
        return None

    @staticmethod
    def __print_coverage_table(files_to_print, skipped_files, average_line_coverage, average_branch_coverage):
        """Print coverage table.

        Print a coverage table to the terminal.

        :param files_to_print: list of printable files, as returned by __prepare_file_for_printing.
        :param skipped_files: amount of files skipped due to complete coverage.
        :param average_line_coverage: percentage of total lines covered.
        :param average_branch_coverage: percentage of total branches covered.
        """
        if files_to_print:
            filepath_width = max(len(x["filepath"]) for x in files_to_print)
            logger.info(
                "{:{width}}{:>7}{:>7}   {}".format("Filename", "Line", "Branch", "Missing", width=filepath_width)
            )
            logger.info(i18n.t("acidcli.terminal_divider.without_name"))

            for file in files_to_print:
                logger.info(
                    "{:{width}}{:>7.0%}{:>7.0%}   {}".format(
                        file["filepath"],
                        file["line_coverage"],
                        file["branch_coverage"],
                        file["missing"],
                        width=filepath_width,
                    )
                )

            logger.info(i18n.t("acidcli.terminal_divider.without_name"))
            logger.info(
                "{:{width}}{:>7.0%}{:>7.0%}".format(
                    "Total:", average_line_coverage, average_branch_coverage, width=filepath_width
                )
            )

        logger.info(
            "{} file{} skipped due to complete coverage.".format(skipped_files, "" if skipped_files == 1 else "s")
        )

    @staticmethod
    def calculate_coverage_percentages(coverage_results):
        """Calculate coverage percentages.

        Calculate coverage percentage based on metrics read from the coverage results.

        :param coverage_results: dictionary containing parsed coverage results.
        :returns: dictionary containing coverage per line, per branch, and total average.
        """
        lines_covered = float(coverage_results["coverage"]["@lines-covered"])
        branches_covered = float(coverage_results["coverage"]["@branches-covered"])
        lines_valid = float(coverage_results["coverage"]["@lines-valid"])
        branches_valid = float(coverage_results["coverage"]["@branches-valid"])

        total_covered = lines_covered + branches_covered
        total_valid = lines_valid + branches_valid

        if total_valid == 0:
            total_percentage = 0
        else:
            total_percentage = float(format(round(total_covered / total_valid * 100, 2), "2f"))

        if lines_valid == 0:
            line_percentage = 0
        else:
            line_percentage = float(format(round(lines_covered / lines_valid * 100, 2), "2f"))

        if branches_valid == 0:
            branch_percentage = 0
        else:
            branch_percentage = float(format(round(branches_covered / branches_valid * 100, 2), "2f"))

        return {"line": line_percentage, "branch": branch_percentage, "total": total_percentage}
