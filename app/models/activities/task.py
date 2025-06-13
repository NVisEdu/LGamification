from abc import ABC

import sqlalchemy as db
from sqlalchemy import ForeignKey as FK, DateTime, String
from sqlalchemy.orm import Mapped as Type, mapped_column as props

from app.models.base import ModelBase
from app.database.db_init import database
from app.core.design_patterns import Singleton


class TaskModel(ModelBase):
    __tablename__ = "tasks"

    title:  Type[str] = props(String(32))
    status: Type[str]  # Set(Draft, To-do, Doing, Done)
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
                 status: str = "Draft"):
        super().__init__()
        self.userID = userID
        self.title  = title
        self.status = status


class TaskRepository(Singleton):
    model = TaskModel

    def get(self, ID: int):
        return database.session.execute(
            db.select(self.model)
            .where(self.model.ID == ID)
        ).scalar_one_or_none()

    @classmethod
    def create(cls, userID, title) -> TaskModel:
        task = cls.model(userID, title)
        task.status = "Draft"
        database.session.add(task)
        database.session.commit()
        return task

    @classmethod
    def get_all_by_user(cls, userID: int) -> tuple[model]:
        res = database.session.execute(
            db.select(cls.model)
            .where(cls.model.userID == int(userID))
        ).scalars().all()
        return res

    @staticmethod
    def edit(task: model, **kwargs):
        for prop in kwargs.keys():
            setattr(task, prop, kwargs[prop])
        database.session.commit()
