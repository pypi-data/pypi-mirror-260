# Copyright Capgemini Engineering B.V..

"""valgrind.

Generic abstraction for working with valgrind.
"""
from os.path import isfile

import i18n
from loguru import logger
from xmltodict import parse as parse_xml

from acidcli.exceptions import CLIError


class Valgrind:
    """Valgrind."""

    def read_valgrind_xml_results_file(self, path):
        """Read valgrind results.

        Load valgrind results from exported XML file and convert into dictionary.

        :param path: Location to persist log files.
        :returns: Dictionary containing valgrind results.
        """
        if not isfile(path):
            raise CLIError("valgrind xml report not found at {}.".format(path))
        with open(path) as input_file:
            valgrind_result = self.read_valgrind_xml_results_string(input_file.read())
        return valgrind_result

    @staticmethod
    def read_valgrind_xml_results_string(data):
        """Read valgrind results.

        Load valgrind results from exported XML file and convert into dictionary.

        :param data: decoded valgrind xml file.
        :returns: Dictionary containing valgrind results.
        """
        valgrind_result = parse_xml(data.split("\n", 2)[2], dict_constructor=dict)
        return valgrind_result

    @staticmethod
    def parse_valgrind(valgrind_parsed_xml):
        """Parse valgrind results.

        Read the valgrind results, and prepare them for Quality Gates.
        :param valgrind_parsed_xml: valgrind parsed xml
        :returns: Amount of memory leaks in bytes and blocks.
        """
        valgrind_results = {
            "Leak_DefinitelyLost": {"bytes": 0, "blocks": 0},
            "Leak_IndirectlyLost": {"bytes": 0, "blocks": 0},
            "Leak_PossiblyLost": {"bytes": 0, "blocks": 0},
            "Leak_StillReachable": {"bytes": 0, "blocks": 0},
        }

        for error in valgrind_parsed_xml["valgrindoutput"]["error"]:
            if "xwhat" in error:
                valgrind_results[error["kind"]]["bytes"] += int(error["xwhat"]["leakedbytes"])
                valgrind_results[error["kind"]]["blocks"] += int(error["xwhat"]["leakedblocks"])
        for key, item in valgrind_results.items():
            if item["bytes"]:
                logger.error(
                    i18n.t(
                        "acidcli.valgrind_memory_leak_found",
                        leak_type=key,
                        bytes=item["bytes"],
                        blocks=item["blocks"],
                    )
                )
        return valgrind_results
