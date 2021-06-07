# -*- coding: utf-8 -*-
"""
    Константы для работы с клавишами
"""

# Поддерживаемые клавиши
class Keys:
    # Стрелочки
    ARROW_UP = 38
    ARROW_DOWN = 40
    ARROW_LEFT = 37
    ARROW_RIGH = 39

    # WASD
    UP = 87
    DOWN = 83
    LEFT = 65
    RIGHT = 68


# Действия вводимые с клавиатуры
class StepKeys:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


# Соответствие клавиши и действия
STEP_KEY = {
    Keys.ARROW_UP: StepKeys.UP,
    Keys.ARROW_DOWN: StepKeys.DOWN,
    Keys.ARROW_LEFT: StepKeys.LEFT,
    Keys.ARROW_RIGH: StepKeys.RIGHT,

    Keys.UP: StepKeys.UP,
    Keys.DOWN: StepKeys.DOWN,
    Keys.LEFT: StepKeys.LEFT,
    Keys.RIGHT: StepKeys.RIGHT
}