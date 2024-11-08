from flask import make_response as resp, request, abort, Response, session, jsonify

from Models.Session import SessionRepository
from Services.Auth import login_check, register_check
from Facades.User import UserFacade as User
from api_models import user_marshal

from flask_restx import Resource as Controller, Namespace, fields

from main import api

ns = Namespace("auth")


usermarshal = api.model("User", {
    # "ID": fields.Integer,
    "username": fields.String,
    # "lvl":    fields.Integer,
    # "xp":     fields.Integer,
    # "cash":   fields.Integer,
    # "hp":     fields.Integer,
    # "max_hp": fields.Integer
})


@ns.route("/register")
class Resister(Controller):
    @ns.marshal_with(usermarshal)
    def post(self) -> Response:
        username: str = request.form["username"]
        password: str = request.form["password"]

        _, error = register_check(username, password)
        if error:
            abort(error["code"], error["msg"])

        new_user = User.Repo.create(username=username, password=password)
        if not new_user:
            abort(500)

        return new_user


@ns.route("/login")
class Login(Controller):
    @staticmethod
    def post() -> Response:
        if session.get("sessionkey"):
            abort(400, "Already logged in.")

        username = str(request.form["username"])
        password = str(request.form["password"])

        user, error = login_check(username, password)
        if error:
            abort(error["code"], error["msg"])

        sessionkey = SessionRepository().create(user.ID).key

        if sessionkey:
            session["sessionkey"] = sessionkey
            return resp(200)


@ns.route("/logout")
class Logout(Controller):
    @staticmethod
    def post() -> Response:
        sessionkey = session.get("sessionkey")
        if not sessionkey:
            return resp("No sessionkey was found.")

        SessionRepository().delete_session_by_key(sessionkey)
        session.pop("sessionkey")
        return resp(200)


@ns.route("/reset-password")
class ResetPassword(Controller):
    @staticmethod
    def post() -> Response:
        return resp(501)  # Not Implemented
