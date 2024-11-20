import sqlalchemy as db

from sqlalchemy import ForeignKey as FK, String
from sqlalchemy.orm import Mapped as Type, mapped_column as props, relationship, relationship as rltn

from app_database import database as appdb


class SkillModel(appdb.modelBase):
    __tablename__ = 'skills'

    title:  Type[str] = props(String(32))
    level:  Type[int]
    score:  Type[int]

    userID:  Type[int] = props(FK("users.ID", ondelete="CASCADE"))

    # user:   Type["User"] = rltn("User", back_populates="skills")
