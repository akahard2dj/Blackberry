from collections import Iterable

from flask import jsonify
from flask_restplus import Resource

from app import cache, get_api

api = get_api()


class ResponseWrapper:
    @staticmethod
    def ok(message: str='success', data: object=None):
        result = dict()
        result['message'] = message

        def row2dict(row):
            d = {}
            for column in row.__table__.columns:
                d[column.name] = str(getattr(row, column.name))
            return d

        if data:
            if isinstance(data, dict):
                data = data
            elif isinstance(data, Iterable):
                data = [row2dict(row) for row in data]
            else:
                data = row2dict(data)
        result['data'] = data
        return result


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
