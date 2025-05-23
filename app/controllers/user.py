from flask import request, make_response as resp, Response, abort
from flask_restx import Resource as Controller, Namespace, fields

from app.core.App import api
from app.schemas.api_models import userdata_dto
from app.services.utils import check_session, edit_model_fields
from app.facades import User

ns = Namespace("user")


@ns.route("/<int:userID>")
class Index(Controller):
    @api.marshal_with(User.dto)
    def get(self, userID: int):
        check_session(userID)

        user = User.get(userID).entry

        return user

    userput_dict = {
        "username": fields.String(required=False),
        "nickname": fields.String(required=False),
        "pfp":      fields.String(required=False),
        "cash":   fields.Integer(required=False),
        "xp":     fields.Integer(required=False),
        "lvl":    fields.Integer(required=False),
        "hp":     fields.Integer(required=False)
    }
    userput_dto = ns.model("Useredit", userput_dict)

    @ns.expect(userput_dto)
    @api.marshal_with(User.dto)
    def put(self, userID: int) -> User.model:
        check_session(userID)

        user = edit_model_fields(
            facade=User.get(userID),
            field_names=list(self.userput_dict.keys()),
            data=request.json
        ).entry

        return user

    @staticmethod
    def delete(userID: int) -> User.model:
        check_session(userID)

        (User.get(userID)).delete()


@ns.route("/<userID>/stats")
class Stats(Controller):
    @api.marshal_with(userdata_dto)
    def get(self, userID: int) -> Response:
        check_session(userID)

        return User.get(userID).entry
        # Logic will be edited/added if stats will be separated from main user model


@ns.route("/<userID>/change_password")
class UserPassword(Controller):
    @ns.expect(ns.model("ChangePassword", {
        "password": fields.String(required=True),
    }))
    def put(self, userID: int) -> Response:
        check_session(userID)

        password = request.json["password"]

        if not password:
            abort(400, "No password given.")
        User.get(userID).set_password(password)

        return resp()
