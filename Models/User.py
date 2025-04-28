from typing import cast

from sqlalchemy import String, select
from sqlalchemy.orm import (Mapped as Col,
                            mapped_column as props,
                            relationship as rltn)

from abstractions import RepositoryGettableAbstract
from app_database import database as appdb

from werkzeug.security import generate_password_hash

# from interfaces import IFacade

dbs = appdb.session


class UserModel(appdb.modelBase):
    __tablename__ = 'users'

    username: Col[str] = props(String(16))
    password: Col[str] = props(String(32))
    nickname: Col[str|None] = props(String(32), nullable=True)
    pfp:      Col[str|None] = props(String(32), nullable=True)

    lvl:      Col[int]
    xp:       Col[int]
    cash:     Col[int]
    hp:       Col[int]
    max_hp:   Col[int]

    # cultivators: Col[list['CultivatorModel']] = rltn("Models.Cultivator.CultivatorModel",
    #                                                  back_populates="user", lazy='dynamic')
    # stats:       Col[list['StatModel']]       = rltn("Models.Stat.StatModel",
    #                                                  back_populates="user", lazy='dynamic')
    # skills:      Col[list['SkillModel']]      = rltn("Models.Skill.SkillModel",
    #                                                  back_populates="user", lazy='dynamic')
    # dailies:     Col[list['DailieModel']]     = rltn("Models.Dailie.DailieModel",
    #                                                  back_populates="user", lazy='dynamic')
    # goals:       Col[list['GoalModel']]       = rltn("Models.Goal.GoalModel",
    #                                                  back_populates="user", lazy='dynamic')
    # objectives:  Col[list['ObjectiveModel']]  = rltn("Models.Objective.ObjectiveModel",
    #                                                  back_populates="user", lazy='dynamic')
    # action_logs: Col[list['ActionLogModel']]  = rltn("Models.ActionLog.ActionLogModel",
    #                                                  back_populates="user", lazy='dynamic')

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = generate_password_hash(password)
        self.pfp = None
        self.lvl = 0
        self.xp = 0
        self.cash = 100
        self.max_hp = 100
        self.hp = 100


class UserRepository(RepositoryGettableAbstract):
    _Model = UserModel

    @property
    def model(self):
        return self._Model

    def get(self, ID: int):
        return cast( self._Model, super().get(ID) )

    @staticmethod
    def delete(user: UserModel):
        dbs.delete(user)
        dbs.commit()

    def create(self, username: str, password: str) -> "_Model":
        res = self._Model(username, password)
        dbs.add(res)
        dbs.commit()
        return res

    def get_by_name(self, username: str) -> _Model:
        return dbs.execute(
            select(self._Model)
            .where(self._Model.username == username)
        ).scalar_one_or_none()

    def is_username_taken(self, name: str) -> bool:
        return True if self.get_by_name(name) else False
