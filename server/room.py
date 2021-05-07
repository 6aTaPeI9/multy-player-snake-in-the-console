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


    def del_player(self, player):
        """
            Удаление игрока
        """
        print('Игрока удаляют')
        self.players.remove(player)


    def add_player(self, player_sock):
        """
            Добавление нового игрока в комнату
        """
        self.players_count += 1

        player = Player(player_sock, f'Player{self.players_count}')
        player_sock.close_event = [self.del_player, (player,)]

        self.players.append(player)
