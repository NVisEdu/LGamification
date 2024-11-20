from flask import request, make_response as resp, Response, abort
from flask_restx import Resource as Controller, Namespace, fields

from App import api
from Services.funcs import check_session, edit_model_fields
from Facades.User import UserFacade as User

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


@ns.route("/<userID>/stats")
class Stats(Controller):
    @api.marshal_with(User.dto)
    def get(self, userID: int) -> Response:
        check_session(userID)

        return Index().get(userID)
        # Logic will be edited/added if stats will be separated from main user model


@ns.route("/<userID>/change_password")
class UserPassword(Controller):
    password_model = ns.model("ChangePassword", {
        "password": fields.String(required=True),
    })

    @ns.expect(password_model)
    def put(self, userID: int) -> Response:
        check_session(userID)

        password = str(request.form["password"])
        if not password:
            return abort(400, "No password given.")
        User.get(userID).set_password(password)

        return resp()
