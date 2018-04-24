from flask import Blueprint

api = Blueprint('api', __name__)

from app.api.v1_0 import posts
