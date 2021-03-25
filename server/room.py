
from player import Player

class Room:
    def __init__(self):
        """
            Инициализация новой игровой сессии
        """
        self.players = []


    def add_player(self, player_sock):
        """
            Добавление нового игрока в комнату
        """
        self.players.append(player_sock)