from flask import Blueprint
from flask_restful import Resource, fields, Api, marshal_with


board_bp = Blueprint('board', __name__)


