from flask_restx import fields

from App import api, logger


user_dto = api.model("User", {
    "ID": fields.Integer,
    "username": fields.String,
    "nickname": fields.String,
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


logger.debug("DTO (marshal) models registered.")
