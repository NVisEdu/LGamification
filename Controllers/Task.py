from collections.abc import Sequence

from flask import request, abort
from flask_restx import Resource, Namespace, fields

from App import api
from Facades.Journal import JournalFacade
from Facades.User import UserFacade
from Services.funcs import check_session, edit_model_fields
from Facades.Task import TaskFacade as Task

ns = Namespace("user/<int:userID>/tasks")


user_param = ()


@ns.route("/")
class Index(Resource):
    @api.marshal_list_with(Task.dto)
    async def get(self, userID: int) -> Sequence:
        check_session(userID)

        res = Task.Repo.get_all_by_user(userID)
        return list(res)

    @api.marshal_with(Task.dto)
    @api.param("title", type=str)
    async def post(self, userID: int) -> Task.model:
        check_session(userID)

        title = request.args.get("title")
        if not title:
            abort(400, "No title arg provided.")

        task = Task.create(userID, title)
        return task.entry


@ns.route("/<int:taskID>")
class TaskEntry(Resource):
    @api.marshal_with(Task.dto)
    async def get(self, userID: int, taskID: int) -> Task.model:
        check_session(userID)

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
    async def put(self, userID: int, taskID: int) -> Task.model:
        check_session(userID)

        return edit_model_fields(
            facade=Task.get(taskID),
            field_names=list(self.taskput_dict.keys()),
            data=request.json
        ).entry


@ns.route("/<int:taskID>/calc_rewards")
class TaskCalc(Resource):
    @api.marshal_with(Task.dto)
    async def post(self, userID: int, taskID: int) -> Task.model:
        check_session(userID)

        task = Task.get(taskID)

        if task.entry.difficulty is None or task.entry.duration is None:
            abort(400, "Task does not have difficulty or duration to calc rewards from.")

        task.calc_rewards()
        return task.entry


@ns.route("/<int:taskID>/complete")
class CompleteTask(Resource):
    @staticmethod
    async def post(userID: int, taskID: int):
        check_session(userID)

        task = Task.get(taskID)
        task.complete()

        user = UserFacade.get(userID)
        user.log(f"Task completed: {task.entry.title}",
                 xp=task.entry.xp,
                 cash=task.entry.cash
                 )
