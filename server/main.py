# -*- coding: utf-8 -*-
"""
    Инициализация сервера
"""

import time
import curses
import threading
import subprocess
import win32gui
from room import Room
from wsocket.server import Server
from wsocket.handler import Handler
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


def debug_window(room: Room):
    """
        Отладочное окно с игровым полем
    """
    stinf = subprocess.STARTUPINFO()

    proc = subprocess.Popen("cmd.exe", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    proc.
    print('kk2')


if __name__ == '__main__':
    serv_sock = Server(AF_INET, SOCK_STREAM)
    serv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    serv_sock.bind(('localhost', 5000))
    serv_sock.listen(8)
    room = Room()
    serv_sock.on_accept(Handler(room.add_player))
    serv_sock.add_task(Handler(room.broadcast), 1000)
    print('Сервер запущен...')
    threading.Thread(target=debug_window, args=(room,)).start()
    serv_sock.forever()

