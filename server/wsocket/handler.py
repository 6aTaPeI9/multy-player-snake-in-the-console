# -*- coding: utf-8 -*-
"""
    Модуль содержит класс обработчиков
"""

import inspect

class Handler:
    def __init__(self, func: callable, **kwargs):
        """
            Инициализация обьекта обработчика
        """
        if 'event' not in list(inspect.signature(func).parameters):
            raise ValueError(f'Метод {func.__name__} не принимает обязательный параметр event')

        self.func = func
        self.kwargs = kwargs
        self.before_handler = None
        self.after_handler = None


    def call(self, event_obj):
        """
            Вызов обработчика
        """
        if self.before_handler:
            self.before_handler.call(event_obj)

        self.func(event_obj, **self.kwargs)

        if self.after_handler:
            self.after_handler.call(event_obj)


    def sub_handler(self, handler, before: bool):
        """
            Обработчик для обработчика
            :param before: флаг позиции вызова относительно основного обработчика
        """
        if not handler:
            return

        if before:
            self.before_handler = handler
        else:
            self.after_handler = handler
