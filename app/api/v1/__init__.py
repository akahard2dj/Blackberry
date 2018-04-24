from flask import Blueprint
from flask_restful import Api

from app.api.v1_0.test_api import TestApi

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(TestApi, '/testapi')
