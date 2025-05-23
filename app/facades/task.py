from typing import Union

from app.models import TaskRepository
from app.services.calculator import Calc, Difficulty, Duration
from app.core.abstractions import FacadeAbstract
from app.schemas.api_models import task_dto


class TaskFacade(FacadeAbstract):
    repo = TaskRepository
    dto = task_dto
    entry: repo.model

    def __init__(self, obj: repo.model):
        super().__init__(obj)

    @classmethod
    def get(cls, ID: int) -> "TaskFacade":
        return cls(cls.repo().get(ID))

    @classmethod
    def create(cls, userID: int, title: str) -> "TaskFacade":
        return cls(cls.repo().create(userID, title))

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

        self.repo.edit(
            self.entry,
            xp=Calc.xp(difficulty),
            cash=Calc.cash(duration)
        )

    def complete(self):
        self.repo.edit(self.entry, status="Done")

    def asdict(self):
        res = self.__dict__
        return res
