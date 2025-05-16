import secrets

from sqlalchemy import ForeignKey as FK, delete, select
from sqlalchemy.orm import Mapped as Col, mapped_column as props

from app.core.abstractions import RepositoryAbstract
from app.database.db_init import database as appdb

dbs = appdb.session


class SessionModel(appdb.modelBase):
    __tablename__ = 'sessions'
    key:    Col[str] = props(unique=True, nullable=False)
    userID: Col[int] = props(FK("users.ID", ondelete="CASCADE"), nullable=False)

    # user: Col['UserModel'] = rltn("UserModel", back_populates="session")

    def __init__(self, userID: int, key: str = None):
        self.userID = userID
        self.key    = key or secrets.token_urlsafe(16)


class SessionRepository(RepositoryAbstract):
    model = SessionModel

    def get(self, sessionkey) -> model | None:
        return dbs.execute(
            select(self.model)
            .where(self.model.key == sessionkey)
        ).scalar_one_or_none()

    def create(self, userID) -> model:
        return super().create(userID)

    def delete_session_by_key(self, sessionkey: str) -> bool:
        dbs.execute(
            delete(self.model)
            .where(self.model.key == sessionkey)
        )
        dbs.commit()
        return True
