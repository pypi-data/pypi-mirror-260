# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for building binaries
"""
from acidcli.tasks.build.binaries.c_sharp import CSharp
from acidcli.tasks.build.binaries.cmake import CMake
from acidcli.tasks.build.binaries.gradle import Gradle
from acidcli.tasks.build.binaries.make import Make
from acidcli.tasks.build.binaries.maven import Maven
from acidcli.tasks.build.binaries.npm import Npm
from acidcli.tasks.build.binaries.simulink import Simulink
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class BuildBinaries(TaskFactory):
    """Binaries factory for Build stage."""

    def __init__(self):
        """Initialize build binaries for different languages."""
        super().__init__()
        self._creators = {
            "CPP": CMake,
            "CS": CSharp,
            "C": Make,
            "Java": {"Gradle": Gradle, "Maven": Maven},
            "npm": Npm,
            "Simulink": Simulink,
        }


# pylint: enable=too-few-public-methods
