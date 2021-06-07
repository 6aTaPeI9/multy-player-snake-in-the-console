# -*- coding: utf-8 -*-
"""
    Модуль содержит класс игрока
"""

from snake import Snake
from collections import deque
from helpers.coord import Coord
from helpers.keys import StepKeys, STEP_KEY



# Максимальная длина комбинации ходов
MAX_STEPS_QUEUE = 2

# Модификаторы позиции от нажатых клавиш
POS_MODIF = {
    StepKeys.UP: Coord(0, -1),
    StepKeys.DOWN: Coord(0, 1),
    StepKeys.LEFT: Coord(-1, 0),
    StepKeys.RIGHT: Coord(1, 0)
}

class Player:
    def __init__(self, name: str = None, start_pos = list):
        """
            Инициализация нового игрока
        """
        # ник игрока
        self._name = name

        # Очередь ходов игрока.
        # Она обеспечивает возможность очень быстро сделать два хода,
        # например для резкого разворота.
        self.steps_queue = deque(maxlen=MAX_STEPS_QUEUE)

        self.last_step = POS_MODIF.get(StepKeys.UP)

        self.snake = Snake(start_pos)

        self.dead = False


    def name(self) -> str:
        """
            Получение имени игрока
        """
        if not self._name:
            return 'Player'

        return self._name


    def set_name(self, name):
        """
            Обработчик события сокета.
            Установка нового имени игрока.
        """
        if not name:
            return

        self._name = name


    def key_pressed(self, event) -> None:
        """
            Очередь нажатых клавиш
        """
        key = event.get('data')

        # Пустое событие
        if not key:
            return

        key = STEP_KEY.get(key)

        # Неизвестная клавиша
        if not key:
            return

        self.steps_queue.append(POS_MODIF.get(key))


    def get_step(self):
        """
            Получение текущего хода игрока
        """
        if self.steps_queue:
            step = self.steps_queue.popleft()
            self.last_step = step
        else:
            step = self.last_step

        # Добавляем голову
        head = self.snake.move_head(step)

        return head