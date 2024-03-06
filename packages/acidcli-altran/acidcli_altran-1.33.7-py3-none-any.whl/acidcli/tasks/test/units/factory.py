# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for testing units
"""
from acidcli.tasks.task_factory import TaskFactory
from acidcli.tasks.test.units.cmake import CMake
from acidcli.tasks.test.units.pytest import Pytest
from acidcli.tasks.test.units.csharp_units import CSharpUnits
from acidcli.tasks.test.units.gradle import Gradle
from acidcli.tasks.test.units.maven import Maven
from acidcli.tasks.test.units.make import Make
from acidcli.tasks.test.units.npm import Npm
from acidcli.tasks.test.units.simulink import Simulink
from acidcli.tasks.test.units.simulink_test_runner import SimulinkTestRunner


# pylint: disable=too-few-public-methods
class TestUnits(TaskFactory):
    """Units factory."""

    def __init__(self):
        """Initialize unit tests for different languages."""
        super().__init__()
        self._creators = {
            "CPP": CMake,
            "CS": {"NUnit": CSharpUnits, "MSTest": CSharpUnits},
            "C": Make,
            "Java": {"Gradle": Gradle, "Maven": Maven},
            "npm": Npm,
            "Python": Pytest,
            "Simulink": {"Legacy": Simulink, "TestRunner": SimulinkTestRunner},
        }


# pylint: enable=too-few-public-methods
