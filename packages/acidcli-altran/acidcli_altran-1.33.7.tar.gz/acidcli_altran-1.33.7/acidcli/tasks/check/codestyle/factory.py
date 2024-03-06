# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for codestyle
"""
from acidcli.tasks.check.codestyle.checkstyle import CheckStyle
from acidcli.tasks.check.codestyle.pycodestyle import PyCodeStyle
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckCodeStyle(TaskFactory):
    """Code style factory."""

    def __init__(self):
        """Initialize code style for different languages."""
        super().__init__()
        self._creators = {
            "Java": {"Gradle": CheckStyle},
            "Python": PyCodeStyle,
        }


# pylint: enable=too-few-public-methods
