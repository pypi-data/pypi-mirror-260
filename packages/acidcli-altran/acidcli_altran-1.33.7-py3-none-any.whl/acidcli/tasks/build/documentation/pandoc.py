# Copyright Capgemini Engineering B.V.

"""Pandoc.

Pandoc build documentation implementation
"""
import posixpath
import shutil

from os import makedirs, pathsep, remove
from os.path import join, isdir, isfile, dirname, exists
from shutil import copyfile, copytree

from acidcli.facility.decorators import print_job_info, function_debug
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable

VERSIONING_FILE_NAME = "acidcli_versioning.txt"


# pylint: disable=too-few-public-methods
class Pandoc(Executable):
    """Pandoc."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Build documentation.

        Build documentation with Pandoc

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["input", "output", "title", "document_class"])
        self._required_list_parameters_available(self.__job, ["files"])
        self.__create_version_file()
        self.__create_nonexistent_defaults()
        self.__run_pandoc(self.__get_html_specific_command_parameters())
        self.__populate_output_folder()
        self.__run_pandoc(self.__get_pdf_specific_command_parameters())
        self.__remove_plantuml_temporary_files()
        self.__remove_version_file()

    @function_debug
    def __run_pandoc(self, output_specific_command_parameters):
        """Run pandoc.

        Run pandoc command as subprocess

        :param output_specific_command_parameters: extra commands to extend the base command with
        """
        pandoc_command = [
            "pandoc",
            "--standalone",
            "--from=markdown",
            "--toc",
            "--number-sections",
            "--filter",
            "pandoc-plantuml",
            "--metadata",
            f"title={self._parameter_value(self.__job, 'title')}",
        ]
        versioning = self._parameter_as_bool(self.__job, "versioning")
        if versioning or versioning is None:
            pandoc_command.extend(["--include-before-body", VERSIONING_FILE_NAME])
        pandoc_command.extend(output_specific_command_parameters)
        pandoc_command.extend(
            [
                join(self._parameter_value(self.__job, "input"), file)
                for file in self._parameter_value(self.__job, "files")
            ]
        )
        process = Subprocess(pandoc_command, verbose=self._parameter_value(self.__job, "verbose"))
        process.execute_pipe(
            self._parameter_value(self.__job, "output"), "pandoc"
        )

    @function_debug
    def __get_html_specific_command_parameters(self):
        """Get HTML specific command parameters.

        :returns: list with command parameters as string
        """
        return [
            "--to=html5",
            "--css=stylesheet.css",
            f"--include-after-body={join(self._parameter_value(self.__job, 'input'), 'footer.html')}",
            f"--output={join(self._parameter_value(self.__job, 'output'), 'index')}.html",
        ]

    @function_debug
    def __get_pdf_specific_command_parameters(self):
        """Get PDF specific command parameters.

        :returns: list with command parameters as string
        """
        return [
            "--to=latex",
            "--pdf-engine=lualatex",
            "--template",
            join(self._parameter_value(self.__job, "input"), "template.latex"),
            "--variable",
            f"documentclass={self._parameter_value(self.__job, 'document_class')}",
            "--variable",
            f"images_path={posixpath.join(self._parameter_value(self.__job, 'input'), 'images')}",
            f"--resource-path=.{pathsep}{self._parameter_value(self.__job, 'input')}",
            f"--output="
            f"{join(self._parameter_value(self.__job, 'output'), self._parameter_value(self.__job, 'title'))}.pdf",
        ]

    @function_debug
    def __create_nonexistent_defaults(self):
        """Create nonexistent defaults.

        Create default files in the input folder.
        If these files are already present, they will not be overridden.
        """
        self.__copy_file_if_nonexistent("pandoc.css")
        self.__copy_file_if_nonexistent("footer.html")
        makedirs(join(self._parameter_value(self.__job, "input"), "images"), exist_ok=True)
        self.__copy_file_if_nonexistent(join("images", "logo.svg"))
        self.__copy_file_if_nonexistent(join("images", "logo.png"))
        self.__copy_file_if_nonexistent("template.latex")

    @function_debug
    def __copy_file_if_nonexistent(self, filepath):
        """Copy file if nonexistent.

        Copies a file from the defaults directory to the input directory.
        If the file already exists in the input directory, the default file will not be copied.

        :param filepath: The filepath of the file that will be copied, as seen from the defaults folder.
        """
        source = join(dirname(__file__), "..", "..", "..", "defaults", "pandoc")
        destination = self._parameter_value(self.__job, "input")
        if not isfile(join(destination, filepath)):
            copyfile(join(source, filepath), join(destination, filepath))

    @function_debug
    def __populate_output_folder(self):
        """Populate output folder.

        Populate the output folder with the required directories, stylesheet and images
        """
        copyfile(
            join(self._parameter_value(self.__job, "input"), "pandoc.css"),
            join(self._parameter_value(self.__job, "output"), "stylesheet.css")
        )
        copytree(
            join(self._parameter_value(self.__job, "input"), "images"),
            join(self._parameter_value(self.__job, "output"), "images")
        )
        if isdir(join(".", "plantuml-images")):
            copytree(
                join(".", "plantuml-images"),
                join(self._parameter_value(self.__job, "output"), "plantuml-images"),
                ignore=shutil.ignore_patterns("*.uml")
            )

    @staticmethod
    @function_debug
    def __remove_plantuml_temporary_files():
        """Remove temporary files.

        Remove files that were created by pandoc-plantuml-filter.
        """
        if isdir(join(".", "plantuml-images")):
            shutil.rmtree(join(".", "plantuml-images"))

    @function_debug
    def __create_version_file(self):
        """add_version_to_file.

        Generate version file.
        """
        versioning = self._parameter_as_bool(self.__job, "versioning")
        if versioning or versioning is None:
            with open(VERSIONING_FILE_NAME, 'w+', encoding="utf-8") as file:
                file.write(f"Version: {self._parameter_value(self.__job, 'version')}")

    @function_debug
    def __remove_version_file(self):
        """remove_version_from_file.

        Remove version file.
        """
        versioning = self._parameter_as_bool(self.__job, "versioning")
        if versioning or versioning is None:
            if exists(VERSIONING_FILE_NAME):
                remove(VERSIONING_FILE_NAME)

# pylint: enable=too-few-public-methods
