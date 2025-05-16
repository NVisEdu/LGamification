from app.core.App import api
from app.services.utils import check_session, edit_model_fields

from flask import request
from flask_restx import Resource as Controller, Namespace, fields
from app.facades import Journal as ActionLog

ns = Namespace("user/<int:userID>/journal")


@ns.route("/")
class Journal(Controller):
    @api.marshal_list_with(ActionLog.dto)
    def get(self, userID: int) -> tuple[ActionLog.model]:
        check_session(userID)

        return ActionLog.get_by_user(userID)


@ns.route("/<int:entryID>")
class JournalEntry(Controller):
    @api.marshal_list_with(ActionLog.dto)
    def get(self, userID: int, entryID) -> tuple[ActionLog.model]:
        check_session(userID)

        return ActionLog.get(entryID).entry

    journalput_dict = {
        "title": fields.String(required=False),
        "date": fields.DateTime(required=False),
        "xp":   fields.Integer(required=False),
        "cash": fields.Integer(required=False),
        "hp":   fields.Integer(required=False),
        "sp":   fields.Integer(required=False),
    }
    journalput_dto = ns.model("Journaledit", journalput_dict)

    @ns.expect(journalput_dto)
    @api.marshal_list_with(ActionLog.dto)
    def put(self, userID: int, entryID) -> ActionLog.model:
        check_session(userID)

        return edit_model_fields(
            facade=ActionLog.get(entryID),
            field_names=list(self.journalput_dict.keys()),
            data=request.json
        ).entry

    @staticmethod
    def delete(userID: int, entryID):
        check_session(userID)

        ActionLog.get(entryID).delete()
