from flask_restx import fields

from app.core.App import api, logger


user_dto = api.model("User", {
    "ID": fields.Integer,
    "username": fields.String,
    "nickname": fields.String,
    "pfp":    fields.String,
    "lvl":    fields.Integer,
    "xp":     fields.Integer,
    "cash":   fields.Integer,
    "hp":     fields.Integer,
    "max_hp": fields.Integer,
})


userdata_dto = api.model("Userdata", {
    "lvl":    fields.Integer,
    "xp":     fields.Integer,
    "cash":   fields.Integer,
    "hp":     fields.Integer,
    "max_hp": fields.Integer,
})


task_dto = api.model("Task", {
    "ID":   fields.Integer,
    "title":    fields.String,
    "status":   fields.String,
    "due":      fields.DateTime,
    "xp":       fields.Integer,
    "cash":     fields.Integer,
    "difficulty": fields.String,  # Set(Easy,  Normal, Medium, Hard, Very hard)
    "duration": fields.String,    # Set(Quick, Normal, Medium, Long, Very long)
    "userID":   fields.Integer,
    "objectiveID": fields.Integer,
})


journal_dto = api.model("Journal", {
    "ID": fields.Integer,
    "title": fields.String,
    "date": fields.DateTime,
    "cash": fields.Integer,
    "xp": fields.Integer,
    "hp": fields.Integer,
    "sp": fields.Integer,
    "userID": fields.Integer,
})


cultivator_dto = api.model("Cultivator", {
    "ID": fields.Integer,
    "userID":   fields.Integer,
    "title":    fields.String,
    "xp_reward":  fields.Integer,
    "hp_penalty": fields.Integer
})


logger.debug("DTO (marshal) models registered.")
