# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for Format
"""
from acidcli.tasks.check.format.black import Black
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckFormat(TaskFactory):
    """CheckFormat factory."""

    def __init__(self):
        """Initialize CheckFormat."""
        super().__init__()
        self._creators = {
            "Python": Black,
        }


# pylint: enable=too-few-public-methods
