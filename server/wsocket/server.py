# -*- coding: utf-8 -*-
"""
    Класс сервера
"""

import time
import json


from select import select
from socket import socket, getdefaulttimeout
from .handler import Handler
from .wsocket import WSocket, ConnStatus


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

        # Список периодически выполняемых задач
        self._eventually_tasks = []

        self._min_select_timeout = None

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

        if self._handlers.get('NEW_CONNECTION'):
            sock.on_connect(self._handlers.get('NEW_CONNECTION'))

        return sock


    def add_task(self, handler: Handler, timeout: int):
        """
            Добавление периодически выполняемой задачи
        """
        self._eventually_tasks.append([handler, timeout // 1000, time.time()])


    def on_accept(self, handler: Handler):
        """
            Событие при получении нового подключения
        """
        self._handlers['NEW_CONNECTION'] = handler


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

        print('Вызов обработчика(ИзСервера): ', handl.object, '. С параметрами: ', dict(**handl.kwargs))

        handl.call()


    def forever(self):
        """
            Запуск сервера
        """
        next_task = None

        while True:
            # Удаляем закрытые соединения
            self._clear_disconected()
            receive_sock, _, _ = select(self.connections, [], [], next_task)

            for sock in receive_sock:
                # Если поток чтения в серверном сокете не пуст
                # принимаем новое подключение
                if isinstance(sock, Server):
                    sock.accept()
                else:
                    sock.recv(1024)

            for task in self._eventually_tasks:
                if (task[2] + task[1]) > time.time():
                    task[0].call()
                    task[2] = time.time()

                if next_task:
                    next_task = task[1] if next_task > task[1] else next_task
                else:
                    next_task = task[1]


    def broadcast(self, data: bytes):
        """
            Массовая рассылка данных
        """
        for sock in self.connections:
            if not isinstance(sock, Server):
                sock.send(data)