# -*- coding: utf-8 -*-
"""
    Модуль содержит методы для работы с http заголовками
"""

import sys

from io import BytesIO
from re import compile as re_compile
from .exceptions import (
    InvalidHttpHeader,
    InvalidHeaderName,
    InvalidHeaderValue,
    InvalidHeaderLine
)

# Максимальное кол-во заголовков
MAX_HEADERS = 256

# Максимальная длина контента одного заголовка
MAX_LINE = 4096

# Юзерагент сервера
USER_AGENT = f"Python/{sys.version[:3]} snakegame/1"

# Шаблон ключа в заголовке
HKEY_RE = re_compile(rb"[-!#$%&\'*+.^_`|~0-9a-zA-Z]+")

# Шаблон для значения в заголовке
HVALUE_RE = re_compile(rb"[\x09\x20-\x7e\x80-\xff]*")

class HttpRequest:
    def __init__(self):
        self.status = 101
        self.headers = {}
        self.exception = None


    def write_exc(self, ex: Exception):
        """
            Метод обрабатывает исключение
        """
        self.status = 666
        self.exception = ex


    def read_request(self, stream: bytes):
        """
            Чтение и парсинг HTTP запроса
        """
        # Преобразовываем в поток байт
        stream = BytesIO(stream)

        # Читаем открывающую строку http запрсоа
        request_line = self._read_line(stream)

        try:
            method, raw_path, version = request_line.split(b" ", 2)
        except ValueError:
            return self.write_exc(InvalidHeaderLine(value=request_line.decode()))

        if method != b"GET":
            return self.write_exc(InvalidHttpHeader(f'Unsopported http method - {method}'))

        if version != b"HTTP/1.1":
            return self.write_exc(InvalidHttpHeader(f'Unsopported http version - {method}'))

        self.path = raw_path.decode("ascii", "surrogateescape")

        self._read_headers(stream)

        return


    def _read_headers(self, stream: BytesIO):
        """
            Метод парсит и валидирует все http заголовки
        """
        for _ in range(MAX_HEADERS + 1):

            line = self._read_line(stream)

            if line == b"":
                break

            try:
                raw_name, raw_value = line.split(b":", 1)
            except ValueError:
                return self.write_exc(InvalidHeaderLine(line.decode()))

            if not HKEY_RE.fullmatch(raw_name):
                return self.write_exc(InvalidHeaderName(raw_name.decode()))

            raw_value = raw_value.strip(b" \t")

            if not HVALUE_RE.fullmatch(raw_value):
                return self.write_exc(InvalidHeaderValue(raw_value.decode()))

            name = raw_name.decode("ascii")
            value = raw_value.decode("ascii", "surrogateescape")
            self.__setitem__(name, value)
        else:
            return self.write_exc(InvalidHttpHeader("Too many http headers"))

        return


    def _read_line(self, stream: BytesIO) -> bytes:
        """
            Метод читает одну строку http запроса
        """
        line = stream.readline()

        if len(line) > MAX_LINE:
            raise InvalidHttpHeader("Too long line.", value=line)

        if not line.endswith(b"\r\n"):
            raise EOFError("Line without CRLF")

        return line[:-2]


    def get(self, key: str):
        """
            Чтение заголовка
        """
        return self.headers.get(key)


    def __setitem__(self, key, value) -> None:
        """
            Установка нового заголовка
        """
        if not self.headers[key]:
            self.headers[key] = value

        elif isinstance(self.headers[key], list):
            self.headers[key].append(value)

        else:
            self.headers[key] = [self.headers[key], value]

        return