# -*- coding: utf-8 -*-
"""
    Модуль парсинга фреймов
"""

import uuid
from io import BytesIO
from functools import lru_cache

# FIN бит. Указывает фгарменитрованность данных.
# Если фрагмент один или последний то FIN = 0, инчае = 1
FIN = 0b10000000

# Зарезервированные биты для пользовательский расширений протокола.
# По умолчанию всегда равны 0
RSV1 = 0b01000000
RSV2 = 0b00100000
RSV3 = 0b00001000

# Бит указывает маскированы ли данные.
DATA_MASKING = 0b10000000

class OpCodes:
    # opcode расположен в последних 4 битах байта.
    POS = 0b00001111

    OP_TEXT = 0x1
    OP_BINARY = 0x2
    OP_CLOSE = 0x8
    OP_PING = 0x9
    OP_PONG = 0xA
    OP_ADDIT_FRAME = 0x0

    @staticmethod
    @lru_cache(64)
    def codes_list():
        """
            Получение списка кодов
        """
        attrs = []
        for attr, value in OpCodes.__dict__.items():
            if attr.startswith('OP_'):
                attrs.append(value)

        return attrs


class Frame:
    def __init__(self, frame: bytes = None, data: str = None):
        """
            Инициализация фрейма
        """
        self._frame = frame
        self._data = data
        self._op_code = OpCodes.OP_TEXT


    def data(self):
        """
            Получение контента из фрейма
        """
        # Если контент уже есть, парсить ничего не нужно
        if self._data:
            return self._data

        # Если фрема нет, отдаем None
        if not self._frame:
            return None

        reader = BytesIO(self._frame)

        # Читаем первые два байта сообщения
        byte1, byte2 = reader.read(2)

        fin = byte1 & FIN

        op_code = byte1 & OpCodes.POS

        # Читаем второй байт сообщения.
        # В нем находится длина последующего контента
        lenght = byte2 & 0b01111111
        mask = byte2 & DATA_MASKING

        if lenght == 126:
            lenght = reader.read(1)
        elif lenght == 127:
            lenght = reader.read(2)

        if mask:
            # Читаем маску
            mask = reader.read(4)
            # Читаем маскированные данные
            masked_data = reader.read(lenght)
            mask = iter_loop(mask)

            # Применяем маску 
            data = b''
            for bt in masked_data:
                mk = mask.__next__()
                data += (bt ^ mk).to_bytes(1, 'big')
        else:
            data = reader.read(lenght)

        if op_code != OpCodes.OP_CLOSE:
            data = data.decode()

        result = {
            'OpCode': hex(op_code),
            'Data': data
        }
 
        self._data = result
        return result


    def frame(self):
        """
            Получение фрейма
        """
        if not self._op_code:
            raise ValueError('Для обьекта не задан OpCode.')

        if self._frame:
            return self._frame

        if not self._data:
            return None

        body = self._data.encode()
        lenght = len(body)

        masked = 0b00000000
        # Байт с длинной контента, где первый бит указывают маскированы ли данные
        if lenght <= 125:
            len_byte = (masked | lenght).to_bytes(1, 'big')
        elif lenght <= 65535:
            len_byte = (masked | 126).to_bytes(1, 'big')
            len_byte += lenght.to_bytes(2, 'big')
        else:
            len_byte = (masked | 127).to_bytes(1, 'big')
            len_byte += lenght.to_bytes(8, 'big')

        first_byte = (0b10000000 | self._op_code).to_bytes(1, 'big')
        res = first_byte + len_byte + body

        self._frame = res
        return res


    def set_op_code(self, op_code):
        """
            Установка opcode
        """
        if op_code not in OpCodes.codes_list():
            raise ValueError(f'OpCode - <{op_code}> не поддерживается.')

        self._op_code = op_code



def iter_loop(iterable):
    """
        Бесконечная итерация
    """

    while True:
        for item in iterable:
            yield item

    return
