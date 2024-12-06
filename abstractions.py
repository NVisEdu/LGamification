from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type, cast, Protocol

import sqlalchemy as db
import flask_restx
from sqlalchemy import select

from Models.ModelBase import ModelBase
from app_database import database
from design_patterns import Singleton

dbs = database.session


class RepositoryAbstract(Singleton, ABC):
    _Model: ModelBase

    def __init__(self):
        if not hasattr(self, '_Model') or not issubclass(getattr(self, '_Model', None), ModelBase):
            raise NotImplementedError(
                f"Subclasses of {self.__class__.__name__} must define a `_Model` "
                f"attribute that is a subclass of `ModelBase`."
            )

    def create(self, *args, **kwargs) -> "_Model":
        res = self._Model(*args, **kwargs)
        dbs.add(res)
        dbs.commit()
        return res


class RepositoryGettableAbstract(RepositoryAbstract, ABC):
    def get(self, ID: int) -> "RepositoryGettableAbstract._Model":
        return dbs.execute(
            select(self._Model)
            .where(self._Model.ID == ID)
        ).scalar_one_or_none()


class IFacade(Protocol):
    def commit_changes(self):
        ...

    def to_dict(self) -> dict:
        ...


@dataclass
class FacadeAbstract(ABC, IFacade):
    Repo: RepositoryAbstract
    model: ModelBase
    entry: type
    dto: flask_restx.Model


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
