# Copyright Capgemini Engineering B.V.

"""Npm precondition."""
import os

from loguru import logger

from acidcli.facility.subprocess import ProcessError
from acidcli.facility.subprocess import Subprocess
from acidcli.preconditions.exceptions import PreconditionError
from acidcli.preconditions.precondition import Precondition


class NpmPackagesInstalled(Precondition):
    """Npm Install Packages.

    Make sure package dependencies required for the project are installed.
    """

    def enforce(self, job):
        """Enforce."""
        logger.info("Enforce: npm install")

        restore_command = ["npm", "install"]

        with open(
            os.path.join(self._validate_parameter(job, "output"), "npm_install.log"), "w", encoding="utf-8"
        ) as npm_install_output_file:
            try:
                process = Subprocess(
                    restore_command,
                    stdout=npm_install_output_file,
                    stderr=npm_install_output_file,
                    verbose=self._validate_parameter(job, "verbose"),
                )
                process.execute()
            except ProcessError as error:
                raise PreconditionError(error) from error

        logger.info("Finished: npm install")
