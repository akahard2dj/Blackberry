from flask import jsonify
from flask_restplus import Resource

from app import cache, get_api

api = get_api()


class ResponseWrapper:

    @staticmethod
    def ok(message):
        result = dict()
        result['msg'] = message
        return result, 200

    @staticmethod
    def ok(message, data):
        result = dict()
        result['msg'] = message
        result['data'] = data
        return result, 200


@api.route('/hello')
class Hello(Resource):
    def get(self):
        return 'hello'


@api.route('/cache-test')
class CacheTest(Resource):
    def get(self):
        rv = cache.get('my-item')
        print(rv)
        if rv is None:
            rv = 100
            cache.set('my-item', rv, timeout=60)
            print(rv)

        return jsonify({'value': rv})
