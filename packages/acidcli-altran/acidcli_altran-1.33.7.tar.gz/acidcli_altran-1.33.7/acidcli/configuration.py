# Copyright Capgemini Engineering B.V.

"""Acidcli configuration data.

Data class with acidcli configurations
"""
from dataclasses import dataclass

import i18n

from acidcli.exceptions import CLIError


@dataclass
class ProjectConfig:
    """Project configuration dataclass."""

    name: str
    language: str
    code_location: {}

    artifact_repository_url: str
    sonarqube_url: str
    skip_quality_gate_upload: bool
    sonarqube_project_key: str = None


@dataclass
class JobConfig:
    """Job configuration dataclass."""

    stage: str
    job: str
    preconditions: []
    task: []
    postconditions: []
    quality_gates: []
    parameters: {}


class ConfigurationFile:
    """Configuration file."""

    @staticmethod
    def parse_project_config(pipeline_model):
        """Read project configuration from yaml."""
        locations = {}
        for code_location in pipeline_model.code_locations:
            locations[code_location.name] = code_location.directories

        return ProjectConfig(
            pipeline_model.project,
            pipeline_model.language,
            locations,
            pipeline_model.artifact_repository_url,
            pipeline_model.sonarqube_url,
            pipeline_model.skip_quality_gate_upload,
            pipeline_model.sonarqube_project_key,
        )

    @staticmethod
    def parse_string_to_list(list_as_string):
        """Parse string in to list.

        :param list_as_string: List in string format.
        :return: parsed list.
        """
        if list_as_string == "[]":
            return []
        if list_as_string[0] != "[" or list_as_string[-1] != "]":
            raise CLIError(i18n.t("acidcli.list_expected", received=list_as_string))
        result = list_as_string[1:-1].split(",")
        result = [item.strip('"') for item in result]
        return result

    def parse_job_config(self, job_model):
        """Read job configuration from yaml."""
        self.__check_for_duplicate_quality_gate_metrics(job_model.qualitygates)

        model_parameters = {}
        for model_parameter in job_model.parameters:
            model_parameters[model_parameter.name] = model_parameter.value

        return JobConfig(
            job_model.parent.name,
            job_model.name,
            job_model.preconditions,
            None,
            job_model.postconditions,
            job_model.qualitygates,
            model_parameters,
        )

    @staticmethod
    def __check_for_duplicate_quality_gate_metrics(quality_gates):
        """Check quality gates list for duplicate metrics."""
        metrics = []
        for quality_gate in quality_gates:
            if quality_gate.metric not in metrics:
                metrics.append(quality_gate.metric)
            else:
                raise CLIError(
                    f"Duplicated metric.\nMetric: '{quality_gate.metric}' configured multiple times in .acidcli.yml"
                )
