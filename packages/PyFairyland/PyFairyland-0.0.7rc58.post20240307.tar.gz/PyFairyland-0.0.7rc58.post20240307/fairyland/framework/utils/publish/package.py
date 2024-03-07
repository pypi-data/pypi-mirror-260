# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 02 29, 2024
"""
from typing import Dict, Any
from datetime import datetime
import yaml
import os

from fairyland.framework.modules.journals.journal import journal


class PackageConfig:
    """package config"""

    @staticmethod
    def read_config() -> Dict[str, Any]:
        _path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conf", "publish.yaml")
        try:
            with open(_path, mode="r") as publish_file:
                publish_config = yaml.safe_load(publish_file)
        except Exception as error:
            journal.error(error)
            raise
        return publish_config


class PackageInfo:
    """InstallPackageSource"""

    # package name
    name = "PyFairyland"

    __config = PackageConfig.read_config()
    # version
    __major_number = __config.get("major")
    __sub_number = __config.get("sub")
    __stage_number = __config.get("stage")
    __revise_number = __config.get("revise")

    if __revise_number.__str__().__len__() < 5:
        __nbit = 5 - __revise_number.__str__().__len__()
        __revise_number = "".join((("0" * __nbit), __revise_number.__str__()))
    else:
        __revise_number = __revise_number.__str__()
    __date_number = datetime.now().date().__str__().replace("-", "")
    __revise_after = "-".join((__revise_number.__str__(), __date_number))

    # version: (release_version, test_version, alpha_version, beta_version)
    __version = __config.get("version")
    __release_version = ".".join((__major_number.__str__(), __sub_number.__str__(), __stage_number.__str__()))
    if __version == "release":
        version = __release_version
    elif __version == "test":
        version = ".".join((__release_version, "".join(("rc", __revise_after))))
    elif __version == "alpha":
        version = ".".join((__release_version, "".join(("alpha", __revise_after))))
    elif __version == "beta":
        version = ".".join((__release_version, "".join(("beta", __revise_after))))
    else:
        version = ".".join((__release_version, "".join(("rc", __revise_after))))
