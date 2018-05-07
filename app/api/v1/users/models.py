import enum
from datetime import datetime

from flask import current_app

from passlib.hash import pbkdf2_sha256

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import JSONWebSignatureSerializer

from app import db

from app.api.common.utils import random_digit_with_number
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
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        custom_pbkdf2 = pbkdf2_sha256.using(rounds=10000)
        self.password_hash = custom_pbkdf2.hash(password)

    # User 모델과는 무관한 기능. 분리하는게 어떨까요?
    # 이름만으로는 어떤 값을 리턴하는 메소드인지 추측하기 힘드네요.
    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)

    # User 모델과는 무관한 기능. 분리하는게 어떨까요?
    # 이름만으로는 어떤 값을 리턴하는 메소드인지 추측하기 힘드네요.
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return None

        return User.query.get(data['id'])


# Token? UserToken? 테이블 이름에서 s를 제외한 이름으로 통일하면 더 좋을 것 같습니다.
class UserToken(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(128), index=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    nonce = db.Column(db.String(8), nullable=False)
    # 컬럼 이름은 동사보다는 명사로 해야 햇갈리지 않더라구요. method는 동사, 컬럼은 명사로 정하면 어떨까요?
    is_issued = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()

    def generate_token(self):
        nonce = random_digit_with_number(length_of_values=8)
        self.nonce = nonce
        self.is_issued = False
        s = JSONWebSignatureSerializer(secret_key=current_app.config['SECRET_KEY'], salt=nonce)
        payload = {'user_id': self.user_id}
        self.token = s.dumps(payload).decode('utf-8')


class University(db.Model):
    __tablename__ = 'universities'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(256), nullable=False)
    domain = db.Column(db.String(128), nullable=False)
    boards = db.relationship("Board", secondary="university_board_tags")


# Tags? 왜 XXXTags인지 주석 추가 좀 부탁 드려요~
class UniversityBoardTags(db.Model):
    __tablename__ = "university_board_tags"
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey("universities.id"))
    board_id = db.Column(db.Integer, db.ForeignKey("boards.id"))

    university = db.relationship(University, backref=db.backref("university_board_tags", cascade="all, delete-orphan"))
    board = db.relationship(Board, backref=db.backref("university_board_tags", cascade="all, delete-orphan"))
