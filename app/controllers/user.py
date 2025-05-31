from flask import request, make_response as resp, Response, abort
from flask_restx import Resource as Controller, Namespace, fields, marshal, Model

from app.core.App import api
from app.schemas.api_models import userdata_dto
from app.services.utils import edit_model_fields, session_required
from app.facades import User

ns = Namespace("user")


userput_dto = ns.model("Useredit", {
    "username": fields.String(required=False),
    "nickname": fields.String(required=False),
    "pfp": fields.String(required=False),
    "cash": fields.Integer(required=False),
    "xp": fields.Integer(required=False),
    "lvl": fields.Integer(required=False),
    "hp": fields.Integer(required=False)
})

change_password_dto = ns.model("ChangePassword", {
        "password": fields.String(required=True),
    })


@ns.route("/<int:userID>")
class Index(Controller):
    method_decorators = [session_required]

    @api.marshal_with(User.dto)
    def get(self, userID: int):
        return User.get(userID).entry

    @ns.expect(userput_dto)
    @api.marshal_with(User.dto)
    def put(self, userID: int) -> User.model:
        return edit_model_fields(
            facade=User.get(userID),
            field_names=list(userput_dto.keys()),
            data=request.json
        ).entry

    @staticmethod
    def delete(userID: int) -> User.model:
        User.get(userID).delete()

        return resp(204)


@ns.route("/<int:userID>/stats")
class Stats(Controller):
    method_decorators = [session_required]

    @api.marshal_with(userdata_dto)
    def get(self, userID: int) -> Response:
        return User.get(userID).entry
        # Logic will be edited/added if stats will be separated from main user model


@ns.route("/<int:userID>/change_password")
class UserPassword(Controller):
    method_decorators = [session_required]

    @ns.expect(change_password_dto)
    def put(self, userID: int) -> Response:
        password = request.json["password"]

        if not password:
            abort(400, "No password given.")
        User.get(userID).set_password(password)

        return resp()
