# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 03 03, 2024
"""

from typing import Any

from fairyland.framework.utils.generals.constants.constants import DefaultConstantUtils


class SingletonPattern:
    """
    Implements the Singleton pattern as a decorator class.

    This class ensures that a class is only instantiated once and
    returns the same instance on subsequent calls.
    """

    def __init__(self, __cls):
        """
        Initializes the decorator class.

        :param __cls:
        :type __cls:
        """
        self.__cls = __cls
        self.__instance = DefaultConstantUtils.dict()

    def __call__(self, *args: Any, **kwargs: Any):
        """
        On call, ensures the decorated class is instantiated only once
        and returns the singleton instance.

        :param args: args
        :type args: Any
        :param kwargs: kwargs
        :type kwargs: Any
        :return: Singleton instance
        :rtype: Any
        """
        if not self.__instance:
            self.__instance.update(__instance=self.__cls(*args, **kwargs))
            return self.__instance.get("__instance")
        else:
            return self.__instance.get("__instance")
