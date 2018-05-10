import re

from flask import g, jsonify, request
from flask_restplus import Resource

from app import cache, get_api
from app import db

from app.api.common.utils import random_digit_with_number, random_number

from app.api.v1.authentications.authentication import auth_basic
from app.api.v1.authentications.errors import bad_request
from app.api.v1.users.models import User, University, UniversityBoardTags, UserToken
from app.api.v1.boards.models import UserBoardConnector

api = get_api()


@api.route('/auth/token')
class TokenApi(Resource):
    decorators = [auth_basic.login_required]

    # TODO: this function is will be entirely changed to Token base authentication(not timed token)
    # TODO: caching check system is needed
    def get(self):
        token = UserToken.query.filter(UserToken.user_id == g.current_user.id).first()
        if not token.is_issued:
            token.is_issued = True
            try:
                db.session.commit()
            except Exception as e:
                bad_request("Internal Error")
            return jsonify({'token': token.token, 'nonce': token.nonce})
        else:
            return jsonify({'msg': 'Token already has been issued'})


@api.route('/auth/email-check')
class EmailCheckApi(Resource):

    # TODO: WTForm library
    EMAIL_REGEX = re.compile("[^@]+@[^@]+\.[^@]+")

    def get(self):
        # TODO: uuid argument is needed
        email = request.args.get('email')
        if not email:
            bad_request('No email')

        if not self.EMAIL_REGEX.match(email):
            bad_request('Email Validation is failed')

        else:
            # when the information of user is not changed(email, uuid), go to app first
            from_db_user = User.query.filter(User.email == email).first()
            if from_db_user is None:
                # University Checking
                domain = email.split('@')[-1]
                university_from_db = University.query.filter(University.domain == domain).first()
                if university_from_db is None:
                    return jsonify({'msg': "Requested University is Not Service"})
                else:
                    return jsonify({'msg': 'Email Check is completed'})
            else:
                # already registered user
                # email & password check -> tracing an alteration of phone or re-installed app
                is_alteration = from_db_user.verify_password('test1234')
                if not is_alteration:
                    return jsonify({'msg': 'device is changed'})
                from_db_user.status = "PENDING"
                try:
                    db.session.commit()
                except Exception as e:
                    bad_request('internal error')
                return jsonify({'msg': 'already registered user'})


@api.route('/auth/gen-auth-key')
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
                auth_key_status['code'] = random_number()
                auth_key_status['status'] = 'SENT'
                # TODO: timeout variable should contain in app config
                cache.set('auth_key:{}'.format(email), auth_key_status, timeout=600)
                print('## TEMP LOG: code - {}'.format(auth_key_status['code']), type(auth_key_status['code']))
                return jsonify({'msg': 'auth key is generated'})


@api.route('/auth/confirm-auth-key')
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
                if authcode == auth_code_from_cache:
                    cache.delete('auth_key:{}'.format(email))
                    from_db_user = User.query.filter(User.email == email).first()
                    if from_db_user is None:
                        res_from_cache['status'] = 'CONFIRM'
                        res_from_cache['usertype'] = 'NEW'
                        cache.set('auth_key:{}'.format(email), res_from_cache, timeout=1800)
                        domain = email.split('@')[-1]
                        university_from_db = University.query.filter(domain == domain).first()

                        new_user = User()
                        new_user.email = email
                        new_user.password = 'test1234'
                        # TODO: username uniqueness check is needed
                        new_user.username = random_digit_with_number()
                        new_user.university = university_from_db.id

                        db.session.add(new_user)
                        try:
                            db.session.commit()
                        except Exception as e:
                            return bad_request('internal error')
                    else:
                        res_from_cache['status'] = 'CONFIRM'
                        res_from_cache['usertype'] = 'OLD'
                        cache.set('auth_key:{}'.format(email), res_from_cache, timeout=1800)

                    return jsonify({'msg': 'Success'})
                else:
                    return bad_request('invalid auth_code')


@api.route('/auth/registration')
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
                if authcode == auth_code_from_cache:
                    if res_from_cache['status'] == 'CONFIRM':
                        if res_from_cache['usertype'] == 'NEW':
                            to_confirm_user = User.query.filter(User.email == email).first()
                            to_confirm_user.status = 'USE'

                            connector = UserBoardConnector()
                            connector.user_id = to_confirm_user.id

                            joined_boards = UniversityBoardTags.query.filter(
                                UniversityBoardTags.university_id == to_confirm_user.university
                            ).all()

                            for joined_board in joined_boards:
                                connector.set_board_id(joined_board.board_id)

                            db.session.add(connector)

                            token = UserToken()
                            token.user_id = to_confirm_user.id
                            token.generate_token()
                            db.session.add(token)

                            res_from_cache['status'] = 'REGISTER'
                            cache.set('auth_key:{}'.format(email), res_from_cache, timeout=1800)

                            try:
                                db.session.commit()
                            except Exception as e:
                                return bad_request('internal error')
                            return jsonify({'msg': 'registration is ok'})
                        if res_from_cache['usertype'] == 'OLD':
                            registered_user = User.query.filter(User.email == email).first()
                            user_token = UserToken.query.filter(UserToken.user_id == registered_user.id).first()
                            if not user_token:
                                token = UserToken()
                                token.user_id = registered_user.id
                                token.generate_token()
                                db.session.add(token)
                            else:
                                user_token.generate_token()

                            res_from_cache['status'] = 'REGISTER'
                            cache.set('auth_key:{}'.format(email), res_from_cache, timeout=1800)

                            db.session.commit()
                            return jsonify({'msg': 'registration is ok'})
                    else:
                        bad_request('auth code is not confirmed')

                else:
                    return bad_request('invalid auth_code')
