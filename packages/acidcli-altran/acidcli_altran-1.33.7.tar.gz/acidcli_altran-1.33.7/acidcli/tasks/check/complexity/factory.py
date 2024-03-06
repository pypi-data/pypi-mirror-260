# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for complexity
"""
from acidcli.tasks.check.complexity.lizard import Lizard
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckComplexity(TaskFactory):
    """Complexity factory."""

    def __init__(self):
        """Initialize code style for different languages."""
        super().__init__()
        self._creators = {
            "Independent": {"Lizard": Lizard},
        }


# pylint: enable=too-few-public-methods
