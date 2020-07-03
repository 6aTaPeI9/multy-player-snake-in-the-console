class Snake:
    def __init__(self, start_x: int, start_y: int):
        """
            Иниализация обьекта змейки
        """
        self.dead = False
        self.pos = [[start_x, start_y]]


    def make_turn(self, turn: int):
        """
            Метод перемещает голову змеи в направлении нажатой клавиши
        """
        pass