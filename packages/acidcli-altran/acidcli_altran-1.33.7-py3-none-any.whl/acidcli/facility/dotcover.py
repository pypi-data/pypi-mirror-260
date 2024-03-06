# Copyright Capgemini Engineering B.V..

"""DotCover.

Dotcover commands
"""
import glob
import re
import os
import pathlib

import i18n
import xmltodict

from acidcli.exceptions import CLIError
from acidcli.facility.subprocess import Subprocess


class DotCover:
    """DotCover."""

    @staticmethod
    def __find_test_dlls(directory, build_type, matching_pattern):
        """Find test dlls.

        Find all test dll's in the given directory.

        Matches:
        - ending in '.dll'
        - matching matching_pattern (e.g. '.*[uU]nit[tT]est', '.*[iI]ntegration[tT]est')
        - containing the build_type (i.e. 'debug' or 'release')
        - does not contain directory 'obj' (temporary object files)

        :param code_locations: locations to search
        :param build_type: current build type to search trough
        :param matching_pattern: RegEx pattern to use for searching
        :return: list of collected files
        """
        dll_list = glob.glob(os.path.join(directory, "**", "*.dll"), recursive=True)
        regex = re.compile(matching_pattern)

        files = [
            file
            for file in list(filter(regex.match, dll_list))
            if file.lower().__contains__(os.path.join(build_type, ""))
            and not file.lower().__contains__(os.path.join("obj", ""))
        ]
        return files

    @staticmethod
    def collect_test_files(code_locations, build_type, matching_pattern):
        """Collect test files.

        Find all test dll's in given input.

        :param code_locations: locations to search
        :param build_type: current build type to search trough
        :param matching_pattern: pattern to use for searching

        :return: list of collected files
        """
        files = []

        for location_entry in code_locations:
            files += DotCover.__find_test_dlls(location_entry, build_type, matching_pattern)

        if not files:
            raise CLIError(
                i18n.t(
                    "acidcli.test_units.no_dlls_found",
                    build_type=build_type,
                    directories=code_locations,
                )
            )

        return files

    @staticmethod
    def run_tests(files, config_file, output_directory, filename, verbose, test_runner_args=None):
        """Run tests.

        Run the tests defined in all the dll files.

        :param files: Test DLL's
        :param config_file: DotCover config file to use
        :param output_directory: directory for test output
        :param filename: dcvr name
        :param verbose: verbosity
        :param test_runner_args: DotCover target args
        """
        target_args = f"""{'"'}{'" "'.join(files)}{'"'}"""
        result_filename = f"{filename}.dcvr"

        if test_runner_args is not None:
            target_args += f" {test_runner_args}"

        dotcover_command = [
            "dotcover",
            "cover",
            config_file,
            f"/Output={os.path.join(output_directory, result_filename)}",
            f"/TargetWorkingDir={output_directory}",
            f"/TargetArguments={target_args}",
        ]

        process = Subprocess(dotcover_command, verbose=verbose)
        process.execute_pipe(output_directory, "dotcover_execute", check_return_code=False)

    @staticmethod
    def create_report(output_directory, report_format, report_extension, input_filename, output_filename, verbose):
        """Create report.

        Convert dotcover results to a report file in xml, html or json format.

        :param output_directory: output folder
        :param report_format: Format of
        :param report_extension: File type extension of
        :param input_filename: dcvr input file
        :param output_filename: output of
        :param verbose: verbosity
        """
        source_filename = f"{input_filename}.dcvr"

        report_command = [
            "dotcover",
            "report",
            f"/Source={os.path.join(output_directory, source_filename)}",
            f"""/Output={os.path.join(output_directory, f"{output_filename}.{report_extension}")}""",
            f"/ReportType={report_format}",
        ]

        process = Subprocess(report_command, verbose=verbose)
        process.execute_pipe(
            output_directory,
            "dotcover_report",
        )

    @staticmethod
    def create_cobertura_report(output_directory, input_filename, verbose):
        """create_cobertura_report.

        Create a Cobertura report from a DetailedXML report.

        :param output_directory: Output directory to find input file
        :param input_filename: Input DetailedXML file
        :param verbose: verbosity
        """
        report_generator_command = [
            "reportgenerator",
            f'"-reports:{output_directory}/{input_filename}.xml"',
            f'"-targetdir:{output_directory}"',
            '"-reporttypes:Cobertura"',
        ]
        process = Subprocess(report_generator_command, verbose=verbose)
        process.execute_pipe(
            output_directory,
            "reportgenerator_report",
        )

        with open(f"{output_directory}/Cobertura.xml", "r", encoding="utf-8") as file:
            original_data = file.read()

            converted_data = xmltodict.parse(original_data, force_list=("package", "class", "method"))
            try:
                for package in converted_data["coverage"]["packages"]["package"]:
                    for class_obj in package["classes"]["class"]:
                        class_obj["@filename"] = (
                            class_obj["@filename"].replace(f"{str(pathlib.Path().resolve())}\\", "").replace("\\", "/")
                        )
            except KeyError as error:
                raise CLIError(
                    i18n.t(
                        "acidcli.dotcover_unexpected_format_detailed_xml",
                        rerport_path=f"{output_directory}/{input_filename}",
                    )
                ) from error

            xml_data = xmltodict.unparse(converted_data, pretty=True)

        with open(f"{output_directory}/Cobertura.xml", "w", encoding="utf-8") as file:
            file.write(xml_data)
