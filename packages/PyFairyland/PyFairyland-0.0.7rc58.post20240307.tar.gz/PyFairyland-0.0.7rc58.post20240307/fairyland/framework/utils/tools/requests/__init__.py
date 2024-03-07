# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 03 06, 2024
"""

from fake_useragent import UserAgent


class RequestsUtils:
    """Requests utils"""

    @staticmethod
    def user_agent() -> str:
        return UserAgent().random

    @staticmethod
    def chrome_user_agent() -> str:
        return UserAgent().chrome

    @staticmethod
    def edge_user_agent() -> str:
        return UserAgent().edge

    @staticmethod
    def firefox_user_agent() -> str:
        return UserAgent().firefox

    @staticmethod
    def safari_user_agent():
        return UserAgent().safari
