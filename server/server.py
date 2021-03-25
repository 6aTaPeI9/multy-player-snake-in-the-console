# -*- coding: utf-8 -*-
"""
    Модуль содержит основной код серверной части.
"""
__author__ = "6aTaPeI9"

import time
import uuid
import socket
import threading
import traceback

from singleton import Singleton

STEPS_QUEUE = {}

        self.connections = {}
        self.socket = None
        self.port = port
        self.address = address
        self.open_sock()


    def open_sock(self):
        """
            Метод открывает сокет
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.address, self.port))
        except Exception as ex:
            self.close_sock()
            print('Во время открытия сокета произошла ошибка.')
            raise ex


    def send_msg(self, user_uuid: uuid.UUID, msg: str):
        """
            Метод отправляет текстовое сообщение указанному пользователю
        """
        user = self.connections.get(user_uuid)

        if not user:
            return

        try:
            user.con.send(msg.encode())
            user.ex_count = 0
        except Exception as ex:
            print(
                f'Во время отправки сообщения пользователю {user.login} '\
                f'прозоишла ошибка: {str(ex)}'
            )
            user.ex_count += 1
            if user.ex_count >= 3:
                print(f'Пользователь {user.login} отключен.')
                user.con.close()
                del self.connections[user_uuid]


    def process_exception(self, user_uuid: uuid.UUID, ex: Exception):
        """
            Метод обрабатывает упавшее исключение и принимает решение
            об отключении пользователя
        """
        pass


    def close_sock(self):
        """
            Метод закрывает сокет
        """
        if self.socket:
            self.socket.close()


    def listen_connections(self, backlog: int = 5):
        """
            Метод запускает бесконечный цикл слушающий подключения
        """
        self.socket.listen(backlog)
        while True:
            con, (ip, port) = self.socket.accept()

            c = Client(ip, port, con)
            c.uuid = uuid.uuid4()
            c.start()

            self.connections[c.uuid] = c

        self.close_sock()


def process_requests(server: Server, queue: dict):
    """
        Метод обрабатывает очередь ходов
    """
    last_send = time.time()
    while True:
        if not (time.time() - last_send) >= 0.02:
            # time.sleep(0.2 - (time.time() - last_send))
            continue

        for user, turn in queue.items():
            server.send_msg(user, str(turn))

        last_send = time.time()

def start_serv():
    # if __name__ == '__main__':
    serv = Server('127.0.0.1', 6666)
    threading.Thread(target=process_requests, args=(serv, STEPS_QUEUE)).start()
    serv.listen_connections()