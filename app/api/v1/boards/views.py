from flask import Blueprint
from flask_restplus import Resource, fields, Api, marshal_with

from app.api.v1.boards.models import Board

board_bp = Blueprint('board', __name__)
api = Api(board_bp)


@api.route('/<int:board_id>')
class BoardView(Resource):

    board_fields = {
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    }

    @marshal_with(board_fields)
    def get(self, board_id):
        """ 해당 게시판 정보 리턴한다.

        :param board_id: 게시판 아이디
        :return: 게시판
        """
        return Board.query.filter(Board.id == board_id).first()

    def post(self):
        pass
