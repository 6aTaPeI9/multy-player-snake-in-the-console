# -*- coding: utf-8 -*-
"""
    Обьект игровой команаты.
    Управляет рассылкой данных.
"""


from player import Player

class Room:
    def __init__(self):
        """
            Инициализация новой игровой сессии
        """
        self.players: Player = []
        self.players_count = 0


    def del_player(self, player: Player):
        """
            Удаление игрока
        """
        print('Игрока удаляют')
        self.players.remove(player)


    def add_player(self, player: Player):
        """
            Добавление нового игрока в комнату
        """
        print('Игрока добавили')
        self.players_count += 1
        self.players.append(player)
        player._name = f'Player{self.players_count}'


    def broadcast(self):
        for player in self.players:
            print(f'Игрок {player.name}')