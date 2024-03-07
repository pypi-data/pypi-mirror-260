# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 03 03, 2024
"""

import functools


class SingletonPatternMetaclass(type):

    @functools.lru_cache(maxsize=0)
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "__instance"):
            setattr(cls, "__instance", super().__call__(*args, **kwargs))
            return getattr(cls, "__instance")
        else:
            return getattr(cls, "__instance")
