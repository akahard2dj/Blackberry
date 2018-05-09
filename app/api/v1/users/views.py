import re

from flask import g
from flask_restplus import marshal_with, fields, Resource, reqparse

from app import db, api_holder
from app.api.v1.users.models import User

from app.api.v1.authentications.authentication import auth
from app.api.v1.authentications.errors import forbidden, unauthorized, bad_request

api = api_holder[0]

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
            return User.query.filter(User.id == user_id).first()
        else:
            forbidden('Invalid User ID')


@api.route('/users')
class UserRegistrationApi(Resource):
    EMAIL_REGEX = re.compile("[^@]+@[^@]+\.[^@]+")

    @marshal_with(user_field)
    def post(self):
        args = user_register_parser.parse_args()

        # TODO: validate data
        # Email Validation is confirmed by regex
        if not self.EMAIL_REGEX.match(args.email):
            bad_request('Email Validation is failed')

        user = User(username=args.username, password=args.password, email=args.email)
        db.session.add(user)

        commit_flag = True
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            commit_flag = False

        if commit_flag:
            return user
        else:
            bad_request('internal server error')
