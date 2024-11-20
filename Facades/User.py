import datetime
from typing import cast

from werkzeug.security import generate_password_hash, check_password_hash

from Facades.Journal import JournalFacade
from Models.Task import TaskModel, TaskRepository
from Models.User import UserModel, UserRepository
from abstractions import FacadeAbstract
from api_models import user_dto
from app_database import database


class UserFacade(FacadeAbstract):
    Repo = UserRepository()
    model = Repo.model
    entry: model
    dto = user_dto

    def __init__(self, obj: model):
        self.entry = obj

    @staticmethod
    def get(ID: int) -> "UserFacade":
        self = UserFacade
        return UserFacade( self.Repo.get(ID) )

    @staticmethod
    def get_by_name(name: str):
        self = UserFacade
        return UserFacade( self.Repo.get_by_name(name) )

    def to_dict(self):
        res = self.__dict__
        del res["password"]
        return res

    def log(self,
            title: str,
            date: datetime.datetime = None,
            cash: int = None,
            xp: int = None,
            hp: int = None,
            sp: int = None):
        entry = JournalFacade.model(self.entry.ID, title)

        entry.date = date or datetime.datetime.now(datetime.UTC)
        entry.cash = cash
        entry.xp = xp
        entry.hp = hp
        entry.sp = sp

        database.session.add(entry)
        database.session.commit()

    def create_task(self) -> "TaskModel":
        return TaskRepository().create(self.entry.ID)

    def set_password(self, val):
        self.entry.password = generate_password_hash(val)

    def check_password(self, password) -> bool:
        return check_password_hash(self.entry.password, password)
