# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for secrets
"""
from acidcli.tasks.check.secrets.trufflehog import TruffleHog
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckSecrets(TaskFactory):
    """Secrets factory."""

    def __init__(self):
        """Initialize code linting for different languages."""
        super().__init__()
        self._creators = {
            "Independent": TruffleHog,
        }


# pylint: enable=too-few-public-methods
