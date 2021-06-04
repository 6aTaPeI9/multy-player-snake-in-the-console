# -*- coding: utf-8 -*-
"""
    Инициализация сервера
"""

import time
import os
# import curses
import threading
import subprocess
from room import Room
from wsocket.server import Server
from wsocket.handler import Handler
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


def debug_window(room: Room):
    """
        Отладочное окно с игровым полем
    """
    stinf = subprocess.STARTUPINFO()
    stinf.wShowWindow = 5

    proc = subprocess.Popen(
        'cmd.exe',
        bufsize=0,
        cwd=os.getcwd(),
        stdin=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
        startupinfo=stinf
    )
    import time
    # proc.stdin.write('python .\debug_win.py\n'.encode())

    while True:
        mp = str(room.map).split('\n')
        res = ''

        for row in mp:
            if not row:
                continue
            res += f'echo "{row}" &'

        res = res[:-1]
        res += '\n'

        proc.stdin.write(res.encode())
        time.sleep(1)
        proc.stdin.write('cls\n'.encode())

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

