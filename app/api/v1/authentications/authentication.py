from flask import Blueprint, g
from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPTokenAuth
from flask_restplus import Api

from app.api.v1.users.models import User
from app.api.v1.users.models import UserToken
from app.api.v1.authentications.errors import unauthorized

auth = HTTPTokenAuth(scheme='Token')
auth_basic = HTTPBasicAuth()


@auth.verify_token
def verify_token(token):
    # TODO: AuthenticationToken DB querying
    print(token)
    user_token = UserToken.query.filter(UserToken.token == token).first()
    if not user_token:
        return False
    else:
        user = User.query.filter(User.id == user_token.user_id).first()
        if not user:
            return False
    g.current_user = user
    return True


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@auth_basic.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return False
    g.current_user = user
    return True


@auth_basic.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

