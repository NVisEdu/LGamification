import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app.models import (TaskModel,
                        TaskRepository,
                        UserRepository,
                        ActionLogRepository)
from app.core.abstractions import FacadeAbstract
from app.schemas.api_models import user_dto


class UserFacade(FacadeAbstract):
    repo = UserRepository()
    dto = user_dto
    entry: repo.model

    def __init__(self, obj: repo.model):
        super().__init__(obj)

    @classmethod
    def get(cls, ID: int) -> "UserFacade":
        return UserFacade( cls.repo.get(ID) )

    @classmethod
    def get_by_name(cls, name: str):
        return cls( cls.repo.get_by_name(name) )

    def to_dict(self):
        res = self.__dict__
        del res["password"]
        return res

    def delete(self):
        self.repo.delete(self.entry)
        # ToDo delete all sessions

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
