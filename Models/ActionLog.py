from typing import cast, override

from sqlalchemy import String, DateTime, ForeignKey as FK
from sqlalchemy.orm import Mapped as Type, mapped_column as props, relationship as rltn

from abstractions import FacadeAbstract, RepositoryGettableAbstract
from app_database import database as appdb

from interface import implements
from design_patterns import Singleton
# from interfaces import IRepository, IFacade

dbs = appdb.session


class ActionLogModel(appdb.modelBase):
    __tablename__ = 'action_logs'

    title:  Type[str] = props(String(32))
    date = DateTime()

    cash:   Type[int]
    xp:     Type[int]
    hp:     Type[int]
    sp:     Type[int]

    user_id: Type[int] = props(FK("users.ID"))
    user: Type["UserModel"] = rltn("User", back_populates="action_logs")


class ActionLogRepository(RepositoryGettableAbstract, Singleton):
    _Model = ActionLogModel

    def get(self, ID: int):
        return cast(self._Model, super().get(ID))

    @staticmethod
    def get_tuple(userID: int, limit: int = 100) -> tuple[_Model]:
        res = dbs.execute(
            dbs.select(ActionLogModel)
            .where(ActionLogModel.user_id == userID)
            .fetch(limit)
        ).all()
        return res

    @staticmethod
    def delete(user: "UserModel"):
        dbs.delete(user)

    def create(self, username: str, password: str):
        return dbs.add(
            self._Model(username, password)
        )


class ActionLogFacade(FacadeAbstract):
    _model = ActionLogModel
    _Repo = ActionLogRepository()
    entry: _model

    @staticmethod
    def get(ID: int) -> "ActionLogFacade":
        return ActionLogRepository().get(ID)
