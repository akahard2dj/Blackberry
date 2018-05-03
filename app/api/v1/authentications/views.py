import re

from flask import Blueprint, g, jsonify, request
from flask_restplus import Api, Resource, reqparse

from app import cache
from app import db
from app.api.v1.authentications.authentication import auth
from app.api.v1.authentications.errors import bad_request
from app.api.v1.users.models import User, University
from app.api.v1.boards.models import UserBoardConnector


auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)


@api.route('/token')
class TokenApi(Resource):
    decorators = [auth.login_required]

    #TODO: this function is will be entirely changed to Token base authentication(not timed token)
    def get(self):
        expiration = 3600
        token = g.current_user.generate_auth_token(expiration=expiration).decode("utf-8")

        return jsonify({'token': token, 'expiration': expiration})


@api.route('/email-check')
class EmailCheckApi(Resource):

    EMAIL_REGEX = re.compile("[^@]+@[^@]+\.[^@]+")

    def get(self):
        #TODO: uuid argument is needed
        email = request.args.get('email')
        if not email:
            bad_request('No email')

        if not self.EMAIL_REGEX.match(email):
            bad_request('Email Validation is failed')

        else:
            #when the information of user is not changed(email, uuid), go to app first
            from_db_user = User.query.filter(User.email==email).first()
            if from_db_user is None:
                #University Checking
                domain = email.split('@')[-1]
                university_from_db = University.query.filter(University.domain==domain).first()
                if university_from_db is None:
                    return jsonify({'msg': "Requested University is Not Service"})
                else:
                    return jsonify({'msg': 'Email Check is completed'})
            else:
                #already registered user
                #email & password check -> tracing an alteration of phone or re-installed app
                is_alteration = from_db_user.verify_password('test1234')
                from_db_user.status = "PENDING"
                try:
                    db.session.commit()
                except Exception as e:
                    bad_request('internal error')
                return jsonify({'msg': 'already registered user'})


@api.route('/gen-auth-key')
class GenerateAuthKeyApi(Resource):
    EMAIL_REGEX = re.compile("[^@]+@[^@]+\.[^@]+")

    def get(self):
        email = request.args.get('email')
        if not email:
            bad_request('No email')

        if not self.EMAIL_REGEX.match(email):
            bad_request('Email Validation is failed')
        else:
            if cache.get('auth_key:{}'.format(email)):
                return jsonify({'msg': 'already email is sent'})

            else:
                auth_key_status = dict()
                # TODO : auth code is needed to be random function
                auth_key_status['code'] = 1234
                auth_key_status['status'] = 'SENT'
                cache.set('auth_key:{}'.format(email), auth_key_status, timeout=600)
                return jsonify({'msg': 'auth key is generated'})


@api.route('/confirm-auth-key')
class ConfirmAuthKeyApi(Resource):
    EMAIL_REGEX = re.compile("[^@]+@[^@]+\.[^@]+")

    def get(self):
        email = request.args.get('email')
        authcode = request.args.get('authcode')

        if not email:
            bad_request('No email')

        if not authcode:
            bad_request('No authcode')

        if not self.EMAIL_REGEX.match(email):
            bad_request('Email Validation is failed')
        else:
            res_from_cache = cache.get('auth_key:{}'.format(email))
            if res_from_cache is None:
                bad_request('Timed out : re-authentication is needed')
            else:
                auth_code_from_cache = res_from_cache['code']
                if int(authcode) == auth_code_from_cache:
                    cache.delete('auth_key:{}'.format(email))
                    res_from_cache['status'] = 'CONFIRM'
                    cache.set('auth_key:{}'.format(email), res_from_cache, timeout=1800)

                    from_db_user = User.query.filter(User.email==email).first()
                    if from_db_user is None:
                        domain = email.split('@')[-1]
                        university_from_db = University.query.filter(domain=domain).first()

                        new_user = User()
                        new_user.email = email
                        new_user.password = 'test1234'
                        new_user.username = 'randomid'
                        new_user.university = university_from_db.id

                        db.session.add(new_user)
                        try:
                            db.session.commit()
                        except Exception as e:
                            return bad_request('internal error')

                    return jsonify({'msg': 'Success'})
                else:
                    return bad_request('invalid auth_code')


@api.route('/registration')
class RegistrationApi(Resource):
    EMAIL_REGEX = re.compile("[^@]+@[^@]+\.[^@]+")

    def get(self):
        email = request.args.get('email')
        authcode = request.args.get('authcode')

        if not email:
            bad_request('No email')

        if not authcode:
            bad_request('No authcode')

        if not self.EMAIL_REGEX.match(email):
            bad_request('Email Validation is failed')
        else:
            res_from_cache = cache.get('auth_key:{}'.format(email))
            if res_from_cache is None:
                bad_request('Timed out : re-authentication is needed')
            else:
                auth_code_from_cache = res_from_cache['code']
                if int(authcode) == auth_code_from_cache:
                    if res_from_cache['status'] == 'CONFIRM':
                        #TODO: Registration
                        to_confirm_user = User.query.filter(User.email==email).first()
                        to_confirm_user.status = 'USE'

                        #connector = UserBoardConnector()
                        #connector.user_id = to_confirm_user.id
                        try:
                            db.session.commit()
                        except Exception as e:
                            return bad_request('internal error')
                        return jsonify({'msg': 'registration is ok'})
                    else:
                        bad_request('auth code is not confirmed')

                else:
                    return bad_request('invalid auth_code')
