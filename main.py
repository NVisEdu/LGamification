import os

from dotenv import load_dotenv

from app.core import App
from app.core.App import logger
from app.controllers import namespaces
from app.database.db_init import Database


load_dotenv()


def main():
    App.app = App.create_app()
    for ns in namespaces:
        App.api.add_namespace(ns)
        logger.debug(f"Namespace added: \"{ns.name}\"")

    Database()

    logger.debug("App is starting...")
    App.app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.1"),
        port=os.getenv("FLASK_PORT", 5000),
        debug=True,
        use_reloader=False
    )


if __name__ == '__main__':
    main()
