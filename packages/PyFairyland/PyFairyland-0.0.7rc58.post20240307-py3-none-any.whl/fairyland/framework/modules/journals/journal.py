# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 02 29, 2024
"""

import os
import sys
from loguru import logger

from fairyland.framework.constants.typing import TypeLogLevel
from fairyland.framework.modules.decorators.patterns import SingletonPattern
from fairyland.framework.constants.enum import EncodingFormat
from fairyland.framework.constants.enum import LogLevelFormat


@SingletonPattern
class JournalSingleton:
    """Log Module"""

    def __init__(self):
        self.__fairyland_logo = """
                                         _____       _               _                    _     _____        _                      
                                        |  ___|__ _ (_) _ __  _   _ | |  __ _  _ __    __| |   |  ___|_   _ | |_  _   _  _ __  ___  
                                        | |_  / _` || || '__|| | | || | / _` || '_ \  / _` |   | |_  | | | || __|| | | || '__|/ _ \ 
                                        |  _|| (_| || || |   | |_| || || (_| || | | || (_| |   |  _| | |_| || |_ | |_| || |  |  __/ 
                                        |_|   \__,_||_||_|    \__, ||_| \__,_||_| |_| \__,_|   |_|    \__,_| \__| \__,_||_|   \___| 
                                                              |___/                                                                 
"""

        self.__init_logger()

    def __init_logger(self):

        def write_log(_sink: str) -> None:
            with open(_sink, "w", encoding="UTF-8") as log_file:
                log_file.write(self.__fairyland_logo)
            return

        logger.remove()

        logger.add(
            sink="logs/service.log",
            rotation="10 MB",
            retention="60 days",
            # format="[{time:YYYY-MM-DD HH:mm:ss} | {elapsed} | {level:<8}]: {message}",
            format="[{time:YYYY-MM-DD HH:mm:ss} | {level:<8}]: {message}",
            compression="gz",
            encoding=EncodingFormat.default(),
            level=LogLevelFormat.default(),
            enqueue=True,
            colorize=False,
            backtrace=True,
        )

        logger.add(
            sink="logs/service.serialize.log",
            rotation="10 MB",
            retention="60 days",
            format="[{time:YYYY-MM-DD HH:mm:ss} | {level:<8}]: {message}",
            compression="gz",
            encoding=EncodingFormat.default(),
            level=LogLevelFormat.default(),
            enqueue=True,
            colorize=False,
            backtrace=True,
            serialize=True,
        )

        logger.add(
            sink="logs/service.debug.log",
            rotation="10 MB",
            retention="60 days",
            format="[{time:YYYY-MM-DD HH:mm:ss} | {level:<8}]: {message}",
            compression="gz",
            encoding=EncodingFormat.default(),
            level=LogLevelFormat.default_debug(),
            enqueue=True,
            colorize=False,
            backtrace=True,
        )

        logger.add(
            sink=sys.stdout,
            format="[<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level>]: <level>{message}</level>",
            level=LogLevelFormat.default_debug(),
            colorize=True,
        )

        write_log("logs/service.log")
        write_log("logs/service.debug.log")
        print(self.__fairyland_logo)

    def trace(self, msg, *args, **kwargs) -> None:
        """
        Inherits the trace method from loguru.
        :param msg: Log messages: String
        :param args: Tuple
        :param kwargs: Dict
        :return: loguru.logger.trace
        """
        return logger.trace(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs) -> None:
        """
        Inherits the debug method from loguru.logger
        :param msg: Debug Log messages: String
        :param args: Tuple
        :param kwargs: Dict
        :return: loguru.logger.debug
        :rtype: object
        """
        return logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs) -> None:
        """
        Inherits the info method from loguru.
        :param msg: Info Log messages: String
        :param args: Tuple
        :param kwargs: Dict
        :return: loguru.logger.info
        :rtype: object
        """
        return logger.info(msg, *args, **kwargs)

    def success(self, msg, *args, **kwargs) -> None:
        """
        Inherits the success method from loguru.
        :param msg: Success Log messages: String
        :param args: Tuple
        :param kwargs: Dict
        :return: loguru.logger.success
        """
        return logger.success(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs) -> None:
        """
        Inherits the warning method from loguru.
        :param msg: Warning Log messages: String
        :param args: Tuple
        :param kwargs: Dict
        :return: loguru.logger.warning
        """
        return logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs) -> None:
        """
        Inherits the error method from loguru.
        :param msg: Error Log messages: String
        :param args: Tuple
        :param kwargs: Dict
        :return: loguru.logger.error
        """
        return logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs) -> None:
        """
        Inherits the critical method from loguru.
        :param msg: Critical Log messages: String
        :param args: Tuple
        :param kwargs: Dict
        :return: loguru.logger.critical
        """
        return logger.critical(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs) -> None:
        """
        Inherits the exception method from loguru.

        :param msg: Exception Log messages: String
        :param args: Tuple
        :param kwargs: Dict
        :return: loguru.logger.exception
        """
        return logger.exception(msg, *args, **kwargs)


journal: JournalSingleton = JournalSingleton()
