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


class Task:
    def __init__(self, handler: Handler, timeout: int):
        self._handler = handler
        # Таймаут в мс
        self.timeout = timeout
        self.last_executed = time.time()
        super().__init__()


    def call(self):
        """
            Вызов обработчика
        """
        if (time.time() - self.last_executed) * 1000 > self.timeout:
            self._handler.call()
            # Записываем время последнего выполнения таски
            self.last_executed = time.time()

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
        handler.kwargs['event'] = self.__event()
        self._eventually_tasks.append(Task(handler, timeout))


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
        
        handl.kwargs['event'] = self.__event()
        handl.call()


    def broadcast(self, data: bytes):
        """
            Массовая рассылка данных
        """
        for sock in self.connections:
            if not isinstance(sock, Server):
                sock.send(data)


    def __event(self):
        """
            Обьект события
        """
        return {'Server': self}


    def forever(self):
        """
            Запуск сервера
        """
        # Фактическое время блокирования при чтении потока ввода
        # Из фактического времени вычитается время выполнения всех событий
        # получении и отправки данных, а так же время выполнения всех задач
        loop_timeout = 100

        # Макс.время блокирования при чтении потока ввода
        max_timeout = 10000

        while True:
            # Удаляем закрытые соединения
            self._clear_disconected()
            receive_sock, _, _ = select(self.connections, [], [], loop_timeout / 1000)

            # Время начала выполнения одной итерации
            loop_start_time = time.time()

            for sock in receive_sock:
                # Если поток чтения в серверном сокете не пуст
                # принимаем новое подключение
                if isinstance(sock, Server):
                    sock.accept()
                else:
                    sock.recv(1024)

            for task in self._eventually_tasks:
                task.call()

                if max_timeout > task.timeout:
                    max_timeout = task.timeout
            print('max_timeout: ', max_timeout)
            loop_timeout = max_timeout - (time.time() - loop_start_time) * 1000
            print(loop_timeout)
            if loop_timeout < 0:
                loop_timeout = 0
