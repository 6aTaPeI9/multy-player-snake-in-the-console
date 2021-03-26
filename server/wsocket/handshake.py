# -*- coding: utf-8 -*-
"""
    Модуль содержит поддержку 
"""

import base64
import hashlib
import binascii

from tools import get_as_list
from .exceptions import (
    InvalidHeaderValue,
    InvalidHttpHeader,
    HeaderNotFound,
    TooMuchHeader
)

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


def get_req_header(header: dict, key: str):
    """
        Получение обязательного заголовка
    """
    hdr = get_as_list(header, key)

    if not hdr:
        raise HeaderNotFound(key)

    return hdr


def validate_request(headers: dict) -> str:
    """
        Валидация входящего запроса
    """

    # Валидируем заголовок Connection.
    # Их может быть больше одного, но все они
    # должны быть равны строке <upgrade>

    connection = get_req_header(headers, 'Connection')

    for value in connection:
        if value.lower() == "upgrade":
            continue

        raise InvalidHeaderValue(name='Connection', value=value)

    # Валидация заголовка Upgrade
    upgrade = get_req_header(headers, 'Upgrade')

    if len(upgrade) != 1:
        raise TooMuchHeader('Upgrade')

    if upgrade[0].lower() != "websocket":
        raise InvalidHeaderValue(name='Upgrade', value=upgrade[0])

    # Валидация заголовка Sec-WebSocket-Key
    s_w_key = get_req_header(headers, 'Sec-WebSocket-Key')

    if len(s_w_key) != 1:
        raise TooMuchHeader('Sec-WebSocket-Key')

    s_w_key = s_w_key[0]

    try:
        raw_key = base64.b64decode(s_w_key.encode(), validate=True)
    except binascii.Error:
        raise InvalidHeaderValue('Sec-WebSocket-Key', s_w_key)

    if len(raw_key) != 16:
        raise InvalidHeaderValue('Sec-WebSocket-Key', s_w_key)

    # Валидация заголовка Sec-WebSocket-Version
    s_w_version = get_req_header(headers, 'Sec-WebSocket-Version')

    if not s_w_version:
        raise HeaderNotFound('Sec-WebSocket-Version')

    if len(s_w_version) != 1:
        raise TooMuchHeader('Sec-WebSocket-Version')

    if s_w_version[0] != "13":
        raise InvalidHeaderValue('Sec-WebSocket-Version', s_w_version)

    # Валидация заголовка Host
    if not get_req_header(headers, 'Host'):
        HeaderNotFound('Host')

    return s_w_key