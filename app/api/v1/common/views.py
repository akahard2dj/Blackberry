from flask import Blueprint, jsonify

from app import cache

common_bp = Blueprint('common', __name__)


@common_bp.route('/hello')
def hello():
    return "hello"


@common_bp.route('/cache-test')
def cache_test():
    rv = cache.get('my-item')
    print(rv)
    if rv is None:
        rv = 100
        cache.set('my-item', rv, timeout=60)
        print(rv)

    return jsonify({'value': rv})
