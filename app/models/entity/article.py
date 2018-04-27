from datetime import datetime

from app import db
from app.models.entity.board import Board

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    # status index
    # 0 - article, 1 - reported, 2 - deleted
    status_index = db.Column(db.Integer, default=0)
    hits_count = db.Column(db.Integer, default=1)
    likes_count = db.Column(db.Integer, default=0)
    report_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
