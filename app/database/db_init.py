import sqlalchemy.orm

from app.core.App import logger
from app.models.base import ModelBase
from app.core.design_patterns import Singleton


class Database(Singleton):
    engine = sqlalchemy.create_engine(
        url="sqlite:///data.db",
        echo=True
    )
    session = sqlalchemy.orm.sessionmaker(bind=engine)()
    modelBase = ModelBase
    default_cascade = "save-update, merge, delete, delete-orphan"

    def __init__(self):
        self.session.execute(
            sqlalchemy.text("PRAGMA foreign_keys=ON")
        )

        self.create_tables()

    def create_tables(self):
        logger.debug("CREATING DATABASE TABLES...")
        self.modelBase.metadata.create_all(bind=self.engine)


database = Database()
