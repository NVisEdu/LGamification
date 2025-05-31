from app.core.App import api
from app.services.utils import edit_model_fields, session_required

from flask import request, make_response as resp
from flask_restx import Resource as Controller, Namespace, fields
from app.facades import Journal as ActionLog


ns = Namespace("user/<int:userID>/journal")


journalput_dto = ns.model("Journaledit", {
    "title": fields.String(required=False),
    "date": fields.DateTime(required=False),
    "xp": fields.Integer(required=False),
    "cash": fields.Integer(required=False),
    "hp": fields.Integer(required=False),
    "sp": fields.Integer(required=False),
})


@ns.route("/")
class Journal(Controller):
    method_decorators = [session_required]

    @api.marshal_list_with(ActionLog.dto)
    def get(self, userID: int) -> tuple[ActionLog.model]:
        return ActionLog.get_by_user(userID)


@ns.route("/<int:entryID>")
class JournalEntry(Controller):
    method_decorators = [session_required]

    @api.marshal_list_with(ActionLog.dto)
    def get(self, entryID) -> tuple[ActionLog.model]:
        return ActionLog.get(entryID).entry

    @ns.expect(journalput_dto)
    @api.marshal_list_with(ActionLog.dto)
    def put(self, entryID) -> ActionLog.model:
        return edit_model_fields(
            facade=ActionLog.get(entryID),
            field_names=list(journalput_dto.keys()),
            data=request.json
        ).entry

    @staticmethod
    def delete(entryID):
        ActionLog.get(entryID).delete()

        return resp(204)
