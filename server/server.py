# -*- coding: utf-8 -*-
"""
    Модуль содержит основной код серверной части.
"""
__author__ = "6aTaPeI9"

import socket
import threading

from singleton import Singleton


class Client(threading.Thread):
    def __init__(self, ip, port, con):
        super().__init__()
        self.con = con
        self.ip = ip
        self.port = port
        self.login = None


    def run(self):
        try:
            while True:
                data = self.con.recv(1024)
                if not data:
                    break

                data = data.decode()

                if not self.login:
                    self.login = data
                    continue
                else:
                    pass
        finally:
            self.con.close()
        pass


class Server(metaclass=Singleton):
    def __init__(self, port: int, address: str):
        """
            Инициализация класса сервера
        """
        # список всех текущих подключений
        self.connections = []
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
            c.start()

        self.close_sock()
        pass


def process_requests():
    pass

if __name__ == '__main__':
    serv = Server('127.0.0.1', 6666)
    serv.listen_connections()