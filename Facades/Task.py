from typing import cast, Union

from werkzeug.security import generate_password_hash, check_password_hash

from Models.Task import TaskModel, TaskRepository
from Services.Calculator import Calc, Difficulty, Duration
from abstractions import FacadeAbstract
from api_models import task_dto
from app_database import database


class TaskFacade(FacadeAbstract):
    Repo = TaskRepository()
    model = Repo.model
    entry: model
    dto = task_dto

    def __init__(self, obj: model):
        self.entry = obj

    @staticmethod
    def get(ID: int) -> "TaskFacade":
        self = TaskFacade
        return TaskFacade(self.Repo.get(ID))

    @staticmethod
    def create(userID: int, title: str) -> "TaskFacade":
        return TaskFacade(TaskFacade.Repo.create(userID, title))

    def calc_rewards(self,
                     difficulty: Union[None, str, "Difficulty"] = None,
                     duration:   Union[None, str, "Duration"]   = None
                     ):
        if difficulty is None:
            difficulty = self.entry.difficulty
        if duration is None:
            duration = self.entry.duration

        if type(difficulty) is str:
            difficulty = Difficulty[difficulty]
        if type(duration) is str:
            duration = Duration[duration]

        self.entry.xp   = Calc.xp(difficulty)
        self.entry.cash = Calc.cash(duration)

        database.session.commit()

    def complete(self):
        self.entry.status = "Done"
        database.session.commit()

    def to_dict(self):
        res = self.__dict__
        return res
