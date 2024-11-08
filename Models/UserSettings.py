import sqlalchemy as db

from app_database import database as appdb


class UserSettings(appdb.modelBase):
    __tablename__ = "user_settings"

    language = db.Column(db.String(8))

    def __init__(self):
        self.language = "UA"
