from flask import session, abort

from Models.Session import SessionRepository


def check_session(user_id: int, sessionkey: str = None):
    sessionkey = sessionkey or session.get("sessionkey")
    session_user_id = SessionRepository().get(sessionkey).userID
    if user_id != session_user_id:
        abort(401)
