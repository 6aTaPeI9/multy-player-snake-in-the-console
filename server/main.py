# -*- coding: utf-8 -*-
"""
    Инициализация сервера
"""


from room import Room
from player import Player
from wsocket.server import Server
from wsocket.handler import Handler
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


def register_player_handlers(sock, room: Room, player: Player):
    """
        Установка стандартных обработчиков для каждого игрока
    """
    sock.on('key_pressed', Handler(player.key_pressed))

    change_name_handler = Handler(player.set_name)
    change_name_handler.sub_handler(Handler(room.broadcast, info='names'), False)
    sock.on('name_change', change_name_handler)

    sock.on_close(Handler(room.del_player, player=player))
    sock.on_connect(Handler(room.add_player, player=player))

    return


def add_server_handlers(serv: Server):
    """
        Добавление событий сервера
    """
    return


if __name__ == '__main__':
    serv_sock = Server(AF_INET, SOCK_STREAM)
    serv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    serv_sock.bind(('localhost', 5000))
    serv_sock.listen(8)
    serv_sock.forever()
    print('Сервер запущен...')
