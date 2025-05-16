import sqlalchemy as db

from app.database.db_init import database as appdb


class TagModel(appdb.modelBase):
    __tablename__ = "tags"

    # Columns
    ID     = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(16))
    userID = db.Column(db.Integer,
                       db.ForeignKey("users.ID", ondelete="CASCADE")
                       )

    # Relationships
    # user = db.orm.Relationship("User", back_populates="tasks")
