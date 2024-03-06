# Copyright Capgemini Engineering B.V.

"""CICD Preconditions.

----
Preconditions are used to prepare the environment for a task.
"""
from acidcli.preconditions.exceptions import PreconditionError


# pylint: disable=too-few-public-methods
class Precondition:
    """Precondition interface."""

    def check(self, job):
        """Check."""

    def enforce(self, job):
        """Enforce."""
        raise NotImplementedError

    def _validate_parameter(self, job, input_parameter):
        """_validate_parameter with precondition error."""
        for parameter in job.parameters:
            if parameter.name == input_parameter:
                return parameter.value

        raise PreconditionError(
            f"Failed to run precondition: {self.__class__.__name__}. Missing parameter: {input_parameter}"
        )


# pylint: enable=too-few-public-methods
