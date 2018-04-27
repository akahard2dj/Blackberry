from datetime import datetime

from app import db


class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    # status index
    # 0 - article, 1 - reported, 2 - deleted
    status_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.Text)
    description = db.Column(db.String(128))