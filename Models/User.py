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
    nickname: Col[str] = props(String(32))

    lvl:      Col[int]
    xp:       Col[int]
    cash:     Col[int]
    hp:       Col[int]
    max_hp:   Col[int]

    cultivators: Col[list['CultivatorModel']] = rltn("Cultivator", back_populates="user")
    stats:       Col[list['StatModel']]       = rltn("Stat", back_populates="user")
    skills:      Col[list['SkillModel']]      = rltn("Skill", back_populates="user")
    dailies:     Col[list['DailieModel']]     = rltn("Dailie", back_populates="user")
    goals:       Col[list['GoalModel']]       = rltn("Goal", back_populates="user")
    objectives:  Col[list['ObjectiveModel']]  = rltn("Objective", back_populates="user")
    action_logs: Col[list['ActionLogModel']]  = rltn("ActionLog", back_populates="user")

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = generate_password_hash(password)


class UserRepository(RepositoryGettableAbstract):
    _Model = UserModel

    def get(self, ID: int):
        return cast(self._Model, super().get(ID))

    @staticmethod
    def delete(user: UserModel):
        dbs.delete(user)
        dbs.commit()

    def create(self, username: str, password: str) -> _Model:
        res = dbs.add(
            self._Model(username, password)
        )
        dbs.commit()
        return res

    def get_by_name(self, username: str) -> _Model:
        return dbs.execute(
            select(self._Model)
            .where(self._Model.username == username)
        ).scalar_one_or_none()

    def is_username_taken(self, name: str) -> bool:
        return True if self.get_by_name(name) else False


