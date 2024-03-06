# Copyright Capgemini Engineering B.V.

"""Secret detection.

Git secret detection using TruffleHog
"""
import os
import glob
from json import loads, dumps
from pathlib import Path
from copy import deepcopy

import i18n
from loguru import logger

from acidcli.exceptions import CLIError
from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess
from acidcli.quality_gate import QualityGate
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class TruffleHog(Executable):
    """TruffleHog."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check secrets.

        Get secrets for file structure or Git repository.
        File structure is default mode.

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["output", "scan_git_history"])

        scan_git_history = self._parameter_as_bool(self.__job, "scan_git_history")

        if scan_git_history is False:
            self.__run_trufflehog_on_file_tree()
            result = self.__redact_secrets("trufflehog_file_tree*")
        else:
            self.__run_trufflehog_on_git_history()
            result = self.__redact_secrets("trufflehog_git_history*")
        self.__collect_issues(result, scan_git_history)
        secret_counts = self.__count_results(result)
        self.__update_quality_gates(secret_counts)

    @function_debug
    def __run_trufflehog_on_file_tree(self):
        """Run trufflehog on file tree.

        Run TruffleHog on file tree.
        """
        trufflehog_command = ["trufflehog", "--no-update", "filesystem", "--directory", ".", "--json"]

        process = Subprocess(trufflehog_command, verbose=self._parameter_value(self.__job, "verbose"))
        process.execute_pipe(
            self._parameter_value(self.__job, "output"), "trufflehog_file_tree", check_return_code=False
        )

    @function_debug
    def __run_trufflehog_on_git_history(self):
        """Run trufflehog on git history.

        Run TruffleHog on git history.
        """
        logger.info(i18n.t("acidcli.secrets.git_history"))

        trufflehog_command = ["trufflehog", "--no-update", "git", "file://.", "--json"]

        process = Subprocess(trufflehog_command, verbose=self._parameter_value(self.__job, "verbose"))
        process.execute_pipe(
            self._parameter_value(self.__job, "output"), "trufflehog_git_history", check_return_code=False
        )

    @function_debug
    def __redact_secrets(self, file_name):
        """Redact secrets.

        Replaces secret values in TruffleHog log with empty values.

        When no TruffleHog log is found or multiple TruffleHog logs are found, CLIError
        will be thrown to prevent secret leakage.

        :param file_name: to replace secrets in
        :return: list with found secrets (with redacted values)
        """
        trufflehog_file_path = glob.glob(os.path.join(self._parameter_value(self.__job, "output"), file_name))
        exclude_list = self._parameter_value(self.__job, "exclude")
        scan_git_history = self._parameter_as_bool(self.__job, "scan_git_history")

        if len(trufflehog_file_path) == 0:
            raise CLIError(i18n.t("acidcli.secrets.no_log"))
        if len(trufflehog_file_path) > 1:
            raise CLIError(i18n.t("acidcli.secrets.multiple_logs"))

        trufflehog_secrets = []

        with open(trufflehog_file_path[0], "r", encoding="utf-8") as trufflehog_file:
            for line in trufflehog_file.readlines():
                line_content = loads(line)
                if "SourceMetadata" in line_content:
                    line_content["Raw"] = "[REDACTED]"  # Redact secret from TruffleHog result
                    line_content["RawV2"] = "[REDACTED]"  # Redact secret from TruffleHog result

                    trufflehog_secrets.append(line_content)
        if exclude_list:
            trufflehog_secrets = self.__exclude_path(trufflehog_secrets, exclude_list, scan_git_history)
        with open(trufflehog_file_path[0], "w", encoding="utf-8") as trufflehog_file:
            trufflehog_file.write(dumps(trufflehog_secrets, indent=4))

        return trufflehog_secrets

    @function_debug
    def __collect_issues(self, trufflehog_secrets, scan_git_history):
        """Collect issues.

        Collect issues from truffle hog output struct in issue reporter

        :param trufflehog_secrets: struct with detected secrets
        :param scan_git_history: scan git history enabled
        """
        issues = []
        for secret in trufflehog_secrets:
            directory_type = "Filesystem"
            if scan_git_history:
                directory_type = "Git"

            issue = {
                "path": secret["SourceMetadata"]["Data"][directory_type]["file"],
                "message": f"Secret found of type {secret['DetectorName']} with detector {secret['DecoderName']}",
            }

            if "line" in secret["SourceMetadata"]["Data"][directory_type]:
                issue["line_number"] = int(secret["SourceMetadata"]["Data"][directory_type]["line"])
            else:
                issue["line_number"] = 1

            issues.append(issue)
        self.__job.issues = [["combined", issues]]

    @function_debug
    def __count_results(self, trufflehog_secrets):
        """Count results.

        Count the number of detected secrets based on DetectorName

        :param trufflehog_secrets: struct with detected secrets
        :return: list with parsed secrets counts
        """
        secret_counts = []
        for secret in trufflehog_secrets:
            amount = len(
                [
                    value["DetectorName"]
                    for value in trufflehog_secrets
                    if value.get("DetectorName") == secret["DetectorName"]
                ]
            )

            found_match = False
            for secret_count in secret_counts:
                if secret_count["DetectorName"] == secret["DetectorName"]:
                    found_match = True
            if not found_match:
                secret_counts.append({"DetectorName": secret["DetectorName"], "count": amount})

        return secret_counts

    @function_debug
    def __update_quality_gates(self, secret_counts):
        """Update quality gates.

        Check configured quality gates

        Print a warning when gate setting for Detected Secrets > 0

        :param secret_counts: list of parsed secrets counts
        """
        for secret in secret_counts:
            detector_name = secret.get("DetectorName")
            if QualityGate.find_quality_gate(self.__job.qualitygates, f"{detector_name}DetectedSecrets"):
                if (
                    QualityGate.find_quality_gate_threshold(self.__job.qualitygates, f"{detector_name}DetectedSecrets")
                    > 0
                ):
                    logger.warning(
                        i18n.t("acidcli.secrets.gate_over_zero"), detectorname=f"{detector_name}DetectedSecrets"
                    )

            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates, f"{detector_name}DetectedSecrets", secret.get("count"), mandatory=True
            )

    @staticmethod
    @function_debug
    def __exclude_path(secrets, exclude_paths, git_scan):
        return_secrets = deepcopy(secrets)
        for secret in secrets:
            for exclude_path in exclude_paths:
                if git_scan:
                    file_path = Path(secret["SourceMetadata"]["Data"]["Git"]["file"])
                else:
                    file_path = Path(secret["SourceMetadata"]["Data"]["Filesystem"]["file"])
                if str(file_path).startswith(str(Path(exclude_path))):
                    return_secrets.remove(secret)
        return return_secrets

    # pylint: enable=too-few-public-methods
