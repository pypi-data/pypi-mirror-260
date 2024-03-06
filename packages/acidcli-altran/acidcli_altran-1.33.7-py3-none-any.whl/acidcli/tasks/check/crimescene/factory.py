# Copyright Capgemini Engineering B.V.

"""Factory.

Factory implementation for crime scene
"""
from acidcli.tasks.check.crimescene.crime_scene import CrimeScene
from acidcli.tasks.task_factory import TaskFactory


# pylint: disable=too-few-public-methods
class CheckCrimeScene(TaskFactory):
    """Crime scene factory."""

    def __init__(self):
        """Initialize doc style for different languages."""
        super().__init__()
        self._creators = {
            "Independent": {"CrimeScene": CrimeScene},
        }


# pylint: enable=too-few-public-methods
