# -*- coding: utf-8 -*-
"""
    Обьект карты
"""


from helpers.coord import Coord, Ceil


CEIL_STR_FORMAT = {
    Ceil.EMPTY: ' ',
    Ceil.WALL: '#',
    Ceil.PLAYER: '*',
    Ceil.FOOD: '+'
}

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
        for y in range(self.height):
            for x in range(self.width):
                res += CEIL_STR_FORMAT.get(self.map[y][x])

            res += '\n'

        res += '\n'
        return res


    def ceil(self, coord: Coord):
        """
            Получение клетки
        """
        return self.map[coord.y][coord.x]