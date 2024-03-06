# Copyright Capgemini Engineering B.V..

"""Factory.

Factory implementation for acceptance features
"""
from acidcli.tasks.acceptance.features.behave import Behave
from acidcli.tasks.acceptance.features.cmake import CMake
from acidcli.tasks.test.units.csharp_units import CSharpUnits
from acidcli.tasks.acceptance.features.gradle import Gradle
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class AcceptanceFeatures(TaskFactory):
    """Features factory for Acceptance stage."""

    def __init__(self):
        """Initialize acceptance features for different languages."""
        super().__init__()
        self._creators = {
            "CPP": CMake,
            "CS": {"NUnit": CSharpUnits, "MSTest": CSharpUnits},
            "C": CMake,
            "Java": {"Gradle": Gradle},
            "Python": Behave,
        }


# pylint: enable=too-few-public-methods
