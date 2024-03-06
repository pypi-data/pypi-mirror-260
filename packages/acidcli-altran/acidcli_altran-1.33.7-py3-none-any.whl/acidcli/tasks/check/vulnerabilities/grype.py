# Copyright Capgemini Engineering B.V.

"""Docker vulnerability checker.

Vulnerability checker for Docker Images
"""
import os
from collections import defaultdict
from json import dumps, loads
from os import environ

import i18n
from loguru import logger

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable
from acidcli.quality_gate import QualityGate
from acidcli.exceptions import CLIError

_CONFIG_DIR = "/config"


# pylint: disable=too-few-public-methods
class Grype(Executable):
    """Grype."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check vulnerabilities.

        Check vulnerabilities for Docker with Grype.

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["output"])

        self.__set_environment_variables()
        self.__prepare_json_config()
        raw_grype_output = self.__run_grype()
        structured_grype_output = self.__process_grype_output(raw_grype_output)
        self.__print_readable_grype_results(structured_grype_output)
        self.__update_quality_gates(structured_grype_output)

    @staticmethod
    @function_debug
    def __set_environment_variables():
        """Set required environment variables."""
        environ["DOCKER_CONFIG"] = _CONFIG_DIR

    @staticmethod
    @function_debug
    def __prepare_json_config():
        """Generate docker config file."""
        try:
            docker_config = {
                "auths": {
                    environ["CI_REGISTRY"]: {
                        "username": environ["CI_REGISTRY_USER"],
                        "password": environ["CI_REGISTRY_PASSWORD"],
                    }
                }
            }
        except KeyError as error:
            raise CLIError(i18n.t("acidcli.pipeline.environment_variable_missing", message=str(error))) from error
        os.makedirs(_CONFIG_DIR, exist_ok=True)
        with open(_CONFIG_DIR + "/config.json", "w+", encoding="utf-8") as file:
            file.write(dumps(docker_config))

    @function_debug
    def __run_grype(self):
        """Run Grype.

        Runs Grype tooling on specific image.

        :return: dict containing unstructured Grype output.
        """
        version = self._parameter_value(self.__job, "version")
        input_container = f"{self.__job.parent.parent.container_registry}/pipeline:{version.get_pipeline_id()}"
        grype_command = [
            "grype",
            "--add-cpes-if-none",
            input_container,
            "-o",
            "json",
            "--file",
            os.path.join(self._parameter_value(self.__job, "output"), "grype_output.json"),
        ]

        process = Subprocess(grype_command, verbose=self._parameter_value(self.__job, "verbose"))
        process.execute_pipe(
            self._parameter_value(self.__job, "output"),
            "grype",
        )

        with open(
            os.path.join(self._parameter_value(self.__job, "output"), "grype_output.json"), "r", encoding="utf-8"
        ) as grype_output:
            return loads(grype_output.read())

    @staticmethod
    @function_debug
    def __process_grype_output(raw_grype_output):
        """Process grype output.

        :param raw_grype_output: dict containing raw Grype output.
        :return: dict containing structured Grype output.
        """
        result = defaultdict(lambda: defaultdict(list))
        for match in raw_grype_output["matches"]:
            vulnerability_id = match["vulnerability"]["id"]
            link = match["vulnerability"]["dataSource"]
            severity = match["vulnerability"]["severity"]
            tool = match["artifact"]["name"]
            version = match["artifact"]["version"]
            state = match["vulnerability"]["fix"]["state"]
            fix_versions = match["vulnerability"]["fix"]["versions"] if state == "fixed" else None

            result[state][severity].append(
                {
                    "id": vulnerability_id,
                    "link": link,
                    "tool": tool,
                    "version": version,
                    "fix_versions": fix_versions,
                }
            )

        return result

    @staticmethod
    @function_debug
    def __print_readable_grype_results(structured_grype_output):
        """Print readable Grype results.

        :param structured_grype_output: dict containing structured Grype output.
        """
        for state, vulnerabilities_per_state in structured_grype_output.items():
            if state == "fixed":
                logger.error(i18n.t("acidcli.vulnerability.fixable_issues_header"))
            else:
                logger.error(i18n.t("acidcli.vulnerability.non_fixable_issues_header", state=state))
            for severity, vulnerabilities_per_severity in vulnerabilities_per_state.items():
                for vulnerability in vulnerabilities_per_severity:
                    if state == "fixed":
                        message = i18n.t(
                            "acidcli.vulnerability.fixable_issue",
                            severity=severity,
                            id=vulnerability["id"],
                            tool=vulnerability["tool"],
                            version=vulnerability["version"],
                            link=vulnerability["link"],
                            fixes=vulnerability["fix_versions"],
                        )
                    else:
                        message = i18n.t(
                            "acidcli.vulnerability.non_fixable_issue",
                            severity=severity,
                            id=vulnerability["id"],
                            tool=vulnerability["tool"],
                            version=vulnerability["version"],
                            link=vulnerability["link"],
                        )
                    logger.error(message)

    @function_debug
    def __update_quality_gates(self, structured_grype_output):
        """Update quality gates.

        :param structured_grype_output: dict containing structured Grype output.
        """
        fixable_issues = {
            "Critical": 0,
            "High": 0,
            "Medium": 0,
            "Low": 0,
            "Negligible": 0,
            "Unknown": 0,
        }
        non_fixable_issues = {
            "Critical": 0,
            "High": 0,
            "Medium": 0,
            "Low": 0,
            "Negligible": 0,
            "Unknown": 0,
        }
        for state, vulnerabilities_per_state in structured_grype_output.items():
            for severity, vulnerabilities_per_severity in vulnerabilities_per_state.items():
                if state == "fixed":
                    fixable_issues[severity] += len(vulnerabilities_per_severity)
                else:
                    non_fixable_issues[severity] += len(vulnerabilities_per_severity)
        for severity, count in fixable_issues.items():
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates, f"Fixable{severity}", count, mandatory=(severity == "Critical")
            )
        for severity, count in non_fixable_issues.items():
            QualityGate.find_and_update_quality_gate(
                self.__job.qualitygates, f"NonFixable{severity}", count, mandatory=(severity == "Critical")
            )


# pylint: enable=too-few-public-methods
