from flask import make_response as resp, abort, Response, session, request

from app.models import SessionRepository
from app.services.auth import login_check, register_check
from app.facades import User

from flask_restx import Resource as Controller, Namespace, reqparse

from app.core.App import logger


ns = Namespace("auth")
logger.debug("Namespace created: \"Auth\"")


auth_parser = reqparse.RequestParser()
auth_parser.add_argument("username", location='form', type=str, required=True)
auth_parser.add_argument("password", location='form', type=str, required=True)


@ns.route("/register")
class Resister(Controller):
    @ns.expect(auth_parser, validate=True)
    # @api.marshal_with(User.marshal)
    def post(self) -> Response:
        args = auth_parser.parse_args()
        username: str = args["username"]
        password: str = args["password"]

        if error := register_check(username, password):
            abort(error["code"], error["msg"])

        new_user = User.repo.create(username=username, password=password)
        if not new_user:
            abort(500)

        return resp( {"user_ID": new_user.ID} )


@ns.route("/login")
class Login(Controller):
    @ns.expect(auth_parser, validate=True)
    def post(self) -> Response:
        if request.headers.get("SessionKey"):
            abort(400, "Already logged in.")

        args = auth_parser.parse_args()
        username: str = args["username"]
        password: str = args["password"]

        user, error = login_check(username, password)
        if error:
            abort(error["code"], error["msg"])

        user_ID = user.entry.ID

        sessionkey = SessionRepository().create(user_ID).key

        if not sessionkey:
            abort(500)

        session["sessionkey"] = sessionkey
        return resp( {"user_ID": user_ID, "sessionkey": sessionkey} )


@ns.route("/logout")
class Logout(Controller):
    @staticmethod
    def post() -> Response:
        sessionkey = request.headers.get("Authorization")
        if not sessionkey:
            return resp("No sessionkey was found.", 401)

        SessionRepository().delete_session_by_key(sessionkey)
        request.headers.pop("sessionkey")
        return resp()


@ns.route("/reset-password")
class ResetPassword(Controller):
    @staticmethod
    def post() -> Response:
        return abort(501)  # Not Implemented
