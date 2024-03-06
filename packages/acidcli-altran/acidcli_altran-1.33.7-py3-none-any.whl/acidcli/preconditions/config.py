# Copyright Capgemini Engineering B.V.

"""Configuration preconditions."""
from os import path

from loguru import logger

from acidcli.preconditions.exceptions import PreconditionError
from acidcli.preconditions.precondition import Precondition


class ConfigFileExists(Precondition):
    """Config file exists.

    Check existence of the config file pointed to by the config parameter.
    """

    def check(self, job):
        """Check."""
        logger.info("Check: config file exists")

        config_file = self._validate_parameter(job, "config")

        if not path.isfile(config_file):
            raise PreconditionError(
                f"Configuration file ('{config_file}') cannot be found.\n"
                f"Please check if the provided file location is correct, and the file exists."
            )

    def enforce(self, job):
        """Enforce."""
