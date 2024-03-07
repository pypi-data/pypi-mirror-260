# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 02 29, 2024
"""


class ProjectError(Exception):
    def __init__(self, message: str = "Internal error."):
        self.__prompt = f"{self.__class__.__name__}: {message}"

    def __str__(self):
        return self.__prompt


class ParameterError(ProjectError):
    def __init__(self, message: str = "Invalid parameter."):
        super().__init__(message=message)


class ReadFileError(ProjectError):
    def __init__(self, message: str = "Reading file error."):
        super().__init__(message=message)


class DataSourceError(ProjectError):
    def __init__(self, message: str = "Data source error."):
        super().__init__(message=message)


class SQLExecutionError(ProjectError):

    def __init__(self, message: str = "SQL exection error."):
        super().__init__(message=message)
