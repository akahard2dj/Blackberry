
from flask import jsonify
from flask_restplus import Resource

from app import cache, get_api

api = get_api()


def row2dict(row, fields: set=set()):
    d = {}
    for column in row.__table__.columns:
        if column.name in fields:
            d[column.name] = str(getattr(row, column.name))
    return d


def rows2dict(rows, fields: set=set()):
    arr = []
    for row in rows:
        arr.append(row2dict(row, fields))
    return arr


class ResponseWrapper:
    @staticmethod
    def ok(message: str='success', data: object=None):
        result = dict()
        result['message'] = message
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
