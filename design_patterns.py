from abc import ABC


class Singleton(ABC):
    instance: "Singleton" = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance
