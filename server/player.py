# -*- coding: utf-8 -*-
"""
    Модуль содержит класс игрока
"""

from collections import deque

# Максимальная длина комбинации ходов
MAX_STEPS_QUEUE = 2


class Player:
    def __init__(self, sock, name: str = None):
        """
            Инициализация нового игрока
        """
        # ник игрока
        self._name = name
        # сокет по которому подключен игрок
        self.source_sock = sock
        # Очередь ходов игрока.
        # Она обеспечивает возможность очень быстро сделать два хода,
        # например для резкого разворота.
        self.steps_queue = deque(maxlen=MAX_STEPS_QUEUE)

        self.last_step = None


    def fileno(self) -> int:
        """
            Получение файлового дескриптора сокета к
            которому подключен игрок
        """
        return self.source_sock.fileno()


    def name(self) -> str:
        """
            Получение имени игрока
        """
        if not self._name:
            return 'Player'

        return self._name


    def check_steps(self) -> None:
        """
            Чтение нажатых клавиш
        """
        step = self.source_sock.recv(1024)

        if not step:
            return

        self.steps_queue.append(step)


    def get_step(self):
        """
            Получение текущего хода игрока
        """
        if self.steps_queue:
            step = self.steps_queue.popleft()
            self.last_step = step

            return step

        return None
