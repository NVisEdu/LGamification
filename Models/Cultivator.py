from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped as Type, mapped_column as props, relationship as rltn

from Models.User import UserModel
from abstractions import RepositoryAbstract
from app_database import database as appdb


class CultivatorModel(appdb.modelBase):
    __tablename__ = 'cultivators'

    title:  Type[str] = props(String(32))
    is_enemy: Type[bool]
    hp:     Type[int]
    sp:     Type[int]

    stats_id:  Type[int] = props(ForeignKey("stats.ID"))
    skills_id: Type[int] = props(ForeignKey("skills.ID"))

    user_id: Type[int]   = props(ForeignKey("users.ID"))
    # user: Type["UserModel"] = rltn("User", back_populates="cultivators")


class CultivatorRepository(RepositoryAbstract):
    _Model = CultivatorModel
