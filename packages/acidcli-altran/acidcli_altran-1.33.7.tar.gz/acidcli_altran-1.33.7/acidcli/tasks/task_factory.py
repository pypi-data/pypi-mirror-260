# Copyright Capgemini Engineering B.V.

"""Task factory.

Template for factory pattern, where init needs override to declare
the factory behaviour
"""
from abc import ABC
from abc import abstractmethod

from acidcli.exceptions import CLIError


# pylint: disable=too-few-public-methods
class TaskFactory(ABC):
    """Task factory."""

    @abstractmethod
    def __init__(self):
        """Init function."""
        self._creators = {}

    def get_executable(self, language, platform):
        """Get factory implementation based on key."""
        creator = self._creators.get(language)

        if platform is not None:
            if isinstance(creator, dict):
                creator = creator.get(platform)
            else:
                raise CLIError(language)

        if not creator:
            raise ValueError(language)

        return creator()


# pylint: enable=too-few-public-methods
