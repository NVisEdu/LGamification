from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped as Type, mapped_column as props

from app.database.db_init import database as appdb


# from interfaces import IRepository


class GoalModel(appdb.modelBase):
    __tablename__ = 'goals'

    title: Type[str] = props(String(32))
    priority: Type[str]  # Set(Low, Normal, Medium, High, Very high, Urgent)
    status: Type[str]  # Set(Planned, In progress, Achieved)
    xp: Type[int]
    cash: Type[int]
    due = DateTime()
    difficulty: Type[str]  # Set(Easy, Normal, Medium, Hard, Very hard)
    duration: Type[str]  # Set(Quick, Normal, Medium, Long, Very long)

    user_id: Type[int] = props(ForeignKey("users.ID"))
    # user: Type["UserModel"] = rltn("User", back_populates="goals")


class GoalRepository():
    model = GoalModel
