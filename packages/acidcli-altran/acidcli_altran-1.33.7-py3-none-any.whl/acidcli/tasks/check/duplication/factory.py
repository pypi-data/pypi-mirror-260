# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for copy paste detection
"""
from acidcli.tasks.check.duplication.cpd import CopyPasteDetection
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckDuplication(TaskFactory):
    """Duplication factory."""

    def __init__(self):
        """Initialize copy paste detection for different languages."""
        super().__init__()
        self._creators = {
            "CPP": {"CPD": CopyPasteDetection},
            "CS": {"CPD": CopyPasteDetection},
            "C": {"CPD": CopyPasteDetection},
            "Java": {"CPD": CopyPasteDetection},
            "Python": {"CPD": CopyPasteDetection},
            "Matlab": {"CPD": CopyPasteDetection},
        }


# pylint: enable=too-few-public-methods
