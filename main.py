import logging

from flask import Flask
from flask_restx import Api

from Controllers import namespaces
from app_database import Database


# Flask
app = Flask(__name__)
app.secret_key = "very_secret_key_bro_trust_me_its_secure_af_i_bet_ur_mom"
app.config["SESSION_TYPE"] = "SQLAlchemy"
logging.basicConfig(
        level=logging.DEBUG,
        format="\033[33m%(message)s\033[0m"
    )


# Flask-RestX-Swagger
api = Api()
api.init_app(app)
for ns in namespaces:
    api.add_namespace(ns)
    print(f"namespace {ns.name} was added to api.")


def main():
    print("App launched.")
    app.run(debug=True)


if __name__ == '__main__':
    main()
