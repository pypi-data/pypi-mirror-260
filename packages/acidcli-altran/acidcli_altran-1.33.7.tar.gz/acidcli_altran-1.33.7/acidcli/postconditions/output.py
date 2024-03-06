# Copyright Capgemini Engineering B.V.

"""postconditions.

All collection of all postconditions
"""
import os

from acidcli.postconditions.exceptions import PostconditionError
from acidcli.postconditions.postcondition import Postcondition


# pylint: disable=too-few-public-methods
class OutputDirectoryIsNotEmpty(Postcondition):
    """Output is not empty?.

    Check if the output directory contains data.
    """

    def check(self, job):
        """Enforce."""
        folder = self._validate_parameter(job, "output")

        if not list(f for f in os.listdir(folder)):
            raise PostconditionError("Directory is empty")


# pylint: enable=too-few-public-methods
