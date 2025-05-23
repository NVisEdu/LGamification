import logging

from app.core.App import app, api, logger
from app.controllers import namespaces
from app.database.db_init import Database
from flask_cors import CORS


def configure_app():
    app.secret_key = "very_secret_key_bro_trust_me_its_secure_af_i_bet_ur_mom"
    app.config["SESSION_TYPE"] = "SQLAlchemy"
    CORS(app, supports_credentials=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format="\033[33m%(message)s\033[0m"
    )


def configure_api():
    api.init_app(app)
    logger.debug(f"Flask-RestX API initialized: {api}")
    for ns in namespaces:
        api.add_namespace(ns)
        logger.debug(f"Namespace added: \"{ns.name}\"")


def initialize_extensions():
    Database()


def main():
    configure_app()
    configure_api()
    initialize_extensions()

    logger.debug("App is starting...")
    app.run(
        host="193.201.15.217:5050",  # Avoid including port in host
        port=5050,
        debug=True,
        use_reloader=False
    )


if __name__ == '__main__':
    main()
