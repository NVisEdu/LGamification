from flask_restx import fields

from main import api

user_marshal = api.model("User", {
    "ID": fields.Integer,
    "username": fields.String,
    "lvl":    fields.Integer,
    "xp":     fields.Integer,
    "cash":   fields.Integer,
    "hp":     fields.Integer,
    "max_hp": fields.Integer
})
