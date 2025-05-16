from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped as Type, mapped_column as props

from app.database.db_init import database as appdb


class StatModel(appdb.modelBase):
    __tablename__ = 'stats'

    title: Type[str] = props(String(32))
    level: Type[int]
    score: Type[int]

    user_id: Type[int] = props(ForeignKey("users.ID"))
    # user: Type["User"] = rltn("User", back_populates="stats")
