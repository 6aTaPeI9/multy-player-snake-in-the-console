# -*- coding: utf-8 -*-
"""
    Модуль содержит класс игрока
"""

from collections import deque

class Player:
    def __init__(self, sock):
        """
            Инициализация нового игрока
        """
        # ник игрока
        self._name = None
        # сокет по которому подключен игрок
        self.sourc_sock = sock
        # Очередь ходов игрока.
        # Она обеспечивает возможность очень быстро сделать два хода,
        # например для резкого разворота.
        self.steps_queue = deque

        return


    def fileno(self):
        """
            Получение файлового дескриптора сокета к
            которому подключен игрок
        """
        return self.sourc_sock.fileno()


    def name(self):
        """
            Получение имени игрока
        """

        if not self._name:
            return 'Player'

        return self._name


    def check_steps(self):
        """
            Чтение нажатых клавиш
        """