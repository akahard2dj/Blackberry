from flask import Blueprint, request
from flask_restful import Api, marshal_with, fields, Resource

from app import db
from app.api.v1.users.models import User

user_bp = Blueprint('user', __name__)

user_field = {
    'id': fields.Integer,
    'name': fields.String,
    'university': fields.String,
    'email': fields.String
}


class UserSearchApi(Resource):

    @marshal_with(user_field)
    def get(self, user_id):
        return User.query.filter(User.id == user_id).first()


class UserRegistrationApi(Resource):

    def post(self):
        data = request.json

        #TODO: validate data
        user = User(name=data['name'], university=data['university'],
                    email=data['email'])

        db.session.add(user)
        db.session.commit()

        return {"userId": user.id}


user = Api(user_bp)
user.add_resource(UserSearchApi, '/<int:user_id>')
user.add_resource(UserRegistrationApi, '')
