from abc import ABC, abstractmethod

from sqlalchemy.orm import (Mapped as Type,
                            mapped_column as props,
                            DeclarativeBase)


class ModelBase(DeclarativeBase):
    ID: Type[int] = props(primary_key=True)

    @abstractmethod
    def __call__(self, *args, **kwargs):
        ...
