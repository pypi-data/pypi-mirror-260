# Copyright Capgemini Engineering B.V..

"""Issue reporter.

Job issues reporting functionality
"""
import os
from copy import deepcopy
from difflib import SequenceMatcher

from loguru import logger

import i18n

from acidcli.facility.upload import Upload

from acidcli.exceptions import CLIError

from acidcli import __version__ as acidcli_version


# pylint: disable=too-few-public-methods


class IssueReporter:
    """IssueReporter."""

    __MATCH_PERCENTAGE = 90  # Minimum percentage an issue should match with another issue
    # before it is considered the same issue.

    @staticmethod
    def pull_issues():
        """
        Pull issues.

        Pull issues from API endpoint.

        :return: lists of found issues
        """
        try:
            params = {
                "ref": os.environ["CI_DEFAULT_BRANCH"],
                "project_id": int(os.environ["CI_PROJECT_ID"]),
                "job_name": os.environ["CI_JOB_NAME"],
                "stage": os.environ["CI_JOB_STAGE"],
                "pipeline_id": int(os.environ["CI_PIPELINE_ID"]),
            }
        except KeyError as error:
            raise CLIError(
                i18n.t("acidcli.environment_variable_not_found", env_variable="CI_DEFAULT_BRANCH or CI_PROJECT_ID")
            ) from error

        upload = Upload(bearer_token=IssueReporter.__get_bearer_token())
        issues = upload.download_json(IssueReporter.__get_endpoint_url(), params)

        logger.debug(
            i18n.t("acidcli.issue.pulling_issues", issues_length=len(issues)),
        )

        return issues

    @staticmethod
    def push_issues(issues):
        """Push issues.

        Push issues to API endpoint.

        :param issues: list of issues to push
        """
        logger.debug(
            i18n.t("acidcli.issue.pushing_issues", issues_length=len(issues)),
        )

        payload = {
            "project_id": int(os.environ["CI_PROJECT_ID"]),
            "project_name": os.environ["CI_PROJECT_NAME"],
            "tenant": os.environ["TECHNICAL_TENANT"],
            "commit_sha": os.environ["CI_COMMIT_SHA"],
            "commit_timestamp": os.environ["CI_COMMIT_TIMESTAMP"],
            "ref": os.environ["CI_COMMIT_REF_NAME"],
            "pipeline_id": int(os.environ["CI_PIPELINE_ID"]),
            "job_id": int(os.environ["CI_JOB_ID"]),
            "job_name": os.environ["CI_JOB_NAME"],
            "stage": os.environ["CI_JOB_STAGE"],
            "acidcli_version": acidcli_version,
            "issues": issues,
        }

        upload = Upload(bearer_token=IssueReporter.__get_bearer_token())
        upload.upload_json(IssueReporter.__get_endpoint_url(), payload)

    @staticmethod
    def print_old_pipeline_warning(issues_with_metadata):
        """Print old pipeline warning.

        Print a warning if the current pipeline ID is lower than the pipeline ID returned by the issue collector.

        :param issues_with_metadata: issues and metadata.
        """
        pipeline_id = int(os.environ.get("CI_PIPELINE_ID"))
        try:
            if pipeline_id < issues_with_metadata["pipeline_id"]:
                logger.warning(i18n.t("acidcli.issue.newer_pipeline"))
        except TypeError:
            logger.debug(i18n.t("acidcli.issue.no_previous_uploads"))

    @staticmethod
    def print_clickable_links(issues):
        """Print clickable links.

        Print issues in a clickable form.

        :param issues: issues to print.
        """
        for location in issues:
            logger.info(f"Found issues in code location: {location[0]}")
            if len(location[1]) == 0:
                logger.info("No issues found")
            for issue in location[1]:
                message = i18n.t(
                    "acidcli.clickable_path.file",
                    path=issue["path"],
                    line_number=issue["line_number"],
                    error_message=issue["message"],
                )
                logger.warning(message)

    @staticmethod
    def strip_code_locations(issues):
        """Strip code locations.

        Strip the code locations from the issues.

        :param issues: issues to be stripped.
        :return: issues stripped from their code locations.
        """
        stripped_issues = []
        for location in issues:
            stripped_issues.extend(location[1])
        return stripped_issues

    @staticmethod
    def compare_issues(previous_run, current_run):
        """Compare issues.

        Detects and returns differences and similarities in issues between two different runs.

        First checks which issues are identical (fast).
        Secondly uses ratio matching to check remaining issues (slower).

        Ratio checking first calculates all the ratios and only then picks the issue with the best matching ratio.

        Sorted by path, line_number and then message.

        :param previous_run: list of issues in previous job run
        :param current_run: list of issues in current job run
        :return: lists of: new_issues, removed_issues, unchanged_issues
        """
        current_run_copy = deepcopy(current_run)
        previous_run_copy = deepcopy(previous_run)

        logger.debug(
            i18n.t(
                "acidcli.issue.comparing_issues",
                previous_run_length=len(previous_run_copy),
                current_run_length=len(current_run_copy),
            ),
        )

        # Fast way of getting exactly matching issues
        sorted_matching_issues = IssueReporter.__get_exact_matching_issues(previous_run_copy, current_run_copy)

        # Excluding exactly matched issues from probability matching
        current_run_copy = IssueReporter.__delete_matching_issues(current_run_copy, sorted_matching_issues)
        previous_run_copy = IssueReporter.__delete_matching_issues(previous_run_copy, sorted_matching_issues)

        # Probability match left over issues
        new_issues, removed_issues, unchanged_issues = IssueReporter.__get_ratio_matched_issues(
            previous_run_copy, current_run_copy
        )

        # Add exact matching issues to unchanged issues list
        unchanged_issues.extend(sorted_matching_issues)

        # Sort issue arrays
        sorted_new_issues = sorted(new_issues, key=lambda k: (k["path"], k["line_number"], k["message"]))
        sorted_removed_issues = sorted(removed_issues, key=lambda k: (k["path"], k["line_number"], k["message"]))
        sorted_unchanged_issues = sorted(unchanged_issues, key=lambda k: (k["path"], k["line_number"], k["message"]))

        logger.debug(
            i18n.t(
                "acidcli.issue.issue_status",
                new_issues_length=len(sorted_new_issues),
                removed_issue_length=len(sorted_removed_issues),
                unchanged_issues_length=len(sorted_unchanged_issues),
            ),
        )
        return sorted_new_issues, sorted_removed_issues, sorted_unchanged_issues

    @staticmethod
    def __get_exact_matching_issues(previous_run, current_run):
        """Get exact matching issues.

        Returns issues that are exactly the same over both run.

        Duplicates inside a run ar handled as unique issues.

        :param previous_run: list of issues in previous job run
        :param current_run: list of issues in current job run
        :return: list with exactly matching issue
        """
        unique_matching_issues = []

        current_run_copy = deepcopy(current_run)
        previous_run_copy = deepcopy(previous_run)

        longest_list = current_run_copy if len(current_run_copy) >= len(previous_run_copy) else previous_run_copy
        shortest_list = previous_run_copy if len(current_run_copy) >= len(previous_run_copy) else current_run_copy

        while len(longest_list) > 0:
            issue = longest_list[0]
            if len(shortest_list) == 0:
                break

            match = False
            for id_inner, issue_compare in enumerate(shortest_list):
                if issue == issue_compare:
                    unique_matching_issues.append(issue)
                    longest_list.pop(0)
                    shortest_list.pop(id_inner)
                    match = True
                    break

            # No match for result in longest list, pop to prevent endless looping
            if not match:
                longest_list.pop(0)

        logger.debug(
            i18n.t(
                "acidcli.issue.exact_matching_issues",
                issues_length=len(unique_matching_issues),
            ),
        )

        return unique_matching_issues

    @staticmethod
    def __get_ratio_matched_issues(previous_run, current_run):
        """Get ratio matched issue.

        Ratio checking first calculates all the ratios and only then picks the issue with the best matching ratio.

        When no ratios left to compare or no ratios under given threshold, ratio comparing stops.
        All leftover issues from previous run are removed issues.
        All leftover issues from current run are new issues.

        :param previous_run: list of issues in previous job run
        :param current_run: list of issues in current job run
        :return: lists of: new_issues, removed_issues, unchanged_issues
        """
        new_issues = []
        removed_issues = []
        unchanged_issues = []

        while True:
            total_set = []

            for previous_issue in previous_run:
                for current_issue in current_run:
                    previous_interpolated = (
                        f"{previous_issue['path']} {previous_issue['line_number']} {previous_issue['message']}"
                    )
                    current_interpolated = (
                        f"{current_issue['path']} {current_issue['line_number']} {current_issue['message']}"
                    )
                    total_set.append(
                        {
                            "previous_issue": previous_issue,
                            "current_issue": current_issue,
                            "ratio": SequenceMatcher(a=previous_interpolated, b=current_interpolated).ratio(),
                        }
                    )

            sorted_result = sorted(total_set, key=lambda entry: entry["ratio"], reverse=True)

            if sorted_result:
                if sorted_result[0]["ratio"] >= IssueReporter.__MATCH_PERCENTAGE / 100:
                    unchanged_issues.append(sorted_result[0]["current_issue"])
                    current_run.remove(sorted_result[0]["current_issue"])
                    previous_run.remove(sorted_result[0]["previous_issue"])

                    continue

            if previous_run:
                removed_issues.extend(previous_run)
            if current_run:
                new_issues.extend(current_run)
            break

        return new_issues, removed_issues, unchanged_issues

    @staticmethod
    def __delete_matching_issues(list_1, list_2):
        """Delete matching issues.

        Deletes issues from both list where issues occurs in both lists.

        Duplicates in a single list are allowed and are counted as separate issues.

        :param list_1: list of issues
        :param list_2: list of issues
        :return: list_1 of: list_1 where all matching issues with list_2 are deleted
        """
        list_1_copy = deepcopy(list_1)
        list_2_copy = deepcopy(list_2)

        longest_list = list_1_copy if len(list_1_copy) >= len(list_2_copy) else list_2_copy
        shortest_list = list_2_copy if len(list_1_copy) >= len(list_2_copy) else list_1_copy

        # index is used to delete element in longest_list
        index = 0
        while len(longest_list) > index:
            issue_longest_list = longest_list[index]
            if len(shortest_list) == 0:
                break

            match = False
            for id_inner, issue_shortest_list in enumerate(shortest_list):
                if issue_longest_list == issue_shortest_list:
                    longest_list.pop(index)
                    shortest_list.pop(id_inner)

                    match = True
                    break

                break

            if not match:
                # if no matching issue in shortest_list then increase index
                index = index + 1

        return list_1_copy

    @staticmethod
    def print_differences(new_issues, removed_issues, unchanged_issues):
        """Print differences.

        Prints amount of removed, unchanged and new issues.

        If new issues present, print warning and each new issue as a warning message.
        If removed issues present, print each removed issue as as a info message.

        :param new_issues: newly found issues
        :param removed_issues: removed issues
        :param unchanged_issues: unchanged issues
        """
        logger.info(i18n.t("acidcli.issue.amount_removed_issues", removed_issues_length=len(removed_issues)))
        logger.info(i18n.t("acidcli.issue.amount_unchanged_issues", unchanged_issues_length=len(unchanged_issues)))
        logger.info(i18n.t("acidcli.issue.amount_new_issues", new_issues_length=len(new_issues)))

        if removed_issues:
            logger.info(i18n.t("acidcli.issue.removed_issues"))
            for issue in removed_issues:
                logger.info(
                    i18n.t(
                        "acidcli.clickable_path.file",
                        path=issue["path"],
                        line_number=issue["line_number"],
                        error_message=issue["message"],
                    )
                )

        if new_issues:
            logger.warning(i18n.t("acidcli.issue.new_issues"))
            for issue in new_issues:
                logger.warning(
                    i18n.t(
                        "acidcli.clickable_path.file",
                        path=issue["path"],
                        line_number=issue["line_number"],
                        error_message=issue["message"],
                    )
                )

    @staticmethod
    def __get_bearer_token():
        """Get bearer token.

        Get the bearer token from the `TECHNICAL_API_KEY` env var.
        Raises CLIError when bearer token not found.

        :return: bearer token
        """
        try:
            bearer_token = os.environ["TECHNICAL_API_KEY"]
            return bearer_token
        except KeyError as error:
            raise CLIError(
                i18n.t("acidcli.environment_variable_not_found", env_variable="TECHNICAL_API_KEY")
            ) from error

    @staticmethod
    def __get_endpoint_url():
        """Get endpoint url.

        Get the issue API endpoint url.
        Raises CLIError when ACIDMETRICS_API_URL env var not found.

        :return: endpoint url
        """
        try:
            url = f"{os.environ['ACIDMETRICS_API_URL']}/issues/issuecollection/"
            return url
        except KeyError as error:
            raise CLIError(
                i18n.t("acidcli.environment_variable_not_found", env_variable="ACIDMETRICS_API_URL")
            ) from error


# pylint: disable=too-few-public-methods
