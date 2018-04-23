from flask import jsonify, request, g, url_for, current_app
from . import api

@api.route('/')
def hello():
    return jsonify({'msg': 'success'})
