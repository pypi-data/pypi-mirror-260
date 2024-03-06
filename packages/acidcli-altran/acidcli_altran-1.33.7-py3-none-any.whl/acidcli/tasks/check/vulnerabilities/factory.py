# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for Vulnerability checks
"""
from acidcli.tasks.check.vulnerabilities.grype import Grype
from acidcli.tasks.check.vulnerabilities.bandit import Bandit
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckVulnerabilities(TaskFactory):
    """Vulnerabilities factory."""

    def __init__(self):
        """Initialize vulnerability checks for different languages."""
        super().__init__()
        self._creators = {
            "Docker": Grype,
            "Python": Bandit,
        }


# pylint: enable=too-few-public-methods
