import sqlalchemy as db

from sqlalchemy import ForeignKey as FK, String
from sqlalchemy.orm import Mapped as Type, mapped_column as props, relationship, relationship as rltn

from app_database import database as appdb


class Skill(appdb.modelBase):
    __tablename__ = "skills"

    # Columns
    name:  Type[str] = db.Column(String(16))
    sp:    Type[int]
    level: Type[int]

    userID: Type[int] = props(FK("users.id", ondelete="CASCADE"))

    # Relationships
    user: Type["User"] = relationship()


class SkillModel(appdb.modelBase):
    __tablename__ = 'skills'

    title:  Type[str] = props(String(32))
    level:  Type[int]
    score:  Type[int]

    user_id: Type[int] = props(FK("users.id"))
    user:   Type["User"] = rltn("User", back_populates="skills")
