from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped as Type, mapped_column as props, relationship as rltn

from app_database import database as appdb


class DailieModel(appdb.modelBase):
    __tablename__ = 'dailies'

    title:  Type[str] = props(String(32))
    status: Type[str]  # Set(ToDo, Doing, Done)
    xp:     Type[int]
    cash:   Type[int]
    du = DateTime()

    user_id: Type[int] = props(ForeignKey("users.id"))
    user:   Type["UserModel"] = rltn("User", back_populates="dailies")


class DailieRepository():
    _Model = DailieModel
