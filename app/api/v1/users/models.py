import enum
from datetime import datetime

from flask import current_app

from passlib.hash import pbkdf2_sha256
from passlib.hash import sha256_crypt

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import JSONWebSignatureSerializer as JWS

from app import db

from app.api.v1.boards.models import Board


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
    # TODO: username should have an unique property
    username = db.Column(db.Text)

    # TODO: university -> university_id
    university = db.Column(db.Integer, db.ForeignKey("universities.id"))

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

    def generate_auth_token(self, expiration=7200):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None

        return User.query.get(data['id'])


class UserToken(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(128), index=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    is_issued = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def generate_token(self, salt):
        s = JWS(secret_key=current_app.config['SECRET_KEY'], salt=salt)
        payload = {'user_id': self.user_id}
        self.token = s.dumps(payload)


class University(db.Model):
    __tablename__ = 'universities'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(256), nullable=False)
    domain = db.Column(db.String(128), nullable=False)
    boards = db.relationship("Board", secondary="university_board_tags")


class UniversityBoardTags(db.Model):
    __tablename__ = "university_board_tags"
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey("universities.id"))
    board_id = db.Column(db.Integer, db.ForeignKey("boards.id"))

    university = db.relationship(University, backref=db.backref("university_board_tags", cascade="all, delete-orphan"))
    board = db.relationship(Board, backref=db.backref("university_board_tags", cascade="all, delete-orphan"))
