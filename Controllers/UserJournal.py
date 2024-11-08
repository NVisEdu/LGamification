from Controllers.funcs import check_session
from Models.ActionLog import ActionLogFacade, ActionLogRepository

from flask import request, make_response as resp, jsonify, Response, abort
from flask_restx import Resource as Controller, Namespace

from Models.User import UserRepository
from Facades.User import UserFacade

ns = Namespace("user/<user_id>/journal")


@ns.route("/")
class Journal(Controller):
    @staticmethod
    def get(user_id: int) -> Response:
        check_session(user_id)

        user = UserFacade.get(user_id)
        res  = ActionLogRepository.get_tuple(user.ID)
        return resp(jsonify(res))

        # ToDo test this endpoint
