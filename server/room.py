
from player import Player

class Room:
    def __init__(self):
        """
            Инициализация новой игровой сессии
        """
        self.players = []
        self.players_count = 0


    def add_player(self, player_sock):
        """
            Добавление нового игрока в комнату
        """
        self.players_count += 1

        player = Player(player_sock, f'Player{self.players_count}')

        self.players.append(player)
