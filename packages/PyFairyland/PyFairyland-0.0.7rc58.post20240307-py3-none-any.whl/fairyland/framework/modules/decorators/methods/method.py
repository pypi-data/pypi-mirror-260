# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 02 29, 2024
"""
from types import FunctionType, MethodType
from typing import Union, Any, Callable

import time

from fairyland.framework.modules.journals.journal import journal, logger


class MethodTimingDecorator:
    """Calculate running time"""

    def __init__(self, __method: Union[FunctionType, MethodType]):
        """
        Initialize the decorator with the method to be wrapped.

        :param __method: The method/__method to be timed.
        :type __method: Union[FunctionType, MethodType]
        """
        self.__method = __method

    def __call__(self, *args, **kwargs):
        """
        Execute the wrapped method and calculate its execution time.

        :param args: Positional arguments passed to the method.
        :type args: tuple
        :param kwargs: Keyword arguments passed to the method.
        :type kwargs: dict
        :return: The result of the method execution.
        :rtype: Any
        """
        start_time = time.time()
        results = self.__method(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time.__lt__(60):
            elapsed_time_format_str = f"00:00:{elapsed_time:.3f}"
        elif elapsed_time.__ge__(60) and elapsed_time.__lt__(3600):
            elapsed_time_format_str = f"00:{(elapsed_time / 60).__int__():02d}:{elapsed_time % 60:06.3f}"
        else:
            elapsed_time_format_str = f"{(elapsed_time / 3600).__int__():02d}:{((elapsed_time - (elapsed_time / 3600).__int__() * 3600) / 60).__int__():02d}:{elapsed_time % 60:06.3f}"
        journal.success(f"This method ran for {elapsed_time_format_str}")
        return results


class MethodTipsDecorator:
    """Decorator to log method execution tips (start, success, failure)."""

    def __init__(self, __name: str = "A Method"):
        """
        Initialize the decorator with an optional method name.

        :param __name: The name of the method for logging purposes. Defaults to "A Method".
        :type __name: str
        """
        self.__name = __name

    def __call__(self, __method: Union[FunctionType, MethodType], *args: Any, **kwargs: Any) -> Callable[..., Any]:
        """
        The decorator's logic to wrap around the given method.

        :param __method: The function or method to be decorated.
        :type __method: Union[FunctionType, MethodType]
        :param args: args
        :type args: Any
        :param kwargs: kwargs
        :type kwargs: Any
        :return: The wrapper function around the original method.
        :rtype: Callable[..., Any]
        """

        @logger.catch()
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper function that logs the execution status (start, success, failure) of the decorated method.

            :param args: Positional arguments for the decorated method.
            :type args: Any
            :param kwargs: Keyword arguments for the decorated method.
            :type kwargs: Any
            :return: The return value of the decorated method.
            :rtype: Any
            """
            try:
                journal.info(f"Action Running {self.__name}")
                results = __method(*args, **kwargs)
                journal.success(f"Success Running {self.__name}")
                return results
            except Exception as error:
                journal.error(error)
                journal.error(f"Failure Running {self.__name}")
                raise

        return wrapper
