import sqlalchemy as db
from sqlalchemy import ForeignKey as FK, DateTime, String
from sqlalchemy.orm import Mapped as Type, mapped_column as props, relationship as rltn

from Models.ModelBase import ModelBase
from Models.Objective import ObjectiveModel
from Models.utility import cascade_relation as reltn
from app_database import database
from design_patterns import Singleton


class TaskModel(ModelBase):
    __tablename__ = "tasks"

    title:  Type[str] = props(String(32))
    status: Type[str]  # Set(To-do, Doing, Done)
    due = props(DateTime, nullable=True)

    xp:   Type[int] = props(nullable=True)
    cash: Type[int] = props(nullable=True)

    difficulty: Type[str] = props(nullable=True)  # Set(Easy,  Normal, Medium, Hard, Very hard)
    duration:   Type[str] = props(nullable=True)  # Set(Quick, Normal, Medium, Long, Very long)

    userID:      Type[int] = props(FK("users.ID",      ondelete="CASCADE"))

    # Relationships
    # user:   Type["UserModel"] = rltn()
    # tags:   Type[list["TagModel"]]   = reltn()
    # skills: Type[list["SkillModel"]] = reltn()

    def __init__(self,
                 userID: int,
                 title: None | str = None,
                 status: str = "ToDo"):
        super().__init__()
        self.userID = userID
        self.title  = title
        self.status = status


class TaskRepository(Singleton):
    _Model = TaskModel

    @property
    def model(self):
        return self._Model

    def get(self, ID: int):
        return database.session.execute(
            db.select(self._Model)
            .where(self._Model.ID == ID)
        ).scalar_one_or_none()

    def create(self, userID, title) -> TaskModel:
        task = self._Model(userID, title)
        task.status = "ToDo"
        database.session.add(task)
        database.session.commit()
        return task

    def get_all_by_user(self, userID: int) -> tuple[_Model]:
        res = database.session.execute(
            db.select(self._Model)
            .where(self._Model.userID == int(userID))
        ).scalars().all()
        return res

    @staticmethod
    def edit(task: _Model, **kwargs):
        for prop in kwargs.keys():
            setattr(task, prop, kwargs[prop])
        database.session.commit()
