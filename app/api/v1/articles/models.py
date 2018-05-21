import enum
from datetime import datetime

from app import db


class YesOrNo(enum.Enum):
    Y = 'Y'
    N = 'N'


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    body = db.Column(db.Text)
    hits_count = db.Column(db.Integer, default=1)
    likes_count = db.Column(db.Integer, default=0)
    dislike_count = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Enum(YesOrNo), default='N')
    reported = db.Column(db.Enum(YesOrNo), default='N')
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
