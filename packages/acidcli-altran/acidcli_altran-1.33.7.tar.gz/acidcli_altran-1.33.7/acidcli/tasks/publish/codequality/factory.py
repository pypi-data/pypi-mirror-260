# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for CodeQuality
"""
from acidcli.tasks.publish.codequality.sonar_scanner_msbuild import SonarScannerMSBuild
from acidcli.tasks.publish.codequality.sonar_scanner_python import SonarScannerPython
from acidcli.tasks.publish.codequality.sonar_scanner_cpp import SonarScannerCpp
from acidcli.tasks.publish.codequality.sonar_scanner_c import SonarScannerC
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class PublishCodeQuality(TaskFactory):
    """CodeQuality factory."""

    def __init__(self):
        """Initialize CodeQuality for different languages."""
        super().__init__()
        self._creators = {
            "CS": {"NUnit": SonarScannerMSBuild, "MSTest": SonarScannerMSBuild},
            "C": SonarScannerC,
            "CPP": SonarScannerCpp,
            "Python": SonarScannerPython,
        }


# pylint: enable=too-few-public-methods
