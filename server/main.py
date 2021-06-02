# -*- coding: utf-8 -*-
"""
    Инициализация сервера
"""

from room import Room
from wsocket.server import Server
from wsocket.handler import Handler
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


if __name__ == '__main__':
    serv_sock = Server(AF_INET, SOCK_STREAM)
    serv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    serv_sock.bind(('localhost', 5000))
    serv_sock.listen(8)
    room = Room()
    serv_sock.on_accept(Handler(room.add_player))
    serv_sock.add_task(Handler(room.broadcast), 1000)
    print('Сервер запущен...')
    serv_sock.forever()

