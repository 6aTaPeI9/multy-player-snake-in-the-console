# -*- coding: utf-8 -*-
"""
    Обьект игровой команаты.
    Управляет рассылкой данных.
"""


from game_map import Map
from player import Player
from wsocket.handler import Handler


class Room:
    def __init__(self):
        """
            Инициализация новой игровой сессии
        """
        self.players: Player = []
        self.players_count = 0
        self.map = Map(20, 20)


    def search_free_spawn(self):
        """
            Метод выполняет поиск свободного пространства для спавна игрока.
        """

        return (7, 7)


    def del_player(self, event):
        """
            Удаление игрока
        """
        del_player = event.get('player')

        if not del_player:
            return

        self.players.remove(del_player)


    def add_player(self, event):
        """
            Добавление нового игрока в комнату
        """
        print('Игрока добавили')

        self.players_count += 1

        # Имя игрока
        name = f'Player{self.players_count}'
        new_player = Player(name, self.search_free_spawn())
        source = event.get('source')
        source.on('KEY_PRESSED', Handler(new_player.key_pressed))
        source.on_close(Handler(self.del_player, player = new_player))

        self.players.append(new_player)


    def broadcast(self, event):
        source = event.get('source')
        dt = ''

        for player in self.players:
            dt += f'Игрок {player.name()} нажал {player.last_step}'

        if dt:
            source.broadcast(dt)