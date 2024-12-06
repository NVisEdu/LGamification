import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from Models import (TaskModel,
                    TaskRepository,
                    UserRepository,
                    ActionLogRepository)
from abstractions import FacadeAbstract
from Controllers.api_models import user_dto


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

    def log(self, title: str,
            date: datetime.datetime = None,
            cash: int = None,
            xp: int = None,
            hp: int = None,
            sp: int = None):
        ActionLogRepository().create(
            userID=self.entry.ID,
            title=title,
            date=date,
            cash=cash,
            xp=xp,
            hp=hp,
            sp=sp,
        )

    def create_task(self, title) -> "TaskModel":
        return TaskRepository.create(self.entry.ID, title)

    def set_password(self, val):
        self.entry.password = generate_password_hash(val)

    def check_password(self, password) -> bool:
        return check_password_hash(self.entry.password, password)
