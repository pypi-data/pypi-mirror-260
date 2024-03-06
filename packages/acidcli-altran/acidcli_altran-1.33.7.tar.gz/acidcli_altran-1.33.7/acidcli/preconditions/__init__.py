# Copyright Capgemini Engineering B.V.

"""Preconditions.

All available preconditions need to be exposed
"""
from acidcli.preconditions.config import ConfigFileExists
from acidcli.preconditions.exceptions import PreconditionError
from acidcli.preconditions.input import InputDirectoryIsNotEmpty
from acidcli.preconditions.input import InputFileExists
from acidcli.preconditions.npm import NpmPackagesInstalled
from acidcli.preconditions.nuget import NugetPackagesRestored
from acidcli.preconditions.assemblyversion import AssemblyVersionUpdated
from acidcli.preconditions.output import OutputDirectoryExists
from acidcli.preconditions.output import OutputDirectoryIsEmpty
from acidcli.preconditions.precondition import Precondition
