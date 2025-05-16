from flask import Response
from flask_restx import Namespace, Resource as Controller, abort

from app.core.App import api
from app.facades import User

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

        User.get(user_id).repo.delete()
