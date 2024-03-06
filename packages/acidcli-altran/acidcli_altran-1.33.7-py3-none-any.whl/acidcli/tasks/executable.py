# Copyright Capgemini Engineering B.V.

"""task interface.

Interface that declares the common opperation of all task implementations
"""
from abc import ABC
from abc import abstractmethod
import i18n

from acidcli.exceptions import CLIError


# pylint: disable=too-few-public-methods


class Executable(ABC):
    """Strategy interface that declares the common operation to all tasks."""

    @abstractmethod
    def execute(self, job):
        """execute."""

    def _required_parameters_available(self, job, required_parameters):
        """Check if required_parameters are available and of type string in job model."""
        self.__required_list_parameters_of_type(job, required_parameters, str)

    def _required_list_parameters_available(self, job, required_parameters):
        """Check if required_parameters are available and of type list in job model."""
        self.__required_list_parameters_of_type(job, required_parameters, list)

    def __required_list_parameters_of_type(self, job, required_parameters, parameter_type):
        """Check if all required parameters are provided and are of the correct type."""
        job_parameters = []
        for parameter in job.parameters:
            if parameter.name in required_parameters:
                if not isinstance(parameter.value, parameter_type):
                    raise CLIError(
                        i18n.t(
                            "acidcli.parameter.invalid",
                            task=self.__class__.__name__,
                            parameter=parameter.name,
                            type=parameter_type.__name__,
                            received_type=parameter.value.__class__.__name__,
                        )
                    )
                job_parameters.append(parameter.name)

        if not all(elements in job_parameters for elements in required_parameters):
            raise CLIError(
                i18n.t(
                    "acidcli.parameter.missing",
                    task=self.__class__.__name__,
                    parameter=required_parameters,
                )
            )

    @staticmethod
    def _parameter_value(job, input_parameter):
        """Return value of parameter object that corresponds to the input_parameter."""
        for parameter in job.parameters:
            if parameter.name == input_parameter:
                return parameter.value

        return None

    @staticmethod
    def _parameter_as_bool(job, input_parameter):
        """Parameter as bool.

        :param input_parameter: name of parameter

        :return: bool, if parameter does not exist, return None
        """
        for parameter in job.parameters:
            if parameter.name == input_parameter:
                if parameter.value in ["true", "True"]:
                    return True
                if parameter.value in ["false", "False"]:
                    return False
                raise CLIError(
                    i18n.t(
                        "acidcli.parameter.invalid",
                        task=job.name,
                        parameter=input_parameter,
                        type="bool",
                        received_type=parameter.value.__class__.__name__,
                    )
                )
        return None

    def _validate_parameter(self, job_config, parameter, optional=False):
        """_validate_parameter."""
        try:
            return job_config.parameters[parameter]
        except KeyError as exception:
            if not optional:
                raise CLIError(
                    f"Failed to run task: {self.__class__.__name__}. Missing parameter: {parameter}"
                ) from exception

            return None

    def _validate_parameter_list(self, job_config, parameter, optional=False):
        """_validate_parameter_list."""
        try:
            parameters = job_config.parameters[parameter]
            if isinstance(parameters, list):
                return parameters

            raise CLIError(
                f"Failed to run task: {self.__class__.__name__}. Parameters in string format, list expected"
            )
        except KeyError as exception:
            if not optional:
                raise CLIError(
                    f"Failed to run task: {self.__class__.__name__}. Missing parameter: {parameter}"
                ) from exception

            return None


# pylint: enable=too-few-public-methods
