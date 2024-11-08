from flask import request, make_response as resp, jsonify, Response
from flask_restx import Resource as Controller, Namespace

from Facades.User import UserFacade

ns = Namespace("user/<user_id>/task")


@ns.route("/")
class Task(Controller):
    @staticmethod
    def get(user_id: int):
        UserFacade.get(user_id).create_task()


@ns.route("/")
class Task(Controller):
    @staticmethod
    def post(user_id: int):
        UserFacade.get(user_id).create_task()
