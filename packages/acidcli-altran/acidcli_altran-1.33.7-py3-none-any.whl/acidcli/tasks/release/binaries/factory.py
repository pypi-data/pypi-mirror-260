# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for release binaries
"""
from acidcli.tasks.release.binaries.publish_directory import PublishDirectory
from acidcli.tasks.release.binaries.publish_gradle import PublishGradle
from acidcli.tasks.release.binaries.publish_nuget import PublishNuget
from acidcli.tasks.release.binaries.publish_p2 import PublishP2
from acidcli.tasks.release.binaries.publish_python import PublishPython
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class ReleaseBinaries(TaskFactory):
    """Binaries factory for Release stage."""

    def __init__(self):
        """Initialize release binaries for different languages."""
        super().__init__()
        self._creators = {
            "CPP": PublishDirectory,
            "CS": PublishNuget,
            "C": PublishDirectory,
            "Independent": PublishDirectory,
            "Java": {"Gradle": PublishGradle, "P2": PublishP2},
            "Python": PublishPython,
        }


# pylint: enable=too-few-public-methods
