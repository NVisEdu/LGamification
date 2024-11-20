from abstractions import RepositoryAbstract
from app_database import database as appdb

from sqlalchemy.orm import Mapped as Col, mapped_column as props, relationship as rltn
from sqlalchemy import Integer, String, DateTime, Enum, ForeignKey


class DailieModel(appdb.modelBase):
    __tablename__ = 'dailies'

    title: Col[str] = props(String(32))
    status: Col[Enum] = props(Enum("ToDo", "Done", name="dailie_status"))
    xp: Col[int]
    cash: Col[int]
    due: Col[DateTime] = props(DateTime)
        #  = props(DateTime)
    user_id: Col[int] = props(ForeignKey("users.ID"), nullable=False)
    # user = rltn("UserModel", back_populates="dailies")


class DailieRepository(RepositoryAbstract):
    _Model = DailieModel
