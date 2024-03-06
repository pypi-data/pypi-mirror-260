# Copyright Capgemini Engineering B.V..

"""Python acceptance testing.

Acceptance feature testing for Python
"""
import os

from acidcli.facility.decorators import function_debug, print_job_info
from acidcli.quality_gate import QualityGate
from acidcli.shared_functions.coverage import Coverage
from acidcli.tasks.executable import Executable


# pylint: disable=too-few-public-methods
class Behave(Executable):
    """Behave."""

    def __init__(self):
        """__init__."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Execute acceptance features.

        Execute feature tests for Python with coverage and behave.

        :param job: job model object with job configuration.
        Execute acceptance features.
        """
        self.__job = job
        self._required_parameters_available(self.__job, ["config", "output"])

        os.environ["COVERAGE_PROCESS_START"] = os.path.join(os.getcwd(), self._parameter_value(self.__job, "config"))

        output = self._parameter_value(self.__job, "output")
        verbose = self._parameter_value(self.__job, "verbose")
        config = self._parameter_value(self.__job, "config")

        coverage = Coverage()
        coverage.run_module(["behave", "--junit"], output, verbose=verbose, config=config)
        coverage.combine(output, verbose=verbose, config=config)
        coverage.export_html_report(output, verbose=verbose, config=config)
        coverage.export_xml_report(output, verbose=verbose, config=config)

        coverage_results = coverage.read_coverage_xml_results(output)
        coverage.print_coverage_results(coverage_results)

        coverage_percentages = Coverage.calculate_coverage_percentages(coverage_results)
        self.__update_quality_gates(coverage_percentages)

    @function_debug
    def __update_quality_gates(self, coverage_percentages):
        """Update quality gates.

        Update quality gates with corresponding input values.

        :param coverage_percentages: line, branch, and total coverage percentages.
        """
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, "CoveragePercentage", coverage_percentages["total"], is_percentage=True
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, "LineCoveragePercentage", coverage_percentages["line"], is_percentage=True
        )
        QualityGate.find_and_update_quality_gate(
            self.__job.qualitygates, "BranchCoveragePercentage", coverage_percentages["branch"], is_percentage=True
        )
