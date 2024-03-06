# Copyright Capgemini Engineering B.V.

"""AssemblyVersion preconditions."""

import codecs
import os
import re

from loguru import logger
from acidcli.preconditions.precondition import Precondition
from acidcli.facility.decorators import function_debug


class AssemblyVersionUpdated(Precondition):
    """C# Update Assembly Version.

    Make sure version is updated in Assembly files
    """

    def enforce(self, job):
        """Enforce."""
        logger.info("Enforce: C# set version")

        version = self._validate_parameter(job, "version")

        workspace = os.getcwd()
        logger.debug(f"Search for 'AssemblyInfo.cs' files in {workspace}")
        for root, _, files in os.walk(workspace):
            for file in files:
                if file.endswith("AssemblyInfo.cs"):
                    self._adjust_assembly_version(
                        os.path.join(root, file), "AssemblyVersion", version.get_assemblyversion()
                    )
                    self._adjust_assembly_version(
                        os.path.join(root, file), "AssemblyFileVersion", version.get_assemblyversion()
                    )

        logger.info("Finished: C# set version")

    @staticmethod
    @function_debug
    def _adjust_assembly_version(full_file_name, assembly, new_version):
        """Adjust the given assembly value for all projects."""
        regex = re.compile(r"\[assembly: %s\(\"(.*)\"\)\]" % assembly)

        file_content = AssemblyVersionUpdated._read_file(full_file_name, "utf-8-sig")

        for group in re.findall(regex, file_content):
            replace_old = f'[assembly: {assembly}("{group}")]'
            replace_new = f'[assembly: {assembly}("{new_version}")]'
            file_content = file_content.replace(replace_old, replace_new)
            logger.debug(f"Changed AssemblyVersion from {group} to {new_version} for {full_file_name}")
        AssemblyVersionUpdated._write_file(full_file_name, "utf-8-sig", file_content)

    @staticmethod
    @function_debug
    def _read_file(full_file_name, encoding):
        """Read the content of the given file."""
        with codecs.open(full_file_name, "r", encoding=encoding) as file_stream:
            return file_stream.read()

    @staticmethod
    @function_debug
    def _write_file(full_file_name, encoding, file_content):
        """Write the given content to the given file."""
        with codecs.open(full_file_name, "w", encoding=encoding) as file_stream:
            file_stream.write(file_content)
