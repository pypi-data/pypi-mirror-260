# Copyright Capgemini Engineering B.V.

"""Job.

Handling job flow
"""
import os
from json import dumps
from os.path import join

import i18n
from loguru import logger

import acidcli.postconditions
import acidcli.preconditions
import acidcli.tasks
from acidcli.configuration import ConfigurationFile
from acidcli.exceptions import CLIError
from acidcli.facility import Upload
from acidcli.facility.subprocess import SubprocessRuntimeError, ProcessError
from acidcli.quality_gate import QualityGateError
from acidcli.postconditions import PostconditionError
from acidcli.preconditions import PreconditionError
from acidcli import __version__ as acidcli_version


class Job:
    """Job."""

    def __init__(self, job_model):
        """Build job behaviour."""
        self.job_model = job_model
        self.job_config = None

    @staticmethod
    def get_function_attribute(function_location, function_name):
        """Wrap getattr interface."""
        function_attribute = None
        for function in dir(function_location):
            if function.lower() == function_name.lower():
                function_attribute = getattr(function_location, function)()

        if function_attribute is None:
            raise AttributeError(function_name)

        return function_attribute

    def enforce_preconditions(self):
        """Enforce preconditions."""
        logger.info(i18n.t("acidcli.precondition.info"))

        for precondition in self.job_model.preconditions:
            try:
                precondition = self.get_function_attribute(acidcli.preconditions, precondition)
                precondition.check(self.job_model)
                precondition.enforce(self.job_model)
            except PreconditionError as exception:
                raise CLIError(
                    i18n.t(
                        "acidcli.precondition.error", precondition=precondition.__class__.__name__, message=exception
                    )
                ) from exception

    def execute_task(self, language, platform):
        """Execute task."""
        logger.info("Execute task")

        project_config = ConfigurationFile.parse_project_config(self.job_model.parent.parent)
        self.job_config = ConfigurationFile().parse_job_config(self.job_model)

        task = self.__get_factory_implementation(language, platform)

        try:
            task.execute(self.job_model)
        except ProcessError as exception:
            raise CLIError(exception) from exception
        except SubprocessRuntimeError as exception:
            raise CLIError(exception) from exception
        except QualityGateError as exception:
            raise CLIError(exception) from exception
        except TypeError:
            try:
                task.execute(project_config, self.job_config)
            except QualityGateError as exception:
                raise CLIError(exception) from exception

    def __get_factory_implementation(self, language, platform):
        try:
            language = language or self.job_model.parent.parent.language
            task_factory = self.get_function_attribute(acidcli.tasks, self.job_model.parent.name + self.job_model.name)
            return task_factory.get_executable(language, platform)
        except TypeError as exception:
            raise CLIError(
                i18n.t("acidcli.job.with_language_requires_use_of_platform", job=self.job_model.name)
            ) from exception
        except ValueError as exception:
            raise CLIError(
                i18n.t("acidcli.job.with_invalid_language", job=self.job_model.name, exception=exception)
            ) from exception
        except CLIError as exception:
            raise CLIError(
                i18n.t("acidcli.job.does_not_support_use_of_platform", job=self.job_model.name, exception=exception)
            ) from exception
        except AttributeError as exception:
            raise CLIError(
                i18n.t("acidcli.acidcli_yaml_invalid_job", job=self.job_model.name, stage=self.job_model.parent.name)
            ) from exception

    def check_postconditions(self):
        """Enforce preconditions."""
        logger.info(i18n.t("acidcli.postcondition.info"))

        for postcondition in self.job_model.postconditions:
            try:
                postcondition = self.get_function_attribute(acidcli.postconditions, postcondition)
                postcondition.check(self.job_model)
            except PostconditionError as exception:
                raise CLIError(
                    i18n.t(
                        "acidcli.postcondition.error",
                        postcondition=postcondition.__class__.__name__,
                        message=exception,
                    )
                ) from exception

    def check_quality_gates(self):
        """Check quality gates."""
        logger.info("Check quality gates:")

        failed_gates = []

        for quality_gate in self.job_model.qualitygates:
            try:
                quality_gate.compare(logging_enabled=True)
            except QualityGateError as outer_exception:
                if "Comparison value is not set for metric" in str(outer_exception):
                    if self.job_config is None:
                        self.job_config = ConfigurationFile().parse_job_config(self.job_model)

                    for quality_gate1 in self.job_config.quality_gates:
                        try:
                            quality_gate1.compare(logging_enabled=True)
                        except QualityGateError as inner_exception:
                            logger.critical(
                                i18n.t("acidcli.quality_gate.job_gate_failed", failed_gate=inner_exception)
                            )
                            failed_gates.append(quality_gate1)
                else:
                    logger.critical(i18n.t("acidcli.quality_gate.job_gate_failed", failed_gate=outer_exception))
                    failed_gates.append(quality_gate)

        if failed_gates:
            raise QualityGateError(i18n.t("acidcli.quality_gate.job_error", failed_gates=len(failed_gates)))

    def upload_quality_gates(self):
        """Upload Quality Gates."""
        if self.job_model.parent.parent.skip_quality_gate_upload:
            logger.info(i18n.t("acidcli.upload.quality_gates.skipped_by_configuration"))
            return
        for parameter in self.job_model.parameters:
            if parameter.name == "version" and not parameter.value.is_pipeline():
                logger.info(i18n.t("acidcli.upload.quality_gates.skipped_by_pipeline"))
                return

        if os.environ.get("ACIDMETRICS_API_URL") and os.environ.get("TECHNICAL_API_KEY"):
            self.upload_quality_gates_to_acidmetrics()
            return

    def upload_quality_gates_to_acidmetrics(self):
        """Upload quality gates to acidmetrics."""
        try:
            url = f"{os.environ['ACIDMETRICS_API_URL']}/metrics/qualitygates/"
        except KeyError as error:
            raise CLIError(
                i18n.t("acidcli.environment_variable_not_found", env_variable="ACIDMETRICS_API_URL")
            ) from error

        try:
            bearer_token = os.environ["TECHNICAL_API_KEY"]
        except KeyError as error:
            raise CLIError(
                i18n.t("acidcli.environment_variable_not_found", env_variable="TECHNICAL_API_KEY")
            ) from error

        for quality_gate in self.job_model.qualitygates:
            json_payload = self.__get_quality_gate_json_payload(quality_gate)
            self.__save_json_payload_to_file(json_payload)

            Upload(bearer_token=bearer_token).upload_json(
                url,
                self.__get_quality_gate_json_payload(quality_gate),
            )

        logger.info(i18n.t("acidcli.upload.quality_gates.upload_successful"))

    @staticmethod
    def __get_quality_gate_json_payload(quality_gate):
        """Get Quality Gate json payload."""
        json_payload = {
            "tenant": os.environ["TECHNICAL_TENANT"],
            "project_name": os.environ["CI_PROJECT_NAME"],
            "project_id": int(os.environ["CI_PROJECT_ID"]),
            "ref": os.environ["CI_COMMIT_REF_NAME"],
            "commit_sha": os.environ["CI_COMMIT_SHA"],
            "commit_timestamp": os.environ["CI_COMMIT_TIMESTAMP"],
            "pipeline_id": int(os.environ["CI_PIPELINE_ID"]),
            "stage": os.environ["CI_JOB_STAGE"],
            "job_name": os.environ["CI_JOB_NAME"],
            "job_id": int(os.environ["CI_JOB_ID"]),
            "metric": quality_gate.metric,
            "operator": quality_gate.operator,
            "threshold": quality_gate.threshold,
            "value": quality_gate.input_value,
            "is_percentage": quality_gate.is_percentage,
            "acidcli_version": acidcli_version,
        }
        return json_payload

    def __save_json_payload_to_file(self, json_payload):
        """Save json payload to file."""
        filepath = ""
        for parameter in self.job_model.parameters:
            if parameter.name == "output":
                if "metric" in json_payload:
                    filepath = join(parameter.value, f"quality_gate_metrics_{json_payload['metric']}.json")
                else:
                    filepath = join(parameter.value, "quality_gate_metrics.json")
        try:
            with open(filepath, "w", encoding="utf-8") as output_file:
                output_file.write(dumps(json_payload))
        except FileNotFoundError as error:
            raise CLIError(error) from error
