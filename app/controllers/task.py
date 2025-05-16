from collections.abc import Sequence

from flask import request, abort
from flask_restx import Resource, Namespace, fields

from app.core.App import api
from app.facades.user import UserFacade
from app.services.utils import check_session, edit_model_fields
from app.facades.task import TaskFacade as Task

ns = Namespace("user/<int:userID>/tasks")


user_param = ()


@ns.route("/")
class Index(Resource):
    @api.marshal_list_with(Task.dto)
    def get(self, userID: int, sessionkey) -> Sequence:
        check_session(userID, sessionkey)

        res = Task.repo.get_all_by_user(userID)
        return list(res)

    @api.marshal_with(Task.dto)
    @api.param("title", type=str)
    def post(self, userID: int, sessionkey) -> Task.model:
        check_session(userID, sessionkey)

        title = request.args.get("title")
        if not title:
            abort(400, "No title arg provided.")

        task = Task.create(userID, title)
        return task.entry


@ns.route("/<int:taskID>")
class TaskEntry(Resource):
    @api.marshal_with(Task.dto)
    def get(self, userID: int, taskID: int, sessionkey) -> Task.model:
        check_session(userID, sessionkey)

        res = Task.get(taskID)
        return res.entry

    taskput_dict = {
        "title":    fields.String(required=False),
        "due":      fields.DateTime(required=False),
        "xp":       fields.Integer(required=False),
        "cash":     fields.Integer(required=False),
        "difficulty": fields.String(required=False),  # Set(Easy, Normal, Medium, Hard, Very hard)
        "duration": fields.String(required=False),   # Set(Quick, Normal, Medium, Long, Very long)
        "status":   fields.String(required=False),
    }
    taskput_dto = ns.model("Taskedit", taskput_dict)

    @ns.expect(taskput_dto)
    @api.marshal_with(Task.dto)
    def put(self, userID: int, taskID: int, sessionkey) -> Task.model:
        check_session(userID, sessionkey)

        return edit_model_fields(
            facade=Task.get(taskID),
            field_names=list(self.taskput_dict.keys()),
            data=request.json
        ).entry


@ns.route("/<int:taskID>/calc_rewards")
class TaskCalc(Resource):
    @api.marshal_with(Task.dto)
    def post(self, userID: int, taskID: int, sessionkey) -> Task.model:
        check_session(userID, sessionkey)

        task = Task.get(taskID)

        if task.entry.difficulty is None or task.entry.duration is None:
            abort(400, "Task does not have difficulty or duration to calc rewards from.")

        task.calc_rewards()
        return task.entry


@ns.route("/<int:taskID>/complete")
class CompleteTask(Resource):
    @staticmethod
    def post(userID: int, taskID: int, sessionkey):
        check_session(userID, sessionkey)

        task = Task.get(taskID)
        task.complete()

        user = UserFacade.get(userID)
        user.log(f"Task completed: {task.entry.title}",
                 xp=task.entry.xp,
                 cash=task.entry.cash
                 )
