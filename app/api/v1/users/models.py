import enum
from datetime import datetime

from app import db


class UserStatus(enum.Enum):
    USE = 'USE',
    PENDING = 'PENDING'
    DELETED = 'DELETED'
    BLOCKED = 'BLOCKED'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(UserStatus), default='PENDING')
    name = db.Column(db.Text)
    university = db.Column(db.String(128))
    email = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
