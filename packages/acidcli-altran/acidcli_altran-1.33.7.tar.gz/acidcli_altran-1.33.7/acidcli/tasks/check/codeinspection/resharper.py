# Copyright Capgemini Engineering B.V.

#
"""Resharper code inspection.

Code inspection using resharper inspectcode
"""
import os
from collections import defaultdict

from xmltodict import parse as parse_xml

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Resharper(Executable):
    """Resharper."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check resharper rules.

        :param job: job model object with job configuration
        """
        self.__job = job
        self.__job.issues = []
        self._required_parameters_available(self.__job, ["config", "input", "output"])

        resharper_results = self._read_resharper_results(self.__run_inspectcode())

        total_issues_per_severity_level = self._determine_issues_per_severity_level(resharper_results)
        sorted_issues = self.__sort_issues_on_code_location(total_issues_per_severity_level)
        for code_location, issues_per_severity_level in sorted_issues.items():
            self.__collect_issues(issues_per_severity_level, code_location)
            self._set_qualitygates(issues_per_severity_level, code_location)

    @function_debug
    def __run_inspectcode(self):
        """Run resharper.

        :return: location of output file.
        """
        output_file = os.path.join(self._parameter_value(self.__job, "output"), "code_inspection_results.xml")
        code_inspection = [
            "inspectcode",
            self._parameter_value(self.__job, "input"),
            f"--profile={self._parameter_value(self.__job, 'config')}",
            f"--output={output_file}",
            "--no-build",
        ]

        process = Subprocess(code_inspection, verbose=self._parameter_value(self.__job, "verbose"))
        process.execute_pipe(self._parameter_value(self.__job, "output"), "inspectcode", check_return_code=False)

        return output_file

    @function_debug
    def _set_qualitygates(self, issues_per_severity_level, code_location):
        """_set_qualitygates.

        Update Quality Gates

        :param issues_per_severity_level: Dict with findings
        :param code_location: code location to set the quality gates for
        """
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, f"{code_location}InspectionHints", len(issues_per_severity_level["HINT"])
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            f"{code_location}InspectionSuggestions",
            len(issues_per_severity_level["SUGGESTION"]),
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            f"{code_location}InspectionWarnings",
            len(issues_per_severity_level["WARNING"]),
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates,
            f"{code_location}InspectionErrors",
            len(issues_per_severity_level["ERROR"]),
            mandatory=True,
        )

    @staticmethod
    @function_debug
    def _read_resharper_results(filename):
        """Read the Resharper issues into a dictionary.

        :param filename: Resharper xml output

        :return: Resharper results dictionary
        """
        with open(filename, encoding="utf-8") as input_file:
            doc = parse_xml(input_file.read())

        return doc

    @staticmethod
    @function_debug
    def _determine_issue_types(resharper_results):
        """Get a list of issue types.

        :return: list
        """
        try:
            issue_types = resharper_results["Report"]["IssueTypes"]["IssueType"]
            if not isinstance(issue_types, list):
                return [issue_types]
            return issue_types
        except TypeError:
            return []

    @staticmethod
    @function_debug
    def _determine_projects(resharper_results):
        """Get the list of projects.

        :rtype: list
        """
        try:
            projects = resharper_results["Report"]["Issues"]["Project"]
            if not isinstance(projects, list):
                return [projects]
            return projects
        except TypeError:
            return []

    @staticmethod
    @function_debug
    def _determine_issues(project):
        """Get the list of issues of a project.

        :return: list
        """
        try:
            issues = project["Issue"]
            if not isinstance(issues, list):
                return [issues]
            return issues
        except KeyError:
            return []

    @staticmethod
    @function_debug
    def _determine_issue_severity(issue_id, issue_types):
        """Determine the severity of an issue."""
        severity = None

        for issue in issue_types:
            issue_type_id = issue["@Id"]
            if issue_type_id == issue_id:
                severity = issue["@Severity"]
                break

        return severity

    @function_debug
    def _determine_issues_per_severity_level(self, resharper_results):
        """Determine the issues for each severity level.

        :param resharper_results: dict with resharper results.
        """
        issues_per_severity_level = defaultdict(list)
        issue_types = self._determine_issue_types(resharper_results)

        projects = self._determine_projects(resharper_results)
        for project in projects:
            issues = self._determine_issues(project)
            for issue in issues:
                issue_severity = self._determine_issue_severity(issue["@TypeId"], issue_types)
                issues_per_severity_level[issue_severity].append(
                    {
                        "file": issue["@File"],
                        "line": issue["@Line"] if "@Line" in issue else 1,
                        "message": issue["@Message"],
                    }
                )

        return issues_per_severity_level

    @function_debug
    def __sort_issues_on_code_location(self, total_issues_per_severity_level):
        """Sort issues on code location.

        :param total_issues_per_severity_level: dict with issues per severity level.
        """
        sorted_issues = {location.name: defaultdict(list) for location in self.__job.parent.parent.code_locations}

        for severity, issues in total_issues_per_severity_level.items():
            for issue in issues:
                for code_location in self.__job.parent.parent.code_locations:
                    for directory in code_location.directories:
                        common_path = os.path.commonpath([issue["file"], directory])
                        if common_path and os.path.samefile(common_path, directory):
                            sorted_issues[code_location.name][severity].append(issue)

        return sorted_issues

    @function_debug
    def __collect_issues(self, issues_per_severity_level, code_location):
        """Collect issues.

        Collect errors in issuereporter.

        :param issues_per_severity_level: dict with issuer per severity level.
        :param code_location: code type to set the quality gates for
        """
        reported_issues = []
        for severity, issues in issues_per_severity_level.items():
            for issue in issues:
                reported_issues.append(
                    {
                        "path": issue["file"],
                        "line_number": int(issue["line"]),
                        "message": f"[{severity}] {issue['message']}",
                    }
                )
        self.__job.issues.append([code_location, reported_issues])


# pylint: enable=too-few-public-methods
