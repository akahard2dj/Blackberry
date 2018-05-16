import re

from flask import g
from flask_restplus import marshal_with, fields, Resource, reqparse

from app import db, get_api
from app.api.v1.common.exception.exceptions import AccountException, CommonException
from app.api.v1.common.views import ResponseWrapper
from app.api.v1.users.models import User

from app.api.v1.authentications.authentication import auth

api = get_api()

user_field = {
    'id': fields.Integer,
    'status': fields.String(attribute=lambda x: x.status.name),
    'username': fields.String,
    'university': fields.String,
    'email': fields.String
}

user_register_parser = reqparse.RequestParser()
user_register_parser.add_argument('username')
user_register_parser.add_argument('email')
user_register_parser.add_argument('password')


@api.route('/users/<int:user_id>')
class UserSearchApi(Resource):
    decorators = [auth.login_required]

    @marshal_with(user_field)
    def get(self, user_id):
        if g.current_user.id == user_id:
            user = User.query.filter(User.id == user_id).first()
            return ResponseWrapper.ok(data=user)

        raise AccountException('Invalid User ID')


@api.route('/users')
class UserRegistrationApi(Resource):
    EMAIL_REGEX = re.compile("[^@]+@[^@]+\.[^@]+")

    @marshal_with(user_field)
    def post(self):
        args = user_register_parser.parse_args()

        # Email Validation is confirmed by regex
        if not self.EMAIL_REGEX.match(args.email):
            raise CommonException('Email Validation is failed!')

        user = User(username=args.username, password=args.password, email=args.email)
        db.session.add(user)

        try:
            db.session.commit()
            return ResponseWrapper.ok(data=user)
        except Exception as e:
            db.session.rollback()
            db.session.flush()

        raise CommonException('db save failed!')
