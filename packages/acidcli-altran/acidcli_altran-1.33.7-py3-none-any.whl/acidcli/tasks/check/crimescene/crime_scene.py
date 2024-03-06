# Copyright Capgemini Engineering B.V.

"""Crime scene.

Crime scene tooling implementation
"""
from itertools import chain

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.facility.subprocess import Subprocess
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class CrimeScene(Executable):
    """CrimeScene."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Check Crimescene.

        Analyze code with Crimescene

        :param job: job model object with job configuration
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["output"])

        code_locations = list(chain.from_iterable([x.directories for x in self.__job.parent.parent.code_locations]))

        self.__run_crime_scene(code_locations, "hotspot")
        self.__run_crime_scene(code_locations, "knowledge_map")
        self.__run_crime_scene(code_locations, "temporal_coupling")
        self.__run_crime_scene(code_locations, "wordcloud")
        self.__run_crime_scene(code_locations, "code_flower")

    @function_debug
    def __run_crime_scene(self, code_locations, command):
        """Run Crimescene.

        Run a crime scene analysis.

        :param code_locations: The code_locations which will be scanned by Crimescene.
        :param command: The command which specifies which analysis should be executed.
        """
        crime_scene_command = [
            "crimescene",
            command,
            "--output",
            self._parameter_value(self.__job, "output"),
            "--input",
        ]
        crime_scene_command.extend(code_locations)

        process = Subprocess(crime_scene_command, verbose=self._parameter_value(self.__job, "verbose"))
        process.execute_pipe(self._parameter_value(self.__job, "output"), f"crimescene_{command}")


# pylint: enable=too-few-public-methods
