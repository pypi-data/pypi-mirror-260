# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 03 04, 2024
"""

from abc import abstractmethod
from typing import Iterable, Optional, Tuple, Union, List, Set, Dict, Any
from datetime import datetime

from fairyland.framework.constants.typing import TypeSQLConnection
from fairyland.framework.constants.typing import TypeSQLCursor
from fairyland.framework.modules.journals.journal import journal


class DataSource:

    def __init__(self) -> None:

        self.__init_connect()

        return

    @abstractmethod
    def connect(self):

        raise NotImplemented

    def __connect(self) -> TypeSQLCursor:

        return self.connect()

    def __init_connect(self) -> None:

        self.__connection: TypeSQLConnection = self.__connect()
        self.cursor: TypeSQLCursor = self.__connection.cursor()

        return

    def __close_cursor(self) -> None:

        if self.cursor:
            self.cursor.close()
            self.cursor = None
            journal.warning("Database has disconnected the cursor.")

        return

    def __close_connection(self) -> None:

        self.__close_cursor()

        if self.__connection:
            self.__connection.close()
            self.__connection = None

        return

    def __reconnect(self):
        if not self.__connection:
            self.__connection = self.__connect()
            journal.warning("Database has been reconnected.")

        if not self.cursor:
            self.cursor = self.__connection.cursor()
            journal.warning("Database cursor has been reconnected.")
        else:
            journal.warning("The database and cursor are already connected.")

    @abstractmethod
    def execute(self, query, params) -> None:
        raise NotImplemented

    def __operate(self, sqls: Union[str, Iterable], params: Optional[Iterable] = None) -> Tuple:
        try:
            self.__reconnect()
            if isinstance(sqls, str):
                journal.trace(f"SQL >> {sqls} | Params: {params}")
                self.execute(query=sqls, params=params)
                results = self.cursor.fetchall()
            elif isinstance(sqls, (list, tuple)):
                tmp_list = []
                for sql, param in zip(sqls, params):
                    journal.trace(f"SQL >> {sql} | Params: {param}")
                    self.execute(query=sql, params=param)
                    tmp_list.append(self.cursor.fetchall())
                results = tuple(tmp_list)
            else:
                raise TypeError("Wrong SQL statements type.")
            self.__connection.commit()
        except Exception as error:
            journal.warning("Failed to execute the rollback after an error occurred.")
            self.__connection.rollback()
            journal.error(f"Error occurred during SQL operation: {error}")
            raise
        finally:
            self.__close_cursor()
        return results

    def operate(self, query: Union[str, Iterable], params: Optional[Iterable] = None) -> Tuple:

        return self.__operate(query, params)

    def close(self):

        self.__close_connection()
