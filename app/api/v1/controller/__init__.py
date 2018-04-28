from flask import Blueprint
from flask_restful import Api

from app.api.v1.controller.board_api import BoardAPI
from app.api.v1.controller.hello_controller import HelloController

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(HelloController, '/hello')
api.add_resource(BoardAPI, '/board/<int:board_id>')
