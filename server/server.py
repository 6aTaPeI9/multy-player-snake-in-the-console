# -*- coding: utf-8 -*-
"""
    Класс сервера
"""

from room import Room
from player import Player

from select import select
from socket import socket, getdefaulttimeout
from wsocket.wsocket import WSocket, ConnStatus


SELECT_TIMEOUT = 1

class Server(socket):

    def __init__(self, *args, **kwargs):
        """
            Инициализация сервера
        """
        # Список подключений.
        # Сам сервер так же добавляем в список
        # чтобы он сам себя опрашивал на входящие подключения
        self.connections = [self]
        self.status = ConnStatus.CONNECTED

        super().__init__(*args, **kwargs)


    def accept(self, *args, **kwargs):
        """
            Обертка над методом ожидания новых подключений
        """
        fd, addr = self._accept()
        sock = WSocket(self.family, self.type, self.proto, fileno=fd)

        if getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)

        self.connections.append(sock, addr)


    def _clear_disconected(self):
        """
            Удаление отключенных сокетов
        """
        disconected = []
        for sock in self.connections:
            if not sock.status == ConnStatus.CLOSED:
                continue

            disconected.append(sock)

        for sock in disconected:
            self.connections.remove(sock)

        return


    def forever(self):
        """
            Запуск сервера
        """
        while True:
            # Удаляем закрытые соединения
            self._clear_disconected()

            receive_sock, _, _ = select(self.connect, [], [], SELECT_TIMEOUT)

            for sock in receive_sock:
                # Если поток чтения в серверном сокете не пуст
                # принимаем новое подключение
                if isinstance(Server):
                    sock.accept()
                else:
                    sock.recv()


def register_player_handlers(sock, room: Room, player: Player):
    """
        Установка стандартных обработчиков для каждого игрока
    """
    sock.