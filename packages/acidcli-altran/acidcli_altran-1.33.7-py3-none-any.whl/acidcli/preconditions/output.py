# Copyright Capgemini Engineering B.V.

"""Output preconditions."""
import os
import shutil

from loguru import logger

from acidcli.preconditions.exceptions import PreconditionError
from acidcli.preconditions.precondition import Precondition


class OutputDirectoryExists(Precondition):
    """Directory exists.

    Enforce existence of the output directory. Directory is created when it does not exist.
    """

    def enforce(self, job):
        """Enforce."""
        logger.info("Enforce: output directory exists")

        folder = self._validate_parameter(job, "output")

        try:
            os.makedirs(folder, exist_ok=True)
        except OSError as exception:
            raise PreconditionError(f"Failed to create directory {folder}. Reason: {exception}") from exception


class OutputDirectoryIsEmpty(Precondition):
    """Output is empty? .

    Enforce empty output directory. Remove all files and folders from the directory.
    """

    def enforce(self, job):
        """Enforce."""
        logger.info("Enforce: output directory is empty")

        folder = self._validate_parameter(job, "output")

        for filename in os.listdir(folder):
            directory_item = os.path.join(folder, filename)

            try:
                self._remove_content(directory_item)
            except OSError as exception:
                raise PreconditionError(f"Failed to delete {directory_item}. Reason: {exception}") from exception

    @staticmethod
    def _remove_content(directory_item):
        """Remove content."""
        if os.path.isfile(directory_item) or os.path.islink(directory_item):
            os.unlink(directory_item)
        else:
            shutil.rmtree(directory_item)
