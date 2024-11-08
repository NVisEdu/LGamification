import enum
from enum import Enum, auto


class Difficulty(Enum):
    Easy    = auto()
    Normal  = auto()
    Medium  = auto()
    Hard    = auto()
    VeryHard = auto()


class Duration(Enum):
    Quick   = auto()
    Normal  = auto()
    Medium  = auto()
    Long    = auto()
    VeryLong = auto()


class Calc:

    @staticmethod
    def cash_calculator(duration: Duration) -> int:
        return  -5 + duration.value*15

    @staticmethod
    def xp_calculator(difficulty: Difficulty) -> int:
        return -10 + difficulty.value*15

    @staticmethod
    def total_calculator(difficulty: Difficulty, duration: Duration) -> int:
        return Calc.xp_calculator(difficulty) + Calc.cash_calculator(duration)
