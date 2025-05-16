from collections.abc import Sequence

from flask import request, abort
from flask_restx import Resource, Namespace, fields

from app.core.App import api
from app.facades import Cultivator
from app.facades.user import UserFacade as User
from app.services.utils import check_session, edit_model_fields

ns = Namespace("user/<int:userID>/cultivation")


user_param = ()


@ns.route("/")
class Index(Resource):
    @api.marshal_list_with(Cultivator.dto)
    def get(self, userID: int) -> Sequence:
        check_session(userID)

        res = Cultivator.repo.get_all_by_user(userID)
        return list(res)

    @api.marshal_with(Cultivator.dto)
    @api.param("title", type=str)
    @api.param("xp_reward", type=int)
    @api.param("hp_penalty", type=int)
    def post(self, userID: int, sessionkey) -> Cultivator.model:
        check_session(userID, sessionkey)

        title = request.args.get("title")
        xp_reward  = int(request.args.get("xp_reward")  or 0)
        hp_penalty = int(request.args.get("hp_penalty") or 0)
        if not title:
            abort(400, "No title arg provided.")

        cultivator = Cultivator.create(userID, title, xp_reward=xp_reward, hp_penalty=hp_penalty)
        return cultivator.entry
    

@ns.route("/<int:cultivatorID>")
class CultivatorEntry(Resource):
    @api.marshal_with(Cultivator.dto)
    def get(self, userID: int, cultivatorID: int, sessionkey) -> Cultivator.model:
        check_session(userID, sessionkey)

        res = Cultivator.get(cultivatorID)
        return res.entry
    
    cultivatorput_dto = ns.model(
        "cultivator_edit",
        {
            "title": fields.String(required=False),
            "xp_reward":  fields.Integer(required=False),
            "hp_penalty": fields.Integer(required=False),
        }
    )

    @ns.expect(cultivatorput_dto)
    @api.marshal_with(Cultivator.dto)
    def put(self, userID: int, cultivatorID: int, sessionkey: str) -> Cultivator.model:
        check_session(userID, sessionkey)

        return edit_model_fields(
            facade=Cultivator.get(cultivatorID),
            field_names=list(self.cultivatorput_dto.keys()),
            data=request.json
        ).entry


@ns.route("/<int:cultivatorID>/complete")
class CompleteCultivator(Resource):
    @staticmethod
    def post(userID: int, cultivatorID: int, sessionkey: str):
        check_session(userID, sessionkey)

        cultivator = Cultivator.get(cultivatorID)
        cultivator.complete()

        User.get(userID).log(
            f"Cultivated: {cultivator.entry.title}",
            xp=cultivator.entry.xp,
            hp=cultivator.entry.hp
        )
