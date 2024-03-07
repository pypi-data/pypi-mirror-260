# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 03 05, 2024
"""
from typing import Optional, Dict, Union, Any

import requests

from fairyland.framework.modules.journals.journal import journal
from fairyland.framework.utils.tools.requests import RequestsUtils


class Requests:

    @staticmethod
    def get(
        url: str,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        verify: bool = False,
        timeout: int = 10,
    ) -> Union[Dict[str, Any], str]:
        if not params:
            params = dict()
        if not headers:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": RequestsUtils.user_agent(),
                # "Accept": "application/json",
                # "Accept-Encoding": "gzip, deflate, br",
                # "Connection": "keep-alive",
                # "Accept-Language": "en-US,en;q=0.9",
                # "Cache-Control": "no-cache",
                # "Pragma": "no-cache",
                # "Upgrade-Insecure-Requests": "1",
                # "Sec-Fetch-Dest": "document",
                # "Sec-Fetch-Mode": "navigate",
                # "Sec-Fetch-Site": "none",
                # "Sec-Fetch-User": "?1",
                # "Sec-GPC": "1",
                # "TE": "trailers",
            }
        try:
            response = requests.request(
                method="GET",
                url=url,
                params=params,
                headers=headers,
                cookies=cookies,
                verify=verify,
                timeout=timeout,
            )
            if response.status_code == 200:
                try:
                    results = response.json()
                except Exception as error:
                    journal.warning(f"Failed to parse response as JSON, {error}")
                    results = response.text
            else:
                results = response.text
        except Exception as error:
            journal.error(error)
            raise Exception("Failed to get response")

        return results
