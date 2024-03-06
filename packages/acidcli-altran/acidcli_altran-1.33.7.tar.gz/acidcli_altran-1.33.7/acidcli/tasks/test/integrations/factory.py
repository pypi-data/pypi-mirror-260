# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for testing units
"""
from acidcli.tasks.task_factory import TaskFactory
from acidcli.tasks.test.units.csharp_units import CSharpUnits


# pylint: disable=too-few-public-methods
class TestIntegrations(TaskFactory):
    """Units factory."""

    def __init__(self):
        """Initialize unit tests for different languages."""
        super().__init__()
        self._creators = {
            "CS": {"NUnit": CSharpUnits, "MSTest": CSharpUnits},
        }


# pylint: enable=too-few-public-methods
