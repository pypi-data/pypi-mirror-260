# Copyright Capgemini Engineering B.V..

"""Decorators.

General python function decorators.
"""
from functools import wraps

from i18n import t as translation
from loguru import logger


def function_debug(func):
    """Decorate function with debug prints.

    Add debug prints informing when a function starts and stops

    :param func: function attribute of wrapped function
    :return: function results
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger_ = logger.opt(depth=1)
        logger_.debug(translation("acidcli.process.starting_function", function=func.__name__))
        result = func(*args, **kwargs)
        logger_.debug(translation("acidcli.process.finished_function", function=func.__name__))
        return result

    return wrapper


def print_job_info(func):
    """Decorate function with prints about the start and finish of a job.

    Add info prints informing when a job starts and stops

    :param func: function attribute of wrapped function
    :return: function results
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger_ = logger.opt(depth=1)
            logger_.info(translation("acidcli.process.starting_job", stage=args[1].parent.name, job=args[1].name))
            result = func(*args, **kwargs)
            logger_.info(translation("acidcli.process.finished_job", stage=args[1].parent.name, job=args[1].name))
            return result
        except AttributeError:
            logger_ = logger.opt(depth=1)
            logger_.info(translation("acidcli.process.starting_job", stage=args[2].stage, job=args[2].job))
            result = func(*args, **kwargs)
            logger_.info(translation("acidcli.process.finished_job", stage=args[2].stage, job=args[2].job))
            return result

    return wrapper
