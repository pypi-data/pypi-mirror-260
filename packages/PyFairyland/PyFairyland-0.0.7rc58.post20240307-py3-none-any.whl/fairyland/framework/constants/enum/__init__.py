# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 03 04, 2024
"""

from typing import Any

from fairyland.framework.core.abstracts.enumerate.enumerate import StringEnum
from fairyland.framework.core.abstracts.enumerate.enumerate import BaseEnum


class DateTimeFormat(StringEnum):
    """Datetime"""

    DATE = date = "%Y-%m-%d"
    TIME = time = "%H:%M:%S"
    DATETIME = datetime = "%Y-%m-%d %H:%M:%S"

    DATE_CN = date_cn = "%Y年%m月%d日"
    TIME_CH = time_cn = "%H时%M分%S秒"
    DATETIME_CN = datetime_cn = "%Y年%m月%d日 %H时%M分%S秒"

    @classmethod
    def default(cls) -> str:
        return cls.DATETIME.value

    @classmethod
    def default_cn(cls) -> str:
        return cls.DATETIME_CN.value


class EncodingFormat(BaseEnum):
    """Encoding"""

    UTF_8 = utf_8 = "UTF-8"
    GBK = gbk = "GBK"
    GB2312 = gb2312 = "GB2312"
    GB18030 = gb18030 = "GB18030"

    @classmethod
    def default(cls) -> str:
        return cls.UTF_8.value


class LogLevelFormat(BaseEnum):
    """Log Level"""

    TRACE = trace = "TRACE"
    DEBUG = debug = "DEBUG"
    INFO = info = "INFO"
    SUCCESS = success = "SUCCESS"
    WARNING = warning = "WARNING"
    ERROR = error = "ERROR"
    CRITICAL = critical = "CRITICAL"

    @classmethod
    def default(cls) -> str:
        return cls.INFO.value

    @classmethod
    def default_debug(cls) -> str:
        return cls.TRACE.value
