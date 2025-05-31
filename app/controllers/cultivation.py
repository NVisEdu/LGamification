from collections.abc import Sequence

from flask import request, abort, make_response as resp
from flask_restx import Resource, Namespace, fields

from app.core.App import api
from app.facades import Cultivator
from app.facades.user import UserFacade as User
from app.services.utils import edit_model_fields, session_required, require_args

ns = Namespace("user/<int:userID>/cultivation")


cultivatorput_dto = ns.model(
    "cultivator_edit",
    {
        "title": fields.String(required=False),
        "xp_reward": fields.Integer(required=False),
        "hp_penalty": fields.Integer(required=False),
    }
)


@ns.route("/")
class Index(Resource):
    method_decorators = [session_required]

    @api.marshal_list_with(Cultivator.dto)
    def get(self, userID: int) -> Sequence:
        res = Cultivator.repo.get_all_by_user(userID)
        return list(res)

    @api.marshal_with(Cultivator.dto)
    @api.param("title", type=str)
    @api.param("xp_reward", type=int)
    @api.param("hp_penalty", type=int)
    def post(self, userID: int) -> Cultivator.model:
        title, = require_args("title", "xp_reward", "hp_penalty")
        xp_reward  = int(request.args.get("xp_reward")  or 0)
        hp_penalty = int(request.args.get("hp_penalty") or 0)

        cultivator = Cultivator.create(
            userID, title, xp_reward=xp_reward, hp_penalty=hp_penalty
        )
        return cultivator.entry
    

@ns.route("/<int:cultivatorID>")
class CultivatorEntry(Resource):
    method_decorators = [session_required]

    @api.marshal_with(Cultivator.dto)
    def get(self, cultivatorID: int) -> Cultivator.model:
        res = Cultivator.get(cultivatorID)
        return res.entry

    @ns.expect(cultivatorput_dto)
    @api.marshal_with(Cultivator.dto)
    def put(self, cultivatorID: int) -> Cultivator.model:
        return edit_model_fields(
            facade=Cultivator.get(cultivatorID),
            field_names=list(cultivatorput_dto.keys()),
            data=request.json
        ).entry


@ns.route("/<int:cultivatorID>/complete")
class CompleteCultivator(Resource):
    method_decorators = [session_required]

    def post(self, userID: int, cultivatorID: int):
        cultivator = Cultivator.get(cultivatorID)
        cultivator.complete()

        User.get(userID).log(
            f"Cultivated: {cultivator.entry.title}",
            xp=cultivator.entry.xp,
            hp=cultivator.entry.hp
        )

        return resp(204)
