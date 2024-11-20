from flask import make_response, make_response as resp, request, abort, Response, session

from Models.Session import SessionRepository
from Services.Auth import login_check, register_check
from Facades.User import UserFacade as User

from flask_restx import Resource as Controller, Namespace, fields, reqparse

from App import api, logger


ns = Namespace("auth")
logger.debug("Namespace created: \"Auth\"")


auth_parser = reqparse.RequestParser()
auth_parser.add_argument('username', location='form', type=str, required=True)
auth_parser.add_argument('password', location='form', type=str, required=True)


@ns.route("/register")
class Resister(Controller):
    @ns.expect(auth_parser, validate=True)
    # @api.marshal_with(User.marshal)
    def post(self) -> Response:
        # username: str = request.form.get("username")
        # password: str = request.form.get("password")

        args = auth_parser.parse_args()
        username: str = args["username"]
        password: str = args["password"]

        if error := register_check(username, password):
            abort(error["code"], error["msg"])

        new_user = User.Repo.create(username=username, password=password)
        if not new_user:
            abort(500)

        # return new_user
        return resp()


@ns.route("/login")
class Login(Controller):
    @ns.expect(auth_parser, validate=True)
    def post(self) -> Response:
        if session.get("sessionkey"):
            abort(400, "Already logged in.")

        args = auth_parser.parse_args()
        username: str = args["username"]
        password: str = args["password"]

        user, error = login_check(username, password)
        if error:
            abort(error["code"], error["msg"])

        sessionkey = SessionRepository().create(user.entry.ID).key

        if not sessionkey:
            abort(500)

        session["sessionkey"] = sessionkey
        return resp()


@ns.route("/logout")
class Logout(Controller):
    @staticmethod
    def post() -> Response:
        sessionkey = session.get("sessionkey")
        if not sessionkey:
            return resp("No sessionkey was found.")

        SessionRepository().delete_session_by_key(sessionkey)
        session.pop("sessionkey")
        return resp()


@ns.route("/reset-password")
class ResetPassword(Controller):
    @staticmethod
    def post() -> Response:
        return abort(501)  # Not Implemented
