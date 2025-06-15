from collections.abc import Sequence
from datetime import datetime

from flask import request, abort, make_response as resp
from flask_restx import Resource, Namespace, fields

from app.core.App import api
from app.facades.user import UserFacade
from app.services.utils import check_session, edit_model_fields, session_required, require_args
from app.facades.task import TaskFacade as Task


ns = Namespace("user/<int:userID>/tasks")


taskput_dto = ns.model("Taskedit", {
    "title": fields.String(required=False),
    "due": fields.DateTime(required=False),
    "xp": fields.Integer(required=False),
    "cash": fields.Integer(required=False),
    "difficulty": fields.String(required=False),  # Set(Easy, Normal, Medium, Hard, Very hard)
    "duration": fields.String(required=False),  # Set(Quick, Normal, Medium, Long, Very long)
    "status": fields.String(required=False),
})


@ns.route("/")
class Index(Resource):
    method_decorators = [session_required]

    @api.marshal_list_with(Task.dto)
    @api.header('sessionkey', type='string')
    def get(self, userID: int) -> Sequence:
        return list(
            Task.repo.get_all_by_user(userID)
        )

    @api.marshal_with(Task.dto)
    @api.param("title", type=str)
    @api.header('sessionkey', type='string')
    def post(self, userID: int) -> Task.model:
        title, = require_args("title")

        task = Task.create(userID, title)
        return task.entry


@ns.route("/<int:taskID>")
class TaskEntry(Resource):
    method_decorators = [session_required]

    @api.marshal_with(Task.dto)
    @api.header('sessionkey', type='string')
    def get(self, taskID: int) -> Task.model:
        return Task.get(taskID).entry

    @ns.expect(taskput_dto)
    @api.marshal_with(Task.dto)
    @api.header('sessionkey', type='string')
    def put(self, taskID: int) -> Task.model:
        data = request.json.copy()

        if "due" in data and isinstance(data["due"], str):
            try:
                data["due"] = datetime.fromisoformat(data['due'])
            except ValueError:
                abort(400, "Невірний формат дати. Використовуйте ISO 8601 (наприклад, 2025-06-22T10:59)")

        return edit_model_fields(
            facade=Task.get(taskID),
            field_names=list(taskput_dto.keys()),
            data=data
        ).entry

    @staticmethod
    def delete(taskID: int):
        Task.get(taskID).delete()

        return resp(204)


@ns.route("/<int:taskID>/calc_rewards")
class TaskCalc(Resource):
    method_decorators = [session_required]

    @api.marshal_with(Task.dto)
    @api.header('sessionkey', type='string')
    def post(self, taskID: int) -> Task.model:
        task = Task.get(taskID)

        if task.entry.difficulty is None or task.entry.duration is None:
            abort(400, "Task does not have difficulty or duration to calc rewards from.")

        task.calc_rewards()
        return task.entry


@ns.route("/<int:taskID>/complete")
class CompleteTask(Resource):
    method_decorators = [session_required]

    @staticmethod
    @api.header('sessionkey', type='string')
    def post(userID: int, taskID: int):
        task = Task.get(taskID)
        task.complete()

        user = UserFacade.get(userID)
        user.log(f"Task completed: {task.entry.title}",
                 xp=task.entry.xp,
                 cash=task.entry.cash
                 )

        return resp(204)
