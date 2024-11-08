from Models.Session import SessionRepository
from Models.User import UserRepository


def login_check(username: str, password: str) -> (str, dict):
    if not username or not password:
        return None, dict(
            code=400,
            msg="No parameters (username and/or password) given."
        )

    user = UserRepository().get_by_name(username)

    if not user or not user.check_password(password):
        return None, dict(
            code=00,
            msg="Invalid username or password."
        )

    return user


def register_check(username: str, password: str) -> (str, dict):
    if not username or not password:
        return None, dict(
            code=400,
            msg="No parameters (username and/or password) given."
        )

    if username == "ADMIN":
        return None, dict(
            code=403,
            msg="Cannot register own ADMIN account."
        )

    if len(password) < 5:
        return None, dict(
            code=400,
            msg="The password is too short: Password needs to be longer than 4 characters "
                "(like I really care lol bro)"
        )

    if UserRepository().is_username_taken(username):
        return None, dict(
            code=409,
            msg="Such user already exists. Please choose another username or login instead."
        )
