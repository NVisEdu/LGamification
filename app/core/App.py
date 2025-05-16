import logging

from flask import Flask
from flask_restx import Api


app = Flask(__name__)
api = Api()
logger = logging.getLogger(__name__)
