import socket
import sys
import threading
import curses
import json
import multiprocessing
import server


from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from queue import Queue

# Соответствие кнопок и оси координат.
# Игрок не может не сделать два хода подряд по одной и той же оси.
COORD_BACK_KEYS = {
        KEY_RIGHT: 'x',
        KEY_LEFT: 'x',
        KEY_UP: 'y',
        KEY_DOWN: 'y'
    }

port = 6666
size = 1024

sock_conn = None
login = ''

TURNS_HISTORY = {}

# Идентификаторы игровых событий

# Событие гибели игрока
ACTION_DEAD = 1

def init_socket():
    global sock_conn, login
    try:
        sock_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_conn.connect(('127.0.0.1', port))
        login = input('Login: ')
        sock_conn.sendall(login.encode())
    except socket.error as err:
        if sock_conn:
            sock_conn.close()
        print("Не открыт: " + str(err))


def key_listener(win):
    global sock_conn
    prev_key = KEY_LEFT
    while prev_key != 27:
        pressed_key = win.getch()

        if not pressed_key:
            continue

        if not pressed_key in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:
            continue

        if pressed_key == prev_key:
            continue

        if COORD_BACK_KEYS.get(pressed_key) == COORD_BACK_KEYS.get(prev_key):
            continue

        prev_key = pressed_key
        sock_conn.sendall(str(pressed_key).encode())


def render_win(win):
    global sock_conn, TURNS_HISTORY
    while True:
        data = sock_conn.recv(1024)
        if data:
            coord = None
            try:
                coord = data
            except Exception:
                continue

            win.addstr(15, 15, str(data))


if __name__ == '__main__':
    print('Запуск сервера')
    multiprocessing.Process(target=server.start_serv).start()
    print('сервер запущен')
    init_socket()
    curses.initscr() # Инициализируем модуль curses в терминале
    win = curses.newwin(25, 100, 0, 0)
    win.keypad(True)
    curses.noecho() # Убираем вывод нажатых клавишь на экран
    curses.curs_set(False) # Убираем подсветку текущей позиции курсора
    win.border(0)
    win.nodelay(1)
    threading.Thread(target=render_win, args=(win,)).start()
    key_listener(win)
    curses.endwin()

