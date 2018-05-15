from flask import abort
from flask import jsonify

# TODO: CommonException 으로 교체.

def bad_request(message):
    return abort(400, message)
