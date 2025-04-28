import datetime
import logging

from App import app, api, logger
from Controllers import namespaces
from app_database import Database
from flask_cors import CORS


CORS(app, supports_credentials=True)

# Flask
app.secret_key = "very_secret_key_bro_trust_me_its_secure_af_i_bet_ur_mom"
app.config["SESSION_TYPE"] = "SQLAlchemy"
logging.basicConfig(
        level=logging.DEBUG,
        format="\033[33m%(message)s\033[0m"
    )


# Flask-RestX-Swagger
api.init_app(app)
logger.debug(f"App initialized: {api}")
for ns in namespaces:
    logger.debug(f"Namespace added: \"{ns.name}\"")
    api.add_namespace(ns)


def main():
    logger.debug(f"App launched: {api}")
    Database()
    app.run(
        host="193.201.15.217:5050",
        debug=True, use_reloader=False
    )


if __name__ == '__main__':
    main()
