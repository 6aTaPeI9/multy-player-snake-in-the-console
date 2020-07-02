# -*- coding: utf-8 -*-
"""
    Модуль содержащий реализацию синглтона.
"""
__author__ = "6aTaPeI9"

class Singleton(type):
    _INSTANCE = None

    def __call__(self, *args, **kwargs):
        if not self._INSTANCE:
            self._INSTANCE = super().__call__(*args, **kwargs)

        return self._INSTANCE
