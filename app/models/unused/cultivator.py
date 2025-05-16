from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import Mapped as Type, mapped_column as props

from app.core.abstractions import RepositoryGettableAbstract, dbs
from app.core.design_patterns import Singleton
from app.database.db_init import database as appdb


class CultivatorModel(appdb.modelBase):
    __tablename__ = 'cultivators'

    title:  Type[str] = props(String(32))
    is_enemy: Type[bool]
    hp:     Type[int]
    sp:     Type[int]

    statsID:  Type[int] = props(ForeignKey("stats.ID", name='fk_cultivators_statsID'))
    skillsID: Type[int] = props(ForeignKey("skills.ID", name='fk_cultivators_skillsID'))

    userID: Type[int]   = props(ForeignKey("users.ID", name='fk_cultivators_userID'))
    # user: Type["UserModel"] = rltn("User", back_populates="cultivators")


class CultivatorRepository(RepositoryGettableAbstract, Singleton):
    model = CultivatorModel

    @classmethod
    def get(cls, ID: int):
        return super().get(ID)

    @classmethod
    def create(cls, userID: int,
               title: str,
               xp_reward: int, hp_penalty: int,
               ):
        return super().create(
            userID=userID,
            title=title,
            xp=xp_reward,
            hp=hp_penalty
        )

    @classmethod
    def get_all_by_user(cls, userID: int, limit: int = 100) -> tuple[model]:
        res = dbs.execute(
            select(cls.model)
            .where(cls.model.userID == int(userID)).limit(limit)
        ).scalars().all()
        return res

    @staticmethod
    def delete(entry: model):
        dbs.delete(entry)
        dbs.commit()

    @classmethod
    def edit(cls, entry, status):
        # ToDo
        ...
