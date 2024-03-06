# Copyright Capgemini Engineering B.V.

"""Input preconditions."""
import os

from loguru import logger

from acidcli.preconditions.exceptions import PreconditionError
from acidcli.preconditions.precondition import Precondition


class InputFileExists(Precondition):
    """Input file exists.

    Check existence of the input file pointed to by the input parameter.
    """

    def check(self, job):
        """Check."""
        logger.info("Check: input file exists")

        input_file = self._validate_parameter(job, "input")

        if not os.path.isfile(input_file):
            raise PreconditionError(
                f"Input file ('{input_file}') cannot be found.\n"
                f"Please check if the provided file location is correct, and the file exists."
            )

    def enforce(self, job):
        """Enforce."""


class InputDirectoryIsNotEmpty(Precondition):
    """Input directory is not empty.

    Check if the input directory contains data.
    """

    def check(self, job):
        """Enforce."""
        folder = self._validate_parameter(job, "input")

        if not list(f for f in os.listdir(folder)):
            raise PreconditionError("Directory is empty")

    def enforce(self, job):
        """Enforce."""
