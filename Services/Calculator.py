from enum import Enum, auto


class Calc:

    @staticmethod
    def cash(duration: "Duration") -> int:
        return duration.value*15

    @staticmethod
    def xp(difficulty: "Difficulty") -> int:
        return -10 + difficulty.value*15

    @staticmethod
    def cash_xp_sum(difficulty: "Difficulty", duration: "Duration") -> int:
        return Calc.xp(difficulty) + Calc.cash(duration)


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
