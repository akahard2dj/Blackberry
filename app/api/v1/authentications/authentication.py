from flask import Blueprint, g
from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPTokenAuth
from flask_restplus import Api

from app.api.v1.users.models import User
from app.api.v1.authentications.errors import unauthorized

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    #TODO: AuthenticationToken DB querying
    print(token)
    # TEMP USER
    g.current_user = User.query.filter(User.id==2).first()
    return True

#TODO: HTTPAuth is deprecated.
'''
@auth.verify_password
def verify_password(email_or_token, password):
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        return g.current_user is not None

    user = User.query.filter_by(email=email_or_token).first()
    if not user or not user.verify_password(password):
        return False
    g.current_user = user
    return True
'''


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

