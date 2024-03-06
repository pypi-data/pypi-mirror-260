# Copyright Capgemini Engineering B.V.

"""ACID Command Line Interface."""
import os
import sys
from types import SimpleNamespace

from pyfiglet import figlet_format
import i18n
from loguru import logger
from textx import metamodel_from_file
from textx.exceptions import TextXSyntaxError

from acidcli.cli import CLI
from acidcli.exceptions import CLIError, VersionError
from acidcli.quality_gate import QualityGateError, QualityGate
from acidcli.job import Job
from acidcli.configuration import ConfigurationFile
from acidcli.environment import EnvironmentLoader
from acidcli import __version__ as acidcli_version
from acidcli.facility.issue_reporter import IssueReporter

i18n.load_path.append(os.path.join(os.path.dirname(__file__), "locale"))

logger.remove()
logger.add(
    "acidcli.log", rotation="daily", retention="1 week", filter=lambda record: "not_to_file" not in record["extra"]
)


def __print_error(error):
    """Print error messages."""
    for line in str(error).split("\n"):
        logger.error(line)


def __parse_acidcli_model():
    """Parse acidcli model."""
    try:
        acid_model = metamodel_from_file(
            os.path.join(os.path.dirname(__file__), "metamodel", "acid.tx"),
            auto_init_attributes=False,
            classes=[QualityGate],
        )
        pipeline_model = acid_model.model_from_file(".acidcli.yml")
    except FileNotFoundError as error:
        __print_error(i18n.t("acidcli.acidcli_yaml_not_found", filename=error.filename))
        pipeline_model = SimpleNamespace(stages=[])
    except TextXSyntaxError as error:
        __print_error(i18n.t("acidcli.acidcli_yaml_invalid_format", error=error))
        pipeline_model = SimpleNamespace(stages=[])

    return pipeline_model


def __compare_and_push_issues(job_model):
    for parameter in job_model.parameters:
        if parameter.name == "version" and not parameter.value.is_pipeline():
            logger.info(i18n.t("acidcli.issue.skipped_by_pipeline"))
            return

    if os.environ.get("ENABLE_ISSUE_DIFF") == "false":
        logger.warning(i18n.t("acidcli.issue.skipped_by_ff"))
        return

    if os.environ.get("ACIDMETRICS_API_URL") and os.environ.get("TECHNICAL_API_KEY"):
        stripped_issues = IssueReporter.strip_code_locations(job_model.issues)
        previous_run = IssueReporter.pull_issues()
        IssueReporter.print_old_pipeline_warning(previous_run)

        try:
            previous_issues = previous_run["issues"]
        except TypeError:
            previous_issues = []

        new_issues, removed_issues, unchanged_issue = IssueReporter.compare_issues(previous_issues, stripped_issues)
        IssueReporter.print_differences(new_issues, removed_issues, unchanged_issue)
        IssueReporter.push_issues(stripped_issues)


def __run_job(job_model, parameters):
    """Run a certain job."""
    job_model.parameters.append(SimpleNamespace(name="verbose", value=parameters["verbose"]))
    job_model.parameters.append(SimpleNamespace(name="version", value=parameters["version"]))
    job_model.parameters.append(SimpleNamespace(name="environment", value=parameters["environment"]))
    job_model.issues = None
    if job_model.language is None:
        job_model.language = job_model.parent.parent.language

    for parameter in parameters:
        for model_parameter in job_model.parameters:
            if model_parameter.name == parameter:
                if isinstance(model_parameter.value, list):
                    model_parameter.value = ConfigurationFile.parse_string_to_list(parameters[parameter])
                else:
                    model_parameter.value = parameters[parameter]
                break
        else:
            raise CLIError(i18n.t("acidcli.parameter.unkown", parameter=parameter))

    job = Job(job_model)

    job.enforce_preconditions()
    job.execute_task(job_model.language, job_model.platform)

    if job_model.issues is not None:
        IssueReporter.print_clickable_links(job_model.issues)
        __compare_and_push_issues(job_model)

    job.check_postconditions()

    if job_model.qualitygates:
        job.upload_quality_gates()
        job.check_quality_gates()
    else:
        logger.info(i18n.t("acidcli.quality_gate.no_gates_found"))


def __run_stage(stage, config, parameters):
    for job in stage.jobs:
        if (job.name == config.job) or ((config.job is None) and (job.autorun is not False)):
            logger.info(
                i18n.t(
                    "acidcli.terminal_divider.with_name",
                    name=f"{job.name:^20}",
                )
            )
            __run_job(job, parameters)
            logger.info(i18n.t("acidcli.terminal_divider.without_name"))


def _override_verbosity(config_verbose):
    """Override CLI verbose with Environment Variable set by Zebra.

    :param config_verbose: Verbose parameter from the Argparser
    :type config_verbose: int
    :return: Verbosity value
    :rtype: int
    """
    try:
        verbosity_str = os.environ["ZEBRA_VERBOSITY"]
        verbosity = int(verbosity_str)
    except KeyError:
        verbosity = config_verbose
    except ValueError as error:
        raise CLIError(
            i18n.t(
                "acidcli.environment_variable_not_int",
                env_variable="ZEBRA_VERBOSITY",
                env_variable_content=verbosity_str,
            )
        ) from error
    return verbosity


def main():
    """Entry of the acidcli."""
    info_logger = logger.add(sys.stdout, colorize=True, format="<level>{level: <8} - {message}</level>", level="INFO")

    logger.bind(not_to_file=True).opt(raw=True).info(figlet_format("acidcli", font="starwars"))
    logger.info(i18n.t("acidcli.versioning.acidcli_version", version=acidcli_version))

    try:
        pipeline_model = __parse_acidcli_model()

        cli = CLI(pipeline_model)
        config = cli.parser.parse_args(sys.argv[1:])

        verbosity = _override_verbosity(config.verbose)

        if verbosity > 0:
            logger.remove(info_logger)
            logger.add(sys.stdout, colorize=True, format="<level>{level: <8} - {message}</level>", level="DEBUG")

        try:
            parameters = config.parameter
        except AttributeError:
            parameters = {}
        parameters["verbose"] = verbosity

        environment = EnvironmentLoader(pipeline_model)

        parameters["version"] = environment.version
        parameters["environment"] = environment.environment

        for stage in pipeline_model.stages:
            if stage.name == config.stage:
                __run_stage(stage, config, parameters)
    except CLIError as error:
        __print_error(error)
        sys.exit(1)
    except VersionError as error:
        __print_error(error)
        sys.exit(1)
    except QualityGateError as error:
        __print_error(error)
        sys.exit(2)


if __name__ == "__main__":
    main()
