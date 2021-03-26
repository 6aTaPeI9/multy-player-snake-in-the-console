# -*- coding: utf-8 -*-
"""
    Модуль содержит поддержку 
"""

import base64
import hashlib

from tools import get_as_list
from .exceptions import InvalidHeaderValue, InvalidHttpHeader

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def build_response(headers: dict, key: str) -> None:
    """
    """
    headers["Upgrade"] = "websocket"
    headers["Connection"] = "Upgrade"
    headers["Sec-WebSocket-Accept"] = accept(key)


def accept(key: str) -> str:
    sha1 = hashlib.sha1((key + GUID).encode()).digest()
    return base64.b64encode(sha1).decode()


# def validate_request(headers: dict) -> str:
#     """
#         Валидация входящего запроса
#     """

#     # Валидируем заголовок Connection.
#     # Их может быть больше одного, но все они
#     # должны быть равны строке <upgrade>
#     for value in get_as_list(headers, 'Connection'):
#         if value.lower() == "upgrade":
#             continue

#         raise InvalidHeaderValue(name='Connection', value=value)

#     upgrade = get_as_list(headers, 'Upgrade')

#     if len(upgrade) != 1:
#         raise InvalidHttpHeader('Too many Upgrade headers')

#     if upgrade[0].lower() != "websocket":
#         raise InvalidHeaderValue(name='Upgrade', value=upgrade[0])

#     try:
#         s_w_key = headers["Sec-WebSocket-Key"]
#     except KeyError:
#         raise InvalidHeader("Sec-WebSocket-Key")
#     except MultipleValuesError:
#         raise InvalidHeader(
#             "Sec-WebSocket-Key", "more than one Sec-WebSocket-Key header found"
#         )

#     try:
#         raw_key = base64.b64decode(s_w_key.encode(), validate=True)
#     except binascii.Error:
#         raise InvalidHeaderValue("Sec-WebSocket-Key", s_w_key)
#     if len(raw_key) != 16:
#         raise InvalidHeaderValue("Sec-WebSocket-Key", s_w_key)

#     try:
#         s_w_version = headers["Sec-WebSocket-Version"]
#     except KeyError:
#         raise InvalidHeader("Sec-WebSocket-Version")
#     except MultipleValuesError:
#         raise InvalidHeader(
#             "Sec-WebSocket-Version", "more than one Sec-WebSocket-Version header found"
#         )

#     if s_w_version != "13":
#         raise InvalidHeaderValue("Sec-WebSocket-Version", s_w_version)

#     return s_w_key