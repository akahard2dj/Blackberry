from flask import jsonify
from flask_restplus import Resource

from app import cache, get_api

api = get_api()


class ResponseWrapper:
    @staticmethod
    def ok(*args):
        if len(args) == 1 and isinstance(args[0], str):
            result = dict()
            result['message'] = args[0]
            return result, 200
        elif len(args) == 2 and isinstance(args[1], object):
            result = dict()
            result['message'] = args[0]
            result['data'] = args[1]
            return result, 200
        else:
            # TODO: right raise error is needed
            raise AttributeError


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
