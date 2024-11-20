import sqlalchemy.orm

from App import logger
from Models.ModelBase import ModelBase
from design_patterns import Singleton


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
