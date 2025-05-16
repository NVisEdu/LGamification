from abc import ABC
from dataclasses import dataclass
from typing import Protocol

import flask_restx
from sqlalchemy import select

from app.models.base import ModelBase
from app.database.db_init import database
from app.core.design_patterns import Singleton


dbs = database.session


class classproperty:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, _, owner):
        return self.fget(owner)


class RepositoryAbstract(Singleton, ABC):
    model: ModelBase

    def __init__(self):
        if not hasattr(self, 'model') or not issubclass(getattr(self, 'model', None), ModelBase):
            raise NotImplementedError(
                f"Subclasses of {self.__class__.__name__} must define a `model` "
                f"attribute that is a subclass of `ModelBase`."
            )

    @classmethod
    def create(cls, *args, **kwargs) -> "model":
        # noinspection PyCallingNonCallable
        res = cls.model(*args, **kwargs)
        dbs.add(res)
        dbs.commit()
        return res


class RepositoryGettableAbstract(RepositoryAbstract, ABC):
    @classmethod
    def get(cls, ID: int) -> "RepositoryGettableAbstract.model":
        return dbs.execute(
            select(cls.model)
            .where(cls.model.ID == ID)
        ).scalar_one_or_none()


class IFacade(Protocol):
    def commit_changes(self):
        ...

    def to_dict(self) -> dict:
        ...


@dataclass
class FacadeAbstract(ABC, IFacade):
    repo: RepositoryAbstract
    dto: flask_restx.Model

    @classproperty
    def model(self):
        return self.repo.model

    entry: ModelBase

    def __init__(self, obj: "model"):
        self.entry = obj


class FacadeAbstractOld(ABC):
    def __init__(self, entry):
        self.entry = entry
        self._fields = { k: v
                         for k, v in vars(entry).items()
                         if k not in ["password"] }

    def __getattr__(self, attr: str):
        return self._fields.get(attr)

    def __setattr__(self, attr: str, value):
        if attr == "_fields":
            super().__setattr__(attr, value)
        else:
            self._fields[attr] = value

    def commit_changes(self):
        for k, v in self._fields.items():
            setattr(self.entry, k, v)

    def to_dict(self):
        return self.__dict__
