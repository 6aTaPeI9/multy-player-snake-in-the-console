# -*- coding: utf-8 -*-
"""
    Модуль содержит пользовательские исключения при обработке
    http вызовов
"""


class InvalidHttpHeader(Exception):
    """
        Исключения для ошибок в формате http заголовков
    """
    def __init__(self, message: str, name: str = None, value: str = None) -> None:
        message += f'{name}: {value}'
        super().__init__(message)


class HeaderNotFound(InvalidHttpHeader):
    """
        Исключения для обязательных заголовков, которые не были переданы
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('Could not find header - ', *args, **kwargs)


class TooMuchHeader(InvalidHttpHeader):
    """
        Исключения для ошибок в формате http заголовков
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('Could not find header - ', *args, **kwargs)


class InvalidHeaderName(InvalidHttpHeader):
    """
        Исключение дла ошибок в формате ключ заголовка
    """
    def __init__(self, *args, **kwargs):
        super().__init__('invalid header name', *args, **kwargs)


class InvalidHeaderValue(InvalidHttpHeader):
    """
        Исключение дла ошибок в формате значения заголовка
    """
    def __init__(self, *args, **kwargs):
        super().__init__('invalid header value', *args, **kwargs)


class InvalidHeaderLine(InvalidHttpHeader):
    """
        Исключение дла ошибок в формате строки заголовка
    """
    def __init__(self, *args, **kwargs):
        super().__init__('invalid header line', *args, **kwargs)


class NotSupportedProtocolVersion(Exception):
    """
        Исключение дла ошибок в формате строки заголовка
    """
    def __init__(self, *args, **kwargs):
        super().__init__('invalid header line', *args, **kwargs)
