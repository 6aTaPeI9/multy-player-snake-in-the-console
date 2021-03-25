# -*- coding: utf-8 -*-
"""
    Модуль содержит обертку над стандартным сокетом с
    частичной реализацией протокола websocket 13 версии
"""

import socket


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


class WSocket(socket.socket):
    def __init__(self, *args, **kwargs):
        """
            Инциализация сокета с частичной поддержкой
            протокола WebSocket v13
        """
        super().__init__(*args, **kwargs)
        
        # Устанавливаем соединение в статус установки соединения.
        self.status = ConnStatus.CONNECTING

        #
        self.next_ping = 

        #
        self.ping_status = 

        return


    def recv(self, *args, **kwargs):
        """
            Обертка над методом ожидания новых данных
        """
        dt = super().recv(*args, **kwargs)
        return dt


    def accept(self, *args, **kwargs):
        """
            Обертка над методом ожидания новых подключений
        """
        fd, addr = self._accept()
        sock = WSocket(self.family, self.type, self.proto, fileno=fd)

        if socket.getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)

        return sock, addr


    def fileno(self):
        """
            Обработчик получения файлового дескриптора сокета.
        """


