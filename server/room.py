# -*- coding: utf-8 -*-
"""
    Обьект игровой команаты.
    Управляет рассылкой данных.
"""


from game_map import Map
from player import Player
from helpers.coord import Ceil, Coord
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

        return [Coord(18, 18)]


    def del_player(self, event):
        """
            Удаление игрока
        """
        print('Удаление игрока')
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

        # Подписываем игрока на событие нажатия клавиши
        source.on('KEY_PRESSED', Handler(new_player.key_pressed))

        # Подписываем игрока на событие отключения
        source.on_close(Handler(self.del_player, player = new_player))

        self.players.append(new_player)


    def send_positions(self, event):
        """
            Итерация ходов.
        """
        source = event.get('source')

        for player in self.players:
            if player.dead:
                continue

            head = player.get_step()
            print('Head: ', head)
            ceil = self.map.ceil(head)

            if ceil in (Ceil.WALL, Ceil.PLAYER):
                print('Игрок умер')
                player.dead = True
            elif ceil == Ceil.EMPTY:
                tail = player.snake.move_tail()
                self.map.map[tail.y][tail.x] = Ceil.EMPTY
                self.map.map[head.y][head.x] = Ceil.PLAYER

        # source.broadcast()