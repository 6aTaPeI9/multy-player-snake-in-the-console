# -*- coding: utf-8 -*-
"""
    Константы
"""

class SockEvents:
    """
        События сокета
    """
    CONN_CLOSE = 'conn_close'


class ConnStatus:
    """
        Статусы соединения
    """
    # Статус ожидания рукопожатия
    CONNECTING = 0

    # активное соединение
    CONNECTED = 1

    # Ожидание чистого отключения
    CLOSING = 2

    # сокет отключен
    CLOSED = 3


class PingStatus:
    """
        Статусы пинга
    """
    # Пинг отрпавлен
    SENDED = 0

    # Понг получен
    RECIEVED = 1
