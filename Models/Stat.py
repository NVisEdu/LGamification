from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped as Type, mapped_column as props, relationship as rltn

from app_database import database as appdb


class StatModel(appdb.modelBase):
    __tablename__ = 'stats'

    id: Type[int] = props(Integer, primary_key=True)
    title: Type[str] = props(String(32))
    level: Type[int]
    score: Type[int]

    user_id: Type[int] = props(ForeignKey("users.id"))
    user: Type["User"] = rltn("User", back_populates="stats")
