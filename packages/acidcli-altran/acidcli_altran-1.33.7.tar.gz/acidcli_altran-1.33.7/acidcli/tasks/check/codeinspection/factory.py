# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for CodeInspection
"""
from acidcli.tasks.check.codeinspection.cppcheck_and_clang import Cppcheck
from acidcli.tasks.check.codeinspection.pmd_and_spotbugs import PmdSpotbugsGradle
from acidcli.tasks.check.codeinspection.resharper import Resharper
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckCodeInspection(TaskFactory):
    """CodeInspection factory."""

    def __init__(self):
        """Initialize CodeInspection for different languages."""
        super().__init__()
        self._creators = {"CS": Resharper, "C": Cppcheck, "CPP": Cppcheck, "Java": {"Gradle": PmdSpotbugsGradle}}


# pylint: enable=too-few-public-methods
