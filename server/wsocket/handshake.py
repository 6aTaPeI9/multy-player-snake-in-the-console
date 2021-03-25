# -*- coding: utf-8 -*-
"""
    Модуль содержит поддержку 
"""

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def build_response(headers: Headers, key: str) -> None:
    """
    Build a handshake response to send to the client.

    Update response headers passed in argument.

    :param headers: response headers
    :param key: comes from :func:`check_request`

    """
    headers["Upgrade"] = "websocket"
    headers["Connection"] = "Upgrade"
    headers["Sec-WebSocket-Accept"] = accept(key)