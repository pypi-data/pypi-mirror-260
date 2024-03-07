# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 02 29, 2024
"""
from typing import List, Optional, Iterable, Dict, Any

from fairyland.framework.modules.journals.journal import journal
from fairyland.framework.utils.generals.constants.constants import DefaultConstantUtils
from fairyland.framework.modules.decorators.patterns.design import SingletonPattern


class DecoderUtils:

    @classmethod
    def decode_binary_string(
        cls,
        binary_data: str,
        encodings: Optional[Iterable[str]] = None,
        excludes: Optional[Iterable[str]] = None,
    ) -> Dict[str, Any]:
        """
        Attempts to decode a binary string (hexadecimal format or byte sequence) into a human-readable string using a list of encodings.
        This method is useful for decoding data that might be encoded in different character sets.

        :param binary_data: The binary data to decode, either as a hexadecimal string or a byte sequence.
        :type binary_data: str
        :param encodings: An optional list of string encodings to try decoding the binary data with.
                            If not provided, a default list of encodings is used.
                            This allows for customization of the decoding process.
        :type encodings: Optional[Iterable[str]]
        :param excludes: An optional list of encodings to exclude from the decoding process.
                            This is useful when certain encodings are known to cause issues or are not relevant.
        :type excludes: Optional[Iterable[str]]
        :return: A dictionary where each key is an encoding that successfully decoded the binary data and the corresponding value is the decoded string.
                    If no encoding was successful, the dictionary will be empty.
        :rtype: Dict[str, Any]
        """
        default_encodings = ("utf-8", "gb2312", "gbk", "iso-8859-1", "utf-16", "ascii")
        if encodings:
            default_encoding_list = list(default_encodings)
            default_encoding_list.extend([encoding.upper() for encoding in encodings])
        encodings = tuple(set([encoding.upper() for encoding in default_encoding_list]))
        if excludes:
            excludes = tuple([encoding.upper() for encoding in excludes])
            encodings = tuple(set([encoding.upper() for encoding in default_encoding_list if encoding.upper() not in excludes]))
        if isinstance(binary_data, str):
            try:
                binary_data = bytes.fromhex(binary_data)
            except ValueError:
                raise ValueError("The provided data format is incorrect. Please provide a valid hexadecimal encoded string or byte sequence.")
        results = DefaultConstantUtils.dict()
        error_encodings = DefaultConstantUtils.list()
        for encoding in encodings:
            try:
                decoded_data = binary_data.decode(encoding)
                journal.debug(f"Decode successful using {encoding}: {repr(decoded_data)}")
                results.update({encoding: decoded_data})
            except UnicodeDecodeError:
                continue
            except LookupError:
                error_encodings.append(encoding)
        error_encodings = tuple(error_encodings)
        if not results:
            journal.warning(f"Encodeing format: {', '.join(encodings)}")
            journal.warning("Unable to decode, tried all predefined encoding formats.")
        if error_encodings:
            journal.warning(f"Wrong encoding: {', '.join(error_encodings)}")
        return results
