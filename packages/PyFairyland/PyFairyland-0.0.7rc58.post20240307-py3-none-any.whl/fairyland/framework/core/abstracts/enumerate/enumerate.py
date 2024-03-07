# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 02 29, 2024
"""
from typing import Tuple, Any, Iterable, Optional

from enum import Enum


class BaseEnum(Enum):
    """
    Enum Base Class
    """

    @classmethod
    def default(cls) -> Any:
        """
        Abstract method to be implemented in subclasses.
        Returns the default value for the Enum.
        :return: Default value for the Enum.
        :rtype: Any
        """
        raise NotImplementedError("Implement it in a subclass.")

    @classmethod
    def members(cls, exclude_enums: Optional[Iterable[str]] = None, only_value: bool = False) -> Tuple[Any, ...]:
        """
        Returns a tuple with all members of the Enum.
        :param exclude_enums: List of members to exclude from the result.
        :type exclude_enums: Iterable
        :param only_value: If True, returns only the values of the members.
        :type only_value: bool
        :return: Tuple with all members of the Enum.
        :rtype: tuple
        """
        member_list = list(cls)
        if exclude_enums:
            member_list = [member for member in member_list if member not in exclude_enums]
        if only_value:
            member_list = [member.value for member in member_list]
        return tuple(member_list)

    @classmethod
    def names(cls) -> Tuple[str, ...]:
        """
        Returns a tuple with the names of all members of the Enum.
        :return: Tuple with the names of all members of the Enum.
        :rtype: tuple
        """
        return tuple(cls._member_names_)

    @classmethod
    def values(cls, exclude_enums: Optional[Iterable[str]] = None) -> Tuple[Any, ...]:
        """
        Returns a tuple with the values of all members of the Enum.
        :param exclude_enums: List of members to exclude from the result.
        :type exclude_enums: Iterable
        :return: Tuple with the values of all members of the Enum.
        :rtype: tuple
        """
        return cls.members(exclude_enums, True)


class StringEnum(str, BaseEnum): ...


class IntegerEnum(int, BaseEnum): ...
