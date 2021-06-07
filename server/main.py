# -*- coding: utf-8 -*-
"""
    Инициализация сервера
"""

import os
import time
import random
import platform
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

    if platform.system() == 'Windows':
        proc_name = 'cmd.exe'
        encoding = 'cp1252'
        echo_tmpl = 'echo "{row}" & '
        clear_screen = 'cls\n'
        win_resize = 'mode con: cols={height} lines={width}\n'
    else:
        return

    proc = subprocess.Popen(
        proc_name,
        bufsize=0,
        cwd=os.getcwd(),
        stdin=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
        startupinfo=stinf
    )
    # proc.stdin.write('python .\debug_win.py\n'.encode())
    hg = room.map.height
    wd = room.map.width

    proc.stdin.write(win_resize.format(height=hg + 10, width=wd + 10).encode(encoding))

    while True:
        # room.map.map[random.randint(1, hg-2)][random.randint(1, wd-2)] = 2
        mp = str(room.map).split('\n')
        res = ''
        for row in mp:
            res += echo_tmpl.format(row=row)

        res += '\n'

        proc.stdin.write(res.encode(encoding))
        time.sleep(0.1)
        proc.stdin.write(clear_screen.encode(encoding))


if __name__ == '__main__':
    serv_sock = Server(AF_INET, SOCK_STREAM)
    serv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    serv_sock.bind(('localhost', 5000))
    serv_sock.listen(8)
    room = Room()
    # Добавляем событие нового подключения
    serv_sock.on_accept(Handler(room.add_player))

    # Добавляем задачу на постоянную рассылки позиций игроков
    serv_sock.add_task(Handler(room.send_positions), 300)

    print('Сервер запущен...')
    # Запускаем поток с откладочным окном
    threading.Thread(target=debug_window, args=(room,)).start()

    # Запускаем сервер
    serv_sock.forever()

