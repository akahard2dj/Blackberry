from flask import g
from flask_restplus import Resource, fields, marshal_with

from app import get_api
from app.api.v1.authentications.authentication import auth
from app.api.v1.boards.models import Board, UserBoardConnector
from app.api.v1.common.exception.exceptions import AccountException

api = get_api()


@api.route('/boards/<int:board_id>')
class BoardView(Resource):
    decorators = [auth.login_required]

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
        connector = UserBoardConnector.query.filter(UserBoardConnector.user_id == g.current_user.id).first()
        if connector.check_board_id(board_id):
            return Board.query.filter(Board.id == board_id).first()
        else:
            raise AccountException("Permission denied")

