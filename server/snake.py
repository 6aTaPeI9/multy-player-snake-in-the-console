# -*- coding: utf-8 -*-
"""
    Модуль содержит класс змейки
"""

from helpers.coord import Coord


class Snake:
    def __init__(self, pos: list):
        self._snake = pos
        super().__init__()


    def head(self):
        """
            Получение координат головы
        """
        return self._snake[0]


    def move_head(self, coord_modif: Coord):
        """
            Добавление новой головы
        """
        new_head = Coord(
            self._snake[0].x + coord_modif.x,
            self._snake[0].y + coord_modif.y
        )
        self._snake.insert(0, new_head)
        return new_head


    def tail(self):
        """
            Получение координат хвоста
        """
        return self._snake[len(self._snake) - 1]


    def move_tail(self):
        """
            Перемещение хвоста
        """
        return self._snake.pop()
