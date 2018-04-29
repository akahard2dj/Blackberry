import enum
from datetime import datetime

from app import db


class BoardStatus(enum.Enum):
    USE = 'USE',
    DELETED = 'DELETED'


class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(BoardStatus), default='USE')
    title = db.Column(db.Text)
    description = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
