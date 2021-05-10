# -*- coding: utf-8 -*-
"""
    Класс сервера
"""

import json


from select import select
from handler import Handler
from socket import socket, getdefaulttimeout
from .wsocket import WSocket, ConnStatus


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

        # Обработчики для событий
        self._handlers = {}

        super().__init__(*args, **kwargs)


    def accept(self, *args, **kwargs):
        """
            Обертка над методом ожидания новых подключений
        """
        fd, _ = self._accept()
        sock = WSocket(self.family, self.type, self.proto, fileno=fd)

        if getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)

        self.connections.append(sock)

        return sock


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


    def _execute_handler(self, event: str):
        """
            Выполнение обработчика, если он есть.
        """

        handl = self._handlers.get(event)

        if not handl:
            return

        # print('Вызов обработчика(ИзСервера): ', handl.object, '. С параметрами: ', dict(**handl.kwargs), ' | DATA: ', data)

        handl.call()


    def on_connection(self):
        pass


    def forever(self):
        """
            Запуск сервера
        """
        while True:
            # Удаляем закрытые соединения
            self._clear_disconected()
            receive_sock, _, _ = select(self.connections, [], [], SELECT_TIMEOUT)

            for sock in receive_sock:
                # Если поток чтения в серверном сокете не пуст
                # принимаем новое подключение
                if isinstance(sock, Server):
                    new_conn = sock.accept()
                else:
                    data = sock.recv(1024)
