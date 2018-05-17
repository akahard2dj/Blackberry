from flask import jsonify
from flask_restplus import Resource

from app import cache, get_api

api = get_api()


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
