# -*- coding: utf-8 -*-
"""
    Вспомогательные обьекты для работы с координатами
"""

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __str__(self):
        return f'x: {self.x}, y: {self.y}'


class Ceil:
    EMPTY = 0
    WALL = 1
    PLAYER = 2
    FOOD = 3