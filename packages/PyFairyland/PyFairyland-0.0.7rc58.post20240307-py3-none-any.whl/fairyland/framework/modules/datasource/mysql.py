# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 03 04, 2024
"""

from typing import Optional
import pymysql

from fairyland.framework.modules.journals.journal import journal
from fairyland.framework.core.abstracts.datesource.basic import DataSource


class MySQLModule(DataSource):

    def __init__(self, host: str = "127.0.0.1", port: int = 3306, user: str = "root", password: Optional[str] = None, database: Optional[str] = None):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database = database

        super().__init__()

    def connect(self):
        try:
            results = pymysql.connect(host=self.__host, port=self.__port, user=self.__user, password=self.__password, database=self.__database)
        except Exception as error:
            journal.error(error)
            raise
        return results

    def execute(self, query, params) -> None:
        self.cursor.execute(query, params)
