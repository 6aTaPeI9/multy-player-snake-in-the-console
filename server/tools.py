# -*- coding: utf-8 -*-
"""
    Модуль вспомогательных методов 
"""


def get_as_list(data: dict, key: str):
    """
        Получение значения из словаря в списке
    """
    res = data.get(key)

    if not isinstance(res, list):
        res = [res]

    return res
