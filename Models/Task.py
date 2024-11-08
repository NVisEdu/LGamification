import sqlalchemy as db
from interface import implements
from sqlalchemy import ForeignKey as FK, DateTime, String
from sqlalchemy.orm import Mapped as Type, mapped_column as props, relationship as rltn

from Models.ModelBase import ModelBase
from Models.Objective import ObjectiveModel
from Models.utility import cascade_relation as reltn
from app_database import database as appdb
from design_patterns import Singleton
# from interfaces import IRepository


class TaskModel(ModelBase):
    __tablename__ = "tasks"

    title:  Type[str] = props(String(32))
    status: Type[str]  # Set(ToDo, Doing, Done)
    due = DateTime()

    xp:   Type[int]
    cash: Type[int]

    difficulty: Type[str]  # Set(Easy,  Normal, Medium, Hard, Very hard)
    duration:   Type[str]  # Set(Quick, Normal, Medium, Long, Very long)

    userID:      Type[int] = props(FK("users.ID",      ondelete="CASCADE"))
    objectiveID: Type[int] = props(FK(ObjectiveModel.ID, ondelete="CASCADE"))

    # Relationships
    user:   Type["UserModel"] = rltn()
    tags:   Type[list["TagModel"]]   = reltn()
    skills: Type[list["SkillModel"]] = reltn()

    def __init__(self,
                 userID: int,
                 title: None | str = None):
        super().__init__()
        self.userID = userID
        self.title  = title


class TaskRepository(Singleton):
    _Model = TaskModel

    def get(self, ID: int):
        return appdb.session.execute(
            db.select(self._Model)
            .where(self._Model.ID == ID)
        ).one_or_none()

    def create(self, userID) -> TaskModel:
        task = self._Model(userID)
        appdb.session.add(task)
        return task
