from flask import request, make_response as resp, jsonify, Response
from flask_restx import Resource, Namespace


from Models.Task import TaskRepository


ns = Namespace("task")


@ns.route("/")
class Task(Resource):
    @staticmethod
    def post(userID: int):
        return TaskRepository().create(userID)
