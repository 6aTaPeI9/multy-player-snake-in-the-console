# -*- coding: utf-8 -*-
"""
    Модуль парсинга фреймов
"""
# FIN бит. Указывает фгарменитрованность данных.
# Если фрагмент один или последний то FIN = 0, инчае = 1
FIN = 0x10000000

# Зарезервированные биты для пользовательский расширений протокола.
# По умолчанию всегда равны 0
RSV1 = 0x01000000
RSV2 = 0x00100000
RSV3 = 0x00001000


# Бит указывает маскированы ли данные.
DATA_MASKING = 0b10000000

class OpCodes:
    # opcode расположен в последних 4 битах байта.
    POS = 0x00001111

    OP_TEXT = 0x1
    OP_BINARY = 0x2
    OP_PING = 0x9
    OP_PONG = 0xA
    OP_ADDIT_FRAME = 0x0



def iter_loop(iterable):
    """
        Бесконечная итерация
    """

    while True:
        for item in iterable:
            yield item

    return


def read_frame(data: bytes):
    """
        Метод парсит входящий фрейм и отдает контент
    """

    reader = memoryview(data)

    # Читаем первые два байта сообщения
    byte1, byte2 = reader[0:2]

    fin = byte1 & FIN

    op_code = byte1 & OpCodes.POS

    # Читаем второй байт сообщения.
    # В нем находится длина последующего контента
    lenght = byte2 & 0b01111111

    mask = byte2 & DATA_MASKING

    if mask:
        mask = reader[2:6]
        masked_data = reader[6: 6 + lenght + 1]
        mask = iter_loop(mask)

        data = b''
        for bt in masked_data:
            mk = mask.__next__()
            data += (bt ^ mk).to_bytes(1, 'big')

    else:
        data = reader[2: 2 + lenght + 1]

    print(data.decode('utf-8'))
    return data.decode('utf-8')