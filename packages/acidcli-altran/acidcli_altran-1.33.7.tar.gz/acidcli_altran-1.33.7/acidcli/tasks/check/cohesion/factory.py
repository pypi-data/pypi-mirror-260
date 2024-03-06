# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for code cohesion
"""
from acidcli.tasks.check.cohesion.cohesion import Cohesion
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckCohesion(TaskFactory):
    """Cohesion factory."""

    def __init__(self):
        """Initialize cohesion check for different languages."""
        super().__init__()
        self._creators = {
            "Python": Cohesion,
        }


# pylint: enable=too-few-public-methods
