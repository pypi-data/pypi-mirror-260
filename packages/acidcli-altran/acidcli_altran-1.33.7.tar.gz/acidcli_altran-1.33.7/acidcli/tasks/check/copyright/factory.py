# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for code linting
"""
from acidcli.tasks.check.copyright.copyright import Copyright
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckCopyright(TaskFactory):
    """Copyright factory."""

    def __init__(self):
        """Initialize copyright check for different languages."""
        super().__init__()
        self._creators = {
            "Independent": Copyright,
        }


# pylint: enable=too-few-public-methods
