import enum
from datetime import datetime
from passlib.hash import pbkdf2_sha256

from app import db


class UserStatus(enum.Enum):
    USE = 'USE',
    PENDING = 'PENDING'
    DELETED = 'DELETED'
    BLOCKED = 'BLOCKED'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # email is id for login
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    status = db.Column(db.Enum(UserStatus), default='PENDING')
    username = db.Column(db.Text)
    # TODO: University Table is needed
    university = db.Column(db.String(128))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('passowrd is not a readable attribute')

    @password.setter
    def password(self, password):
        custom_pbkdf2 = pbkdf2_sha256.using(rounds=10000)
        self.password_hash = custom_pbkdf2.hash(password)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)
