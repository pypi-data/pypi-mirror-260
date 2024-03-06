# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for building documentation
"""

from acidcli.tasks.build.codedocumentation.doxygen import Doxygen
from acidcli.tasks.task_factory import TaskFactory

# pylint: disable=too-few-public-methods


class BuildCodeDocumentation(TaskFactory):
    """CodeDocumentation factory."""

    def __init__(self):
        """Initialize Documentation for different tools."""
        super().__init__()
        self._creators = {
            "Independent": {"Doxygen": Doxygen},
        }


# pylint: enable=too-few-public-methods
