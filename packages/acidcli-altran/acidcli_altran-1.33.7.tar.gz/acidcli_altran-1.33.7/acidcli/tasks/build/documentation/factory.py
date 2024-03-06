# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for building documentation
"""
from acidcli.tasks.build.documentation.pandoc import Pandoc
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class BuildDocumentation(TaskFactory):
    """Documentation factory."""

    def __init__(self):
        """Initialize Documentation for different tools."""
        super().__init__()
        self._creators = {
            "Markdown": {"Pandoc": Pandoc},
        }


# pylint: enable=too-few-public-methods
