# -*- coding: utf-8 -*-
"""
    Модуль содержит класс обработчиков
"""


class Handler:
    def __init__(self, call_object: callable, *args: tuple, **kwargs):
        """
            Инициализация обьекта обработчика
        """
        self.object = call_object
        self.args = args
        self.kwargs = kwargs

    def call(self):
        """
            Вызов обработчика
        """
        return self.object(*self.args, **self.kwargs)
