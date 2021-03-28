# -*- coding: utf-8 -*-
"""
    Модуль содержит основной поток событий, обработку входящих подключений
    прием и отправку данных
"""

import threading

from room import Room
from select import select
from wsocket import wsocket

# Длительность опроса потоков чтения и записи в подключенных сокетах
SELECT_TIMEOUT = 1


def accept_new_player(sock: wsocket.WSocket, room: Room):
    """
        Прием подключения нового игрока.
    """
    player_sock, _ = sock.accept()

    room.add_player(player_sock)
    return


def receive_data(serv_sock: wsocket.WSocket, room: Room):
    """
        Метод слушает новые подключения игроков и получает данные
        от уже подключенных.
    """
    while True:
        receive_sock, send_sock, _ = select(room.players + [serv_sock], [], [], SELECT_TIMEOUT)

        for sock in receive_sock:
            # Если поток чтения в серверном сокете не пуст
            # принимаем новое подключение
            if sock is serv_sock:
                accept_new_player(serv_sock, room)
            else:
                sock.check_steps()

        for player in room.players:
            print(f'Игрок: {player.name()} нажал: {player.get_step()}')


        # for player in send_sock:


if __name__ == '__main__':
    serv_sock = wsocket.WSocket(
        wsocket.socket.AF_INET,
        wsocket.socket.SOCK_STREAM
    )

    serv_sock.setsockopt(
        wsocket.socket.SOL_SOCKET,
        wsocket.socket.SO_REUSEADDR,
        1
    )

    serv_sock.bind(('localhost', 5000))
    serv_sock.listen(5)

    room = Room()
    # threading.Thread(target=receive_data, args=(serv_sock, room)).start()
    print('Сервер запущен...')
    receive_data(serv_sock, room)
