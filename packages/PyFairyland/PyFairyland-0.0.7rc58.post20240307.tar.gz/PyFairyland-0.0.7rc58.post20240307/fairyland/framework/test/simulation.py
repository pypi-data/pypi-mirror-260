# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 03 05, 2024
"""


class TestReturn:

    class Threat:

        @staticmethod
        def ip_reputation():
            return {
                "data": {
                    "159.203.93.255": {
                        "severity": "info",
                        "judgments": ["IDC"],
                        "tags_classes": [],
                        "basic": {
                            "carrier": "digitalocean.com",
                            "location": {
                                "country": "United States",
                                "province": "New York",
                                "city": "New York City",
                                "lng": "-74.006",
                                "lat": "40.713",
                                "country_code": "US",
                            },
                        },
                        "asn": {"rank": 2, "info": "DIGITALOCEAN-ASN - DigitalOcean, LLC, US", "number": 14061},
                        "scene": "",
                        "confidence_level": "low",
                        "is_malicious": False,
                        "update_time": "2016-05-17 20:18:33",
                    }
                },
                "response_code": 0,
                "verbose_msg": "OK",
            }
