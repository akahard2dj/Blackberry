import json
from flask import g, jsonify, request, current_app, url_for

from app.api.v1_0 import api
from app.models.post_dao import PostDAO


@api.route('/posts/')
def get_posts():
    post_dao = PostDAO()
    posts = post_dao.get_posts()
    posts_json = json.dumps([ob.__dict__ for ob in posts])

    return jsonify({'msg': 'sucess', 'data': posts_json})
