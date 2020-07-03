import uuid
import random

from player import Player

class Map:
    def __init__(self, width: int, height: int, max_players: int):
        """
            Инициализация обьекта игрового поля
        """
        self.width = width
        self.height = height
        self.max_players = max_players
        self.players = {}
        self.apples = []

    def add_player(self, player_conn: tuple):
        """
            Мето добавляет на карту нового игрока
        """
        p_uuid = uuid.uuid4()
        player = Player(*player_conn)
        player.uuid = p_uuid

        self.players[p_uuid] = player

    # def 
