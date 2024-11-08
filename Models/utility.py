from sqlalchemy.orm import relationship


def cascade_relation(*args,
                     passive_deletes: bool = True,
                     cascade: str = "save-update, merge, delete, delete-orphan"):
    return relationship(
        *args,
        passive_deletes=passive_deletes,
        cascade=cascade
    )
