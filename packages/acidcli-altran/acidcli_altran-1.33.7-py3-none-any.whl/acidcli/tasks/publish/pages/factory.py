# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for Pages
"""

from acidcli.tasks.task_factory import TaskFactory
from acidcli.tasks.publish.pages.pages import Pages


# pylint: disable=too-few-public-methods
class PublishPages(TaskFactory):
    """Pages factory."""

    def __init__(self):
        """Initialize Pages."""
        super().__init__()
        self._creators = {
            "Independent": Pages,
        }


# pylint: enable=too-few-public-methods
