# -*- coding: utf-8 -*-
"""
    Модуль содержит пользовательские исключения
"""


class InvalidHttpHeader(Exception):
    """
        Исключения для ошибок в формате http заголовков
    """

    def __init__(self, name: str, value: Optional[str] = None) -> None:
        self.name = name
        self.value = value
        super().__init__(message)


class InvalidHeaderName(InvalidHttpHeader):
    pass


class InvalidHeaderValue(InvalidHttpHeader):
    pass


class InvalidHeaderLine(InvalidHttpHeader):
    pass
