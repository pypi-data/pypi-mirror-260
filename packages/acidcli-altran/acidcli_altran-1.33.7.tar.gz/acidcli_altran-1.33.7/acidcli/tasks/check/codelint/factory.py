# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for code linting
"""
from acidcli.tasks.check.codelint.pylint import PythonLint
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckCodeLint(TaskFactory):
    """Code linting factory."""

    def __init__(self):
        """Initialize code linting for different languages."""
        super().__init__()
        self._creators = {
            "Python": PythonLint,
        }


# pylint: enable=too-few-public-methods
