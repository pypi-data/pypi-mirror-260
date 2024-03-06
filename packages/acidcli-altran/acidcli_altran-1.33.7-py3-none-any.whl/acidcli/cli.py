# Copyright Capgemini Engineering B.V.

"""Command Line Interface.

Command line interface for acid tooling
"""
import argparse
import sys

from acidcli import __version__ as acidcli_version


class DerivedArgumentParser(argparse.ArgumentParser):
    """Override of standard ArgumentParser."""

    def error(self, message):
        """Override of error message function for ArgumentParser."""
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        sys.exit(2)


class KeyValueAction(argparse.Action):
    """Custom implementation of Argparse Action."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Return key=value parameters."""
        setattr(namespace, self.dest, {})

        for value in values:
            # split it into key and value
            try:
                key, value = value.split("=")
            except ValueError:
                parser.error(f"Parameter without KEY=VALUE found: {value}")
            if value == "":
                parser.error(f"KEY with empty VALUE found: {key}")
            # assign into dictionary
            getattr(namespace, self.dest)[key] = value


# pylint: disable=too-few-public-methods
class CLI:
    """Main Command Line Interface parser."""

    def __init__(self, pipeline_model):
        """Initialize CLI."""
        parser = DerivedArgumentParser(description="CICD Command Line Interface for %(prog)s")

        parser.add_argument(
            "--version",
            action="version",
            version=f"{parser.prog} {acidcli_version}",
        )

        parser.add_argument(
            "--verbose",
            "-v",
            action="count",
            default=0,
            help="verbose mode (-vv for more, -vvv to enable full verbosity)",
        )

        parent_parser = argparse.ArgumentParser(add_help=False)

        parent_parser.add_argument(
            "--parameter",
            metavar="KEY=VALUE",
            nargs="+",
            action=KeyValueAction,
            help="Set a number of key-value pairs "
            "(do not put spaces before or after the = sign). "
            "If a value contains spaces, you should define "
            "it with double quotes: "
            'input_directory="this is a sentence". Note that '
            "values are always treated as strings.",
            default={},
        )

        subparsers = parser.add_subparsers(title="pipeline stages", dest="stage", required=True)

        for stage in pipeline_model.stages:
            subparser = subparsers.add_parser(stage.name, help=f"available {stage.name} commands")
            subsubparsers = subparser.add_subparsers(title=f"{stage.name} tasks", dest="job")

            for job in stage.jobs:
                subsubparsers.add_parser(job.name, parents=[parent_parser], help=f"{stage.name} {job.name}")

        self.parser = parser


# pylint: enable=too-few-public-methods
