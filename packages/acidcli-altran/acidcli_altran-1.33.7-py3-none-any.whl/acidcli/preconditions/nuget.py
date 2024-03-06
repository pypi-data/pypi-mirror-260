# Copyright Capgemini Engineering B.V.

"""Nuget preconditions."""
from loguru import logger

import i18n

from acidcli.facility.subprocess import ProcessError
from acidcli.facility.subprocess import Subprocess
from acidcli.preconditions.exceptions import PreconditionError
from acidcli.preconditions.precondition import Precondition


class NugetPackagesRestored(Precondition):
    """Nuget Restore Packages.

    Make sure package dependencies required for the solution to build are restored.
    """

    def enforce(self, job):
        """Enforce.

        :param job: job model object with job configuration
        """
        logger.info("Enforce: nuget restore")

        restore_command = ["nuget", "restore", "-NonInteractive", self._validate_parameter(job, "input")]

        try:
            process = Subprocess(restore_command, verbose=self._validate_parameter(job, "verbose"))
            process.execute_pipe(None, None, disable_logfile=True)
        except ProcessError as error:
            errors = self.__parse_command_output_error(error.command_output)
            raise PreconditionError(i18n.t("acidcli.build_csharp_error", errors=errors)) from error
        logger.info("Finished: Nuget restore")

    @staticmethod
    def __parse_command_output_error(stdout):
        """Parse command output error.

        Parses the output error from nuget restore.
        Because the errors are returned multiple times, a dict is used to remove the duplicates.

        :param: stdout: stdout to search.
        :return: String with found errors.
        """
        duplicated_found_errors = []
        stdout_lines = stdout.splitlines()

        for line in stdout_lines:
            if "Unable to find" in line:
                duplicated_found_errors.append(line.strip())

        found_errors = list(dict.fromkeys(duplicated_found_errors))
        return "\n".join(found_errors)
