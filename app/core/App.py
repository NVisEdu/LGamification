import logging
from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from dotenv import load_dotenv
import os


app: Flask = None


load_dotenv()


api = Api()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="\033[33m%(message)s\033[0m")


def create_app():
    newapp = Flask(__name__)

    newapp.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
    newapp.config["SESSION_TYPE"] = os.getenv("FLASK_SESSION_TYPE", "filesystem")
    debug = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1")

    CORS(newapp, supports_credentials=True)

    api.init_app(newapp)
    logger.debug("API initialized")

    return newapp
