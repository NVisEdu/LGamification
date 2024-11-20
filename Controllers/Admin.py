from flask import Response
from flask.helpers import resp as resp
from flask_restx import Namespace, Resource as Controller, abort

from App import api
from Services.funcs import check_session
from Facades.User import UserFacade as User

ns = Namespace("admin")


@ns.route("/user/<user_id>")
class User(Controller):
    @api.marshal_with(User.dto)
    def get(self, user_id: int):
        abort(501)  # Not Implemented

        # ToDo

    def put(self, user_id: int) -> Response:
        abort(501)  # Not Implemented

        # ToDo

    def delete(self, user_id: int) -> Response:
        abort(501)  # Not Implemented

        # ToDo

        User.get(user_id).Repo.delete()
