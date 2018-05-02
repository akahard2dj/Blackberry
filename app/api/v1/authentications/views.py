from flask import Blueprint, g, jsonify
from flask_restplus import Api, Resource

from app.api.v1.authentications.authentication import auth

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)


@api.route('/token')
class TokenApi(Resource):
    decorators = [auth.login_required]

    def get(self):
        expiration = 3600
        token = g.current_user.generate_auth_token(expiration=expiration).decode("utf-8")

        return jsonify({'token': token, 'expiration': expiration})
