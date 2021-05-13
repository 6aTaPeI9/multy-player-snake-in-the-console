# -*- coding: utf-8 -*-
"""
    Обьект игровой команаты.
    Управляет рассылкой данных.
"""


from player import Player
from wsocket.handler import Handler

class Room:
    def __init__(self):
        """
            Инициализация новой игровой сессии
        """
        self.players: Player = []
        self.players_count = 0


    def del_player(self, event):
        """
            Удаление игрока
        """
        del_player = event.get('DelPlayer')

        if not del_player:
            return

        self.players.remove(del_player)


    def add_player(self, event):
        """
            Добавление нового игрока в комнату
        """
        print('Игрока добавили')

        self.players_count += 1
        new_player = Player(f'Player{self.players_count}')
        source = event.get('socket')
        source.on('KEY_PRESSED', Handler(new_player.key_pressed))

        self.players.append(new_player)


    def broadcast(self, event):
        print('Вызван room.broadcast')
        source = event.get('Server')
        dt = ''

        for player in self.players:
            dt += f'Игрок {player.name()} нажал {self.last_step}'

        source.broadcast(dt)
