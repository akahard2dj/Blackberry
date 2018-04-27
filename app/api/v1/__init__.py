from flask import Blueprint
from flask_restful import Api

from app.api.v1.test_api import TestApi
from app.api.v1.posts import PostApi
from app.api.v1.post_controller import PostController

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(TestApi, '/testapi')
api.add_resource(PostApi, '/posts/')
api.add_resource(PostController, '/test')
