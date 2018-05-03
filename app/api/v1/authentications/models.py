from datetime import datetime

from app import db


class AuthenticationToken(db.Model):
    __tablename__ = 'authenticationtokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    token = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
