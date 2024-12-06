from typing import Union

from werkzeug.security import generate_password_hash, check_password_hash

from Models import TaskRepository
from Services.Calculator import Calc, Difficulty, Duration
from abstractions import FacadeAbstract
from Controllers.api_models import task_dto


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

        self.Repo.edit(
            self.entry,
            xp=Calc.xp(difficulty),
            cash=Calc.cash(duration)
        )

    def complete(self):
        self.Repo.edit(self.entry, status="Done")

    def to_dict(self):
        res = self.__dict__
        return res
