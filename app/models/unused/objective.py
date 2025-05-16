from sqlalchemy import ForeignKey as FK, String, DateTime
from sqlalchemy.orm import Mapped as Type, mapped_column as props

from app.database.db_init import database as appdb


class ObjectiveModel(appdb.modelBase):
    __tablename__ = 'objectives'

    title: Type[str]  = props(String(32))
    status: Type[str] = props(String(16))  # Set(To-do, Doing, Done)
    due = DateTime()

    xp: Type[int]
    cash: Type[int]

    difficulty: Type[str]  # Set(Easy, Normal, Medium, Hard, Very hard)
    duration:   Type[str]  # Set(Quick, Normal, Medium, Long, Very long)

    user_id: Type[int] = props(FK("users.ID"))

    # user:  Type["UserModel"] = rltn("UserModel", back_populates="objectives",
    #                                 passive_deletes=True, cascade=appdb.default_cascade)
    # tags:   Type["TagModel"]   = rltn("TagModel", back_populates="objectives",
    #                                   passive_deletes=True, cascade=appdb.default_cascade)
    # skills: Type["SkillModel"] = rltn("SkillModel", back_populates="objectives",
    #                                   passive_deletes=True, cascade=appdb.default_cascade)

    def __init__(self,
                 title: None | str = None):
        super().__init__()
        self.title = title
