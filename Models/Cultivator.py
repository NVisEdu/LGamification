from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped as Type, mapped_column as props, relationship as rltn

from Models.User import UserModel
from app_database import database as appdb

from interface import implements
from interfaces import IRepository


class CultivatorModel(appdb.modelBase):
    __tablename__ = 'cultivators'

    title:  Type[str] = props(String(32))
    is_enemy: Type[bool]
    hp:     Type[int]
    sp:     Type[int]

    stats_id:  Type[int] = props(ForeignKey("stats.id"))
    skills_id: Type[int] = props(ForeignKey("skills.id"))

    user_id: Type[int]   = props(ForeignKey("users.id"))
    user:   Type["UserModel"] = rltn("User", back_populates="cultivators")


class CultivatorRepository(implements(IRepository)):
    _Model = CultivatorModel
