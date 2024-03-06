# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for documentation spelling checks
"""
from acidcli.tasks.check.docspell.markdown import MarkdownSpell
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckDocSpell(TaskFactory):
    """Documentation spelling factory."""

    def __init__(self):
        """Initialize documentation spell check for different languages."""
        super().__init__()
        self._creators = {
            "Markdown": MarkdownSpell,
        }


# pylint: enable=too-few-public-methods
