# -*- coding: utf-8 -*-
"""
    Обьект карты
"""

class StepKeys:
    UP = (38, 87)
    DOWN = (40, 83)
    LEFT = (37, 65)
    RIGHT = (39, 68)


class Ceil:
    EMPTY = 0
    WALL = 1
    PLAYER = 2
    FOOD = 3


class Map:
    def __init__(self, width, height):
        """
            Инциализация карты
        """
        self.width = width
        self.height = height
        self.map = []
        self.__fill_map()


    def __fill_map(self):
        """
            Заполнение карты значениями по умолчанию
        """

        # Заполняем клетки пустотой
        for y in range(self.height):
            self.map.append([])
            for x in range(self.width):
                # На границы карты ставим тип WALL
                if (x in (0, self.width - 1)) or y in (0, self.height - 1):
                    self.map[y].append(Ceil.WALL)
                else:
                    self.map[y].append(Ceil.EMPTY)


    def __str__(self):
        """
            Приведем карту к читаемому виду
        """
        res = '\n'
        row_len = (self.width - 2)
        for idx, _ in enumerate(self.map):

            if idx  == 0:
                res += f'-{"-" * row_len}-\n'
            elif idx == (self.height - 1):
                res += f'-{"-" * row_len}-\n'
            else:
                res += f'|{" " * row_len}|\n'

        return res


mp = Map(50, 20)
