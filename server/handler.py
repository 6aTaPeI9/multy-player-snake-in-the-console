# -*- coding: utf-8 -*-
"""
    Модуль содержит класс обработчиков
"""


class Handler:
    def __init__(self, call_object: callable, **kwargs):
        """
            Инициализация обьекта обработчика
        """
        self.object = call_object
        self.kwargs = kwargs

    def call(self, data: None):
        """
            Вызов обработчика
        """
        if data:
            return self.object(data, **self.kwargs)

        return self.object(**self.kwargs)

