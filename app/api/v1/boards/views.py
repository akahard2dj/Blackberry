from flask import Blueprint
from flask_restful import Resource, fields, Api, marshal_with

from app.api.v1.boards.models import Board

board_bp = Blueprint('board', __name__)


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


board = Api(board_bp)
board.add_resource(BoardView, '/<int:board_id>')
