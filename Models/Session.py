import secrets

from sqlalchemy import ForeignKey as FK, delete, select
from sqlalchemy.orm import Mapped as Col, mapped_column as props, relationship as rltn

from Models.User import UserModel
from abstractions import RepositoryAbstract
from app_database import database as appdb

dbs = appdb.session


class SessionModel(appdb.modelBase):
    __tablename__ = 'sessions'
    key:    Col[str] = props(unique=True, nullable=False)
    userID: Col[int] = props(FK("users.ID", ondelete="CASCADE"), nullable=False)

    user: Col['UserModel'] = rltn("User", back_populates="session")

    def __init__(self, userID: int, key: str = None):
        self.key    = key or secrets.token_urlsafe(16)
        self.userID = userID


class SessionRepository(RepositoryAbstract):
    _Model = SessionModel

    def get(self, sessionkey) -> _Model:
        return dbs.execute(
            select(self._Model)
            .where(self._Model.key == sessionkey)
        ).scalar_one_or_none()

    def create(self, userID) -> _Model:
        return super().create(userID)

    def delete_session_by_key(self, sessionkey: str) -> bool:
        dbs.execute(
            delete(self._Model)
            .where(self._Model.key == sessionkey)
        )
        dbs.commit()
        return True
