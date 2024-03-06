# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for Markdown
"""
from acidcli.tasks.check.featurelint.gherkin import GherkinLint
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckFeatureLint(TaskFactory):
    """Featurelint factory."""

    def __init__(self):
        """Initialize Featurelint for different languages."""
        super().__init__()
        self._creators = {
            "Gherkin": GherkinLint,
        }


# pylint: enable=too-few-public-methods
