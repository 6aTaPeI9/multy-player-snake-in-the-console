# -*- coding: utf-8 -*-
"""
    Инициализация сервера
"""

from server import Server
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


if __name__ == '__main__':
    serv_sock = Server(AF_INET, SOCK_STREAM)
    serv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    serv_sock.bind(('localhost', 5000))
    serv_sock.listen(8)
    serv_sock.forever()
    print('Сервер запущен...')
