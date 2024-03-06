# Copyright Capgemini Engineering B.V.

"""quality_gate."""
import i18n
from loguru import logger


class QualityGateError(Exception):
    """Generic quality gate error."""


# pylint: disable=too-few-public-methods
class QualityGate:
    """Class to handle quality gate comparisons."""

    def __init__(self, parent, metric, threshold, operator):
        """Initialize quality gate.

        :param path: path to configuration containing metric, threshold and operator
        :param quality_gate_configuration: configuration containing metric, threshold and operator
        """
        self.input_value = None

        self.metric = metric
        self.threshold = threshold
        self.operator = operator
        self.is_percentage = False

        if self.operator not in self.OPERATOR_MAPPING_FUNCTION:
            raise QualityGateError(
                i18n.t(
                    "acidcli.quality_gate.invalid_operator",
                    operator=self.operator,
                    keys=self.OPERATOR_MAPPING_FUNCTION.keys(),
                    path=f"{parent.parent.name}->{parent.name}",
                )
            )

    def compare(self, comparison_value=None, logging_enabled=False):
        """Compare self.input_value or comparison_value against threshold with operator.

        :param comparison_value: Value to compare against threshold
        :param logging_enabled: enable info logging of succesfull gate
        """
        if comparison_value is None:
            if self.input_value is None:
                raise QualityGateError(
                    i18n.t(
                        "acidcli.quality_gate.comparison_value_missing",
                        metric=self.metric,
                    )
                )
            comparison_value = self.input_value

        within_threshold = self.OPERATOR_MAPPING_FUNCTION.get(self.operator)(self, comparison_value)

        if within_threshold and logging_enabled:
            logger.info(
                i18n.t(
                    "acidcli.quality_gate.comparison_equal",
                    input_value=self.input_value if comparison_value is None else comparison_value,
                    operator=self.OPERATOR_MAPPING_TEXT.get(self.operator),
                    threshold=self.threshold,
                    metric=self.metric,
                )
            )
        if not within_threshold:
            raise QualityGateError(
                i18n.t(
                    "acidcli.quality_gate.comparison_not_equal",
                    input_value=self.input_value,
                    operator=self.OPERATOR_MAPPING_TEXT.get(self.operator),
                    threshold=self.threshold,
                    metric=self.metric,
                )
            )

    def _compare_lower_then(self, input_value):
        """Lower then comparator.

        :param input_value: value to compare against threshold
        """
        if input_value < self.threshold:
            return True

        return False

    def _compare_lower_or_equal_then(self, input_value):
        """Lower then or equal comparator.

        :param input_value: value to compare against threshold
        """
        if input_value < self.threshold or input_value == self.threshold:
            return True

        return False

    def _compare_higher_then(self, input_value):
        """Higher then comparator.

        :param input_value: value to compare against threshold
        """
        if input_value > self.threshold:
            return True

        return False

    def _compare_higher_or_equal_then(self, input_value):
        """Higher then or equal comparator.

        :param input_value: value to compare against threshold
        """
        if input_value > self.threshold or input_value == self.threshold:
            return True

        return False

    def _compare_equal(self, input_value):
        if input_value == self.threshold:
            return True

        return False

    OPERATOR_MAPPING_FUNCTION = {
        "<": _compare_lower_then,
        "<=": _compare_lower_or_equal_then,
        ">": _compare_higher_then,
        ">=": _compare_higher_or_equal_then,
        "=": _compare_equal,
    }

    OPERATOR_MAPPING_TEXT = {
        "<": "less than",
        "<=": "less or equal than",
        ">": "higher than",
        ">=": "higher or equal than",
        "=": "equal to",
    }

    @staticmethod
    def find_and_update_quality_gate(quality_gates, metric, value, mandatory=False, is_percentage=False):
        """find_and_update_quality_gate.

        Find the Quality Gate from a list and update

        :param quality_gates: list with QualityGate objects
        :param metric: Name of metric
        :param value: Value of metric
        :param mandatory: Must the Quality gate exist
        :param is_percentage: Whether to interpret value and threshold as percentage or not
        """
        logger.debug(f"Metrics: {metric}: {value}")

        try:
            quality_gate = next(quality_gate for quality_gate in quality_gates if quality_gate.metric == metric)
            quality_gate.input_value = value
            quality_gate.is_percentage = is_percentage
        except StopIteration as exception:
            if mandatory:
                raise QualityGateError(
                    i18n.t(
                        "acidcli.quality_gate.quality_gate_missing",
                        metric=metric,
                        value=value,
                    )
                ) from exception

    @staticmethod
    def find_quality_gate_threshold(quality_gates, metric):
        """find_quality_gate_threshold.

        Find the Quality Gate from a list and return threshold

        :param quality_gates: list with QualityGate objects
        :param metric: Name of metric
        """
        try:
            return next(quality_gate for quality_gate in quality_gates if quality_gate.metric == metric).threshold
        except StopIteration:
            return None

    @staticmethod
    def find_quality_gate(quality_gates, metric):
        """find_quality_gate.

        Find the Quality Gate from a list and return object

        :param quality_gates: list with QualityGate objects
        :param metric: Name of metric
        """
        try:
            return next(quality_gate for quality_gate in quality_gates if quality_gate.metric == metric)
        except StopIteration:
            return None

    @staticmethod
    def remove_quality_gate(quality_gates, quality_gate):
        """remove_quality_gate.

        Remove the Quality Gate from the quality_gates list

        :param quality_gates: list with QualityGate objects
        :param quality_gate: QualityGate object to remove
        """
        quality_gates.remove(quality_gate)


# pylint: enable=too-few-public-methods
