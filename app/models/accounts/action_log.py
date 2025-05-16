import datetime

from sqlalchemy import String, DateTime, ForeignKey as FK, select
from sqlalchemy.orm import Mapped as Type, mapped_column as props

from app.core.abstractions import RepositoryGettableAbstract
from app.database.db_init import database as appdb

from app.core.design_patterns import Singleton

dbs = appdb.session


class ActionLogModel(appdb.modelBase):
    __tablename__ = 'action_logs'

    title:  Type[str] = props(String(32))
    date:   Type[DateTime] = props(DateTime, nullable=False)

    cash:   Type[int] = props(nullable=True)
    xp:     Type[int] = props(nullable=True)
    hp:     Type[int] = props(nullable=True)
    sp:     Type[int] = props(nullable=True)

    userID: Type[int] = props(FK("users.ID"))
    # user: Type["UserModel"] = rltn("User", back_populates="action_logs")

    def __init__(self, userID: int,
                 title: str,
                 date: datetime.datetime = None,
                 cash: int = None,
                 xp: int = None,
                 hp: int = None,
                 sp: int = None):
        self.userID = userID

        if date is None:
            date = datetime.datetime.now(datetime.timezone.utc)

        self.title = title
        self.date  = date
        self.cash = cash
        self.xp = xp
        self.hp = hp
        self.sp = sp


class ActionLogRepository(RepositoryGettableAbstract, Singleton):
    model = ActionLogModel

    def get(self, ID: int):
        return super().get(ID)

    # def create(self,
    #            userID: int,
    #            title: str,
    #            date: datetime.datetime = None,
    #            cash: int = None,
    #            xp: int = None,
    #            hp: int = None,
    #            sp: int = None
    #            ):
    #     return super().create(
    #         userID=userID,
    #         title=title,
    #         date=date,
    #         cash=cash,
    #         xp=xp,
    #         hp=hp,
    #         sp=sp
    #     )

    @staticmethod
    def get_all_by_user(userID: int, limit: int = 100) -> tuple[model]:
        res = dbs.execute(
            select(ActionLogModel)
            .where(ActionLogModel.userID == int(userID)).limit(limit)
        ).scalars().all()
        return res

    @staticmethod
    def delete(entry: model):
        dbs.delete(entry)
        dbs.commit()
