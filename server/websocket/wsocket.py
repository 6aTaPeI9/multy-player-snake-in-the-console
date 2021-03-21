"""
    Модуль содержит обертку над стандартным сокетом с
    частичной реализацией протокола websocket 13 версии
"""

import socket


class WSocket(socket.socket):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass


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
