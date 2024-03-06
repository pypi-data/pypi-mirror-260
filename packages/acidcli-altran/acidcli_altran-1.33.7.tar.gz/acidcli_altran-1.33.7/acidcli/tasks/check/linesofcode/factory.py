# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for LinesOfCode
"""
from acidcli.tasks.check.linesofcode.linesofcode import LinesOfCode
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckLinesOfCode(TaskFactory):
    """LinesOfCode factory."""

    def __init__(self):
        """Initialize LinesOfCode for different languages."""
        super().__init__()
        self._creators = {
            "Independent": {"CLOC": LinesOfCode},
        }


# pylint: enable=too-few-public-methods
