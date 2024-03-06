# Copyright Capgemini Engineering B.V.

"""CICD postconditions.

----
Post conditions are used to validate the environment after a task completed
"""

# pylint: disable=too-few-public-methods
from acidcli.postconditions.exceptions import PostconditionError


class Postcondition:
    """Post condition interface."""

    def check(self, job):
        """Check."""
        raise NotImplementedError

    def _validate_parameter(self, job, input_parameter):
        """_validate_parameter with post condition error."""
        for parameter in job.parameters:
            if parameter.name == input_parameter:
                return parameter.value

        raise PostconditionError(
            f"Failed to run post condition: {self.__class__.__name__}. Missing parameter: {input_parameter}"
        )


# pylint: enable=too-few-public-methods
