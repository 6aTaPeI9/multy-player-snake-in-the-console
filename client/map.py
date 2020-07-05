# -*- coding: utf-8 -*-
"""
    Модуль содержащий класс игрового поля.
"""
__author__ = "6aTaPeI9"


import uuid
import random

from player import Player
from functools import lru_cache

class Map:
    def __init__(self, width: int, height: int, max_players: int):
        """
            Инициализация обьекта игрового поля
        """
        self.width = width
        self.height = height
        self.max_players = max_players
        self.snakes = {}
        self.apples = []


    def add_player(self, player_conn: tuple):
        """
            Мето добавляет на карту нового игрока
        """
        p_uuid = uuid.uuid4()
        player = Player(*player_conn)
        player.uuid = p_uuid

        self.players[p_uuid] = player

    @lru_cache(maxsize=1024)
    def get_occupied_pos(self):
        pass
