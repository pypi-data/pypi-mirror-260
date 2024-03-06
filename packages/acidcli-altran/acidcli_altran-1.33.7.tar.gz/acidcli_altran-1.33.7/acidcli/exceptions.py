# Copyright Capgemini Engineering B.V.

"""acidcli exceptions.

Specific exceptions for acidcli
"""


class CLIError(Exception):
    """Generic CLI error."""


class VersionError(Exception):
    """Versioning error."""
