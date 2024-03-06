# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for docstyle
"""
from acidcli.tasks.check.docstyle.pydocstyle import PyDocStyle
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckDocStyle(TaskFactory):
    """Doc style factory."""

    def __init__(self):
        """Initialize doc style for different languages."""
        super().__init__()
        self._creators = {
            "Python": PyDocStyle,
        }


# pylint: enable=too-few-public-methods
