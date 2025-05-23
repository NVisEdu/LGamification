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

    def asdict(self) -> dict:
        ...


@dataclass
class FacadeAbstract(ABC, IFacade):
    repo: RepositoryAbstract
    dto: flask_restx.Model
    entry: ModelBase

    @classproperty
    def model(self):
        return self.repo.model

    def __init__(self, obj: "model"):
        self.entry = obj

    @staticmethod
    def __check_if_attr_is_repo_or_dto(name):
        if name in ("repo", "dto"):
            raise AttributeError(f"{name} is a read-only class attribute")

    def __setattr__(self, name, value):
        self.__check_if_attr_is_repo_or_dto(name)
        super().__setattr__(name, value)

    def __delattr__(self, name):
        self.__check_if_attr_is_repo_or_dto(name)
        super().__delattr__(name)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not hasattr(cls, 'repo') or not hasattr(cls, 'dto'):
            raise TypeError(f"{cls.__name__} must define class-level 'repo' and 'dto' attributes")

        def frozen_setattr(cls_, name, value):
            cls.__check_if_attr_is_repo_or_dto(name)
            super(cls_, cls_).__setattr__(name, value)

        cls.__setattr__ = classmethod(frozen_setattr)


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
