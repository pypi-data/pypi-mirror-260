# Copyright Capgemini Engineering B.V.

"""CICD Postconditions.

----
Postconditions are used to check if a task passed successfully.
"""
from acidcli.postconditions.exceptions import PostconditionError
from acidcli.postconditions.output import OutputDirectoryIsNotEmpty
from acidcli.postconditions.postcondition import Postcondition
