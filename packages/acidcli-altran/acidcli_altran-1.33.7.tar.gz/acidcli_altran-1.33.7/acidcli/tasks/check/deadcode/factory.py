# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for deadcode
"""
from acidcli.tasks.check.deadcode.vulture import Vulture
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckDeadcode(TaskFactory):
    """Deadcode factory."""

    def __init__(self):
        """Initialize deadcode for different languages."""
        super().__init__()
        self._creators = {
            "Python": Vulture,
        }


# pylint: enable=too-few-public-methods
