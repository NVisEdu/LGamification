from typing import cast

from werkzeug.security import generate_password_hash, check_password_hash

from Models.Task import TaskModel, TaskRepository
from Models.User import UserModel, UserRepository
from abstractions import FacadeAbstract
from api_models import user_marshal


class UserFacade(FacadeAbstract):
    model = UserModel
    Repo = UserRepository()
    entry: model
    marshal = user_marshal

    def __init__(self, obj: model):
        # self.ID = None
        self.entry = obj

    @staticmethod
    def get(ID: int) -> "UserFacade":
        return UserFacade(
            cast(UserModel, UserRepository().get(ID) )
        )

    def create_task(self) -> "TaskModel":
        return TaskRepository().create(self.entry.ID)

    def get_model(self, ID: int) -> model:
        return cast(self.model, self.Repo.get(ID))

    def to_dict(self):
        res = self.__dict__
        del res["password"]
        return res

    def set_password(self, val):
        self.model.password = generate_password_hash(val)

    def check_password(self, password) -> bool:
        return check_password_hash(self.model.password, password)
