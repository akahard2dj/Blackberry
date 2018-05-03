import enum
from datetime import datetime

from sqlalchemy import exc

from app import db


class BoardStatus(enum.Enum):
    USE = 'USE',
    DELETED = 'DELETED'


class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True, index=True)
    status = db.Column(db.Enum(BoardStatus), default='USE')
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(128), nullable=False)
    university = db.relationship("University", secondary="university_board_tags")
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserBoardConnector(db.Model):
    __tablename__ = 'connectors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    board_id_str = db.Column(db.Text)

    def set_board_id(self, board_id):
        value = self.board_id_str
        if not value:
            value = '{board_id},'.format(board_id=board_id)
        else:
            value += '{board_id},'.format(board_id=board_id)

        id_list = list(map(int, value.split(',')[:-1]))
        id_list = sorted(set(id_list))
        value_to_db = ','.join(str(x) for x in id_list) + ','
        self.board_id_str = value_to_db
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise exc.SQLAlchemyError

    def get_board_id(self):
        value = self.board_id_str
        return list(map(int, value.split(',')[:-1]))

    def pop_board_id(self, board_id):
        value = self.board_id_str
        id_list = list(map(int, value.split(',')[:-1]))
        if board_id in id_list:
            id_list.remove(board_id)
            value_to_db = ','.join(str(x) for x in id_list) + ','
            self.board_id_str = value_to_db

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise exc.SQLAlchemyError

    def check_board_id(self, board_id):
        board_id = int(board_id)

        value = self.board_id_str
        if not value:
            return False
        else:
            id_list = list(map(int, value.split(',')[:-1]))
            return board_id in id_list
