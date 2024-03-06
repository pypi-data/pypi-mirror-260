# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for Markdown
"""
from acidcli.tasks.check.doclint.markdown import MarkdownLint
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckDocLint(TaskFactory):
    """Markdown factory."""

    def __init__(self):
        """Initialize markdown for different languages."""
        super().__init__()
        self._creators = {
            "Markdown": MarkdownLint,
        }


# pylint: enable=too-few-public-methods
