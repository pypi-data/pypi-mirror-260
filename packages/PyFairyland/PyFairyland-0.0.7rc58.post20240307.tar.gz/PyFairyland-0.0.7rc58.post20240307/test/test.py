# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 02 29, 2024
"""
import sys
import warnings

from fairyland.framework.modules.journals.journal import journal
from fairyland.framework.core.abstracts.enumerate.enumerate import BaseEnum
from fairyland.framework.constants.enum import DateTimeFormat
from fairyland.framework.modules.exceptions import ProjectError
from fairyland.framework.utils.generals.constants.constants import DefaultConstantUtils
from fairyland.framework.utils.generals.datetime.datetime import DatetimeUtils
from fairyland.framework.utils.publish.package import PackageInfo
from fairyland.framework.utils.generals.decoder.decoder import DecoderUtils
from fairyland.framework.utils.generals.constants.constants import EncodingConstantUtils
from fairyland.framework.modules.decorators.patterns.design import SingletonPattern
from fairyland.framework.core.abstracts.metaclass.metaclass import SingletonPatternMetaclass
from fairyland.framework.modules.decorators.methods.method import MethodTipsDecorator
from fairyland.framework.modules.decorators.methods.method import MethodTimingDecorator
from fairyland.framework.modules.datasource.mysql import MySQLModule
from fairyland.framework.modules.static.requests.requests import Requests
from fairyland.framework.utils.tools.requests import RequestsUtils

from fairyland.framework.test.simulation import TestReturn

sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")


class Test:

    @classmethod
    @MethodTimingDecorator
    @MethodTipsDecorator("Test Main Method.")
    def run(cls) -> None:
        cls.test_1()
        cls.test_2()
        cls.test_3()
        cls.test_4()
        # cls.test_5()
        # cls.test_6()
        # cls.test_7()
        # cls.test_8()
        # cls.test_9()
        cls.test_10()
        cls.test_11()
        cls.test_12()
        cls.test_13()
        cls.test_14()
        return

    @classmethod
    def test_1(cls):
        class DatetimeEnum(BaseEnum):
            data = {"a": 1}

        journal.debug(f"测试枚举继承方法: {DatetimeEnum.values()}")

    @classmethod
    def test_2(cls):
        journal.debug(f"日期时间格式化枚举成员: {DateTimeFormat.members()}")
        journal.debug(f"日期时间格式化枚举字段: {DateTimeFormat.names()}")
        journal.debug(f"日期时间格式化枚举值: {DateTimeFormat.values()}")
        journal.debug(f"日期时间格式化: {DateTimeFormat.datetime_cn.value}")

    @classmethod
    def test_3(cls):
        journal.debug(f"当前时间时间戳: {DatetimeUtils.normtimestamp()}")
        a = DefaultConstantUtils.dict()
        a.update(测试时间=DatetimeUtils.normdatetime_to_str())
        journal.debug(f"测试字典: {a}")

    @classmethod
    def test_4(cls):
        journal.debug(f"包名: {PackageInfo.name}")
        journal.debug(f"版本号: {PackageInfo.version}")

    @classmethod
    def test_5(cls):
        b_str = b"\xd3\xd0\xb9\xd8\xc4\xb3\xb8\xf6\xc3\xfc\xc1\xee\xb5\xc4\xcf\xea\xcf\xb8\xd0\xc5\xcf\xa2\xa3\xac\xc7\xeb\xbc\xfc\xc8\xeb HELP \xc3\xfc\xc1\xee\xc3\xfb\r\nASSOC"
        a = DecoderUtils.decode_binary_string(b_str, encodings=EncodingConstantUtils.encodings())
        journal.debug(f"解码: {a}")

    @classmethod
    def test_6(cls):
        string = "big5, big5-hkscs, cesu-8, euc-jp, euc-kr, gb18030, gb2312, gbk, ibm-thai, ibm00858, ibm01140, ibm01141, ibm01142, ibm01143, ibm01144, ibm01145, ibm01146, ibm01147, ibm01148, ibm01149, ibm037, ibm1026, ibm1047, ibm273, ibm277, ibm278, ibm280, ibm284, ibm285, ibm290, ibm297, ibm420, ibm424, ibm437, ibm500, ibm775, ibm850, ibm852, ibm855, ibm857, ibm860, ibm861, ibm862, ibm863, ibm864, ibm865, ibm866, ibm868, ibm869, ibm870, ibm871, ibm918, iso-2022-cn, iso-2022-jp, iso-2022-jp-2, iso-2022-kr, iso-8859-1, iso-8859-13, iso-8859-15, iso-8859-2, iso-8859-3, iso-8859-4, iso-8859-5, iso-8859-6, iso-8859-7, iso-8859-8, iso-8859-9, jis_x0201, jis_x0212-1990, koi8-r, koi8-u, shift_jis, tis-620, us-ascii, utf-16, utf-16be, utf-16le, utf-32, utf-32be, utf-32le, utf-8, windows-1250, windows-1251, windows-1252, windows-1253, windows-1254, windows-1255, windows-1256, windows-1257, windows-1258, windows-31j, x-big5-hkscs-2001, x-big5-solaris, x-euc-jp-linux, x-euc-tw, x-eucjp-open, x-ibm1006, x-ibm1025, x-ibm1046, x-ibm1097, x-ibm1098, x-ibm1112, x-ibm1122, x-ibm1123, x-ibm1124, x-ibm1166, x-ibm1364, x-ibm1381, x-ibm1383, x-ibm300, x-ibm33722, x-ibm737, x-ibm833, x-ibm834, x-ibm856, x-ibm874, x-ibm875, x-ibm921, x-ibm922, x-ibm930, x-ibm933, x-ibm935, x-ibm937, x-ibm939, x-ibm942, x-ibm942c, x-ibm943, x-ibm943c, x-ibm948, x-ibm949, x-ibm949c, x-ibm950, x-ibm964, x-ibm970, x-iscii91, x-iso-2022-cn-cns, x-iso-2022-cn-gb, x-iso-8859-11, x-jis0208, x-jisautodetect, x-johab, x-macarabic, x-maccentraleurope, x-maccroatian, x-maccyrillic, x-macdingbat, x-macgreek, x-machebrew, x-maciceland, x-macroman, x-macromania, x-macsymbol, x-macthai, x-macturkish, x-macukraine, x-ms932_0213, x-ms950-hkscs, x-ms950-hkscs-xp, x-mswin-936, x-pck, x-sjis_0213, x-utf-16le-bom, x-utf-32be-bom, x-utf-32le-bom, x-windows-50220, x-windows-50221, x-windows-874, x-windows-949, x-windows-950, x-windows-iso2022jp"
        string_tuple = tuple([item for item in string.replace(" ", "").split(",")])
        journal.debug(f"字符集: {string_tuple}")
        journal.debug(f"字符集数量: {string_tuple.__len__()}")

    @classmethod
    def test_7(cls):
        a = A()
        aa = A()
        if a == aa:
            journal.debug(True)
        else:
            journal.debug(False)

    @classmethod
    def test_8(cls):
        b = B()
        bb = B()
        if b == bb:
            journal.debug(True)
        else:
            journal.debug(False)

    @classmethod
    def test_9(cls):
        pass
        db = MySQLModule(host="mapping.fairy.host", port=51001, user="austin", password="Austin.pwd:112#.", database="public_db_test")
        query_tuple = ("select version();", "select * from myapp_myinfo where nid > %s;")
        param_tuple = (None, 0)
        a = db.operate(query_tuple, param_tuple)
        journal.debug(a)

    @classmethod
    def test_10(cls):
        response = Requests.get(
            url="https://api.threatbook.cn/v3/scene/ip_reputation",
            params={"apikey": "25702dcf45db4f4c95dac98cabe0b6f9", "resource": "159.203.93.255"},
        )
        # response = TestReturn.Threat.ip_reputation()
        journal.debug(f"Response: {response}")
        journal.debug(f"Type: {type(response)}")

    @classmethod
    def test_11(cls):
        journal.debug(f"当前时间戳: {DatetimeUtils.normtimestamp()}")
        # 1709636127
        # journal.debug(f"{DatetimeUtils.timestamp_to_datetime(1709626679000)}")
        # journal.debug(f"{DatetimeUtils.timestamp_to_datetime(1709636127)}")
        journal.debug(f"{DatetimeUtils.timestamp_to_datetime(1709626749)}")
        journal.debug(f"{DatetimeUtils.timestamp_to_datetime(1709626758)}")

    @classmethod
    def test_12(cls):
        journal.debug(f"{RequestsUtils.user_agent()}, type: {type(RequestsUtils.user_agent())}")
        journal.debug(f"{RequestsUtils.chrome_user_agent()}")
        journal.debug(f"{RequestsUtils.edge_user_agent()}")
        journal.debug(f"{RequestsUtils.firefox_user_agent()}")
        journal.debug(f"{RequestsUtils.safari_user_agent()}")

    @classmethod
    def test_13(cls):
        # a = Requests.get("https://baidu.com")
        b = Requests.get("https://douban.api.fairy.host")
        # b = Requests.get("https://ttime.v1.timerecord.cn/asdqwefac")
        # journal.debug(f"Type a: {type(a)}")
        journal.debug(f"b: {b}, Type b: {type(b)}")
        if isinstance(b, dict):
            journal.debug(f"b -> code: {b.get('code')}")

    @classmethod
    def test_14(cls):
        for i in range(100, 3662, 100):
            journal.debug(i)
            break


@SingletonPattern
class A: ...


class B(metaclass=SingletonPatternMetaclass): ...


if __name__ == "__main__":
    Test.run()
