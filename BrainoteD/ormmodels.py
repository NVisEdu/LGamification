import secrets
import sqlalchemy as db

from app_database import database

default_cascade = "save-update, merge, delete, delete-orphan"


class Session(database.modelBase):
    key     = db.Column("key", db.String, unique=True, nullable=True)
    userID  = db.Column("user_id", db.Integer,
                        db.ForeignKey("users.id", ondelete="CASCADE"),
                        nullable=False)

    # Relationships
    user = db.orm.Relationship("User", back_populates="sessions")

    def __init__(self, userID: str, key: str = None):
        if not key: key = secrets.token_urlsafe(16)
        self.key    = key
        self.userID = userID


class NoteItem(database.modelBase):
    __tablename__ = "noteitems"

    # Columns
    ID       = db.Column("id", db.Integer, primary_key=True)
    noteID   = db.Column("note_id", db.Integer,
                         db.ForeignKey("notes.id", ondelete="CASCADE"),
                         nullable=False)
    index    = db.Column("index", db.Integer,
                         unique=True, autoincrement=True, nullable=True)
    content  = db.Column("content", db.String)
    itemtype = db.Column("itemtype", db.String(16))

    # Relationships
    note = db.orm.Relationship("Note", back_populates="items")

    def __init__(self,
                 noteID:    int,
                 content:   str,
                 itemtype:  str = "Text",
                 index:     int | None = None):
        self.noteID     = noteID
        self.content    = content
        self.itemtype   = itemtype
        self.index      = index

    def update_item(self,
                    content:  str | None = None,
                    itemtype: str | None = None,
                    ):
        self.content    = content   if content  is not None else self.content
        self.itemtype   = itemtype  if itemtype is not None else self.itemtype

    def drag_item(self, index: int):
        self.index = int(index)

    def move_item(self, noteID: int):
        self.noteID = int(noteID)

    def __repr__(self):
        return str(dict(
            itemID=self.ID,
            content=self.content,
            itemtype=self.itemtype,
            noteID=self.noteID
        ))
