from collections.abc import Sequence
from functools import wraps

from flask import abort, request

from app.models import SessionRepository
from app.core.abstractions import FacadeAbstract
from app.database.db_init import database


def check_session(user_id: int, sessionkey: str = None):
    sessionkey = sessionkey or request.headers.get("Authorization")
    session_user = SessionRepository().get(sessionkey)
    if not (session_user and int(user_id) == session_user.userID):
        abort(401)


def edit_model_fields(facade: FacadeAbstract, field_names: Sequence, data: dict):
    for field_name in field_names:
        if field_name in data and data[field_name] is not None:
            setattr(facade.entry, field_name, data[field_name])
    database.session.commit()
    return facade


def session_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        userID = kwargs.get("userID")
        check_session(userID)
        return f(*args, **kwargs)
    return wrapper


def require_args(*names: str) -> tuple[str, ...]:
    res = []
    for name in names:
        value = request.args.get(name)
        if not value:
            abort(400, f"Missing required argument: {name}")
        res.append(value)
    return tuple(res)
