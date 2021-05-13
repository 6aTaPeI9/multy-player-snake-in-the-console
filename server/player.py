# -*- coding: utf-8 -*-
"""
    Модуль содержит класс игрока
"""

from collections import deque

# Максимальная длина комбинации ходов
MAX_STEPS_QUEUE = 2


class Player:
    def __init__(self, name: str = None):
        """
            Инициализация нового игрока
        """
        # ник игрока
        self._name = name

        # Очередь ходов игрока.
        # Она обеспечивает возможность очень быстро сделать два хода,
        # например для резкого разворота.
        self.steps_queue = deque(maxlen=MAX_STEPS_QUEUE)

        self.last_step = None


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
            Обработчик нажатых клавиш
        """
        key = event.get('data')
        print('Сработало событие KeyPressed', key)

        if not key:
            return

        self.last_step = key


    def get_step(self):
        """
            Получение текущего хода игрока
        """
        if self.steps_queue:
            step = self.steps_queue.popleft()
            self.last_step = step

            return step

        return None

