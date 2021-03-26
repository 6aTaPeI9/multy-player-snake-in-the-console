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


def read_request(stream: bytes):
    """

    """
    # Преобразовываем в поток байт
    stream = BytesIO(stream)

    # Читаем открывающую строку http запрсоа
    request_line = read_line(stream)

    try:
        method, raw_path, version = request_line.split(b" ", 2)
    except ValueError:
        raise InvalidHeaderLine(value=request_line.decode())

    if method != b"GET":
        raise InvalidHttpHeader(f'Unsopported http method - {method}')

    if version != b"HTTP/1.1":
        raise InvalidHttpHeader(f'Unsopported http version - {method}')

    path = raw_path.decode("ascii", "surrogateescape")

    headers = read_headers(stream)

    return path, headers


def read_headers(stream):
    """
    """
    headers = {}

    for _ in range(MAX_HEADERS + 1):

        line = read_line(stream)

        if line == b"":
            break

        try:
            raw_name, raw_value = line.split(b":", 1)
        except ValueError:
            raise InvalidHeaderLine(line.decode())

        if not HKEY_RE.fullmatch(raw_name):
            raise InvalidHeaderName(raw_name.decode())

        raw_value = raw_value.strip(b" \t")

        if not HVALUE_RE.fullmatch(raw_value):
            raise InvalidHeaderValue(raw_value.decode())

        name = raw_name.decode("ascii")
        value = raw_value.decode("ascii", "surrogateescape")
        headers[name] = value

    else:
        raise InvalidHttpHeader("Too many http headers")

    return headers


def read_line(stream) -> bytes:
    """
    """
    line = stream.readline()

    if len(line) > MAX_LINE:
        raise InvalidHttpHeader("Too long line.", value=line)

    if not line.endswith(b"\r\n"):
        raise EOFError("Line without CRLF")

    return line[:-2]
