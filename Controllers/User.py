from flask import request, make_response as resp, jsonify, Response, abort
from flask_restx import Resource as Controller, Namespace

from Controllers.funcs import check_session
from Facades.User import UserFacade as User

ns = Namespace("user")


@ns.route("/<user_id>")
class Index(Controller):
    # @ns.marshal_with(User.marshal)
    def get(self, user_id: int):
        check_session(user_id)

        # ToDo set specific values returned by user model (try to use restx marshal model)
        return User.get(user_id).model

    def put(self, user_id: int) -> Response:
        check_session(user_id)

        # ToDo receive values to edit

        user = User.get(user_id)
        # ToDo update user.model

        return resp(200)

    def delete(self, user_id: int) -> Response:
        return resp(501)  # Not Implemented

        check_session(user_id)

        User.get(user_id).Repo.delete()


@ns.route("/<user_id>/stats")
class Stats(Controller):
    def get(self, user_id: int) -> Response:

        return resp(501)  # Not Implemented
        # ToDo


@ns.route("/<user_id>/change_password")
class UserPassword(Controller):
    @staticmethod
    def put(user_id: int) -> Response:
        check_session(user_id)

        password = str(request.form["password"])
        if not password:
            return abort(400, "No password given.")
        User.get(user_id).set_password(password)

        return resp(200)
