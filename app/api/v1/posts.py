import json
from flask import g, jsonify, request, current_app, url_for

from app.api.v1_0 import api
from app.models.post_dao import PostDAO


@api.route('/posts/')
def get_posts():
    post_dao = PostDAO()
    posts = post_dao.get_posts()
    posts_json = json.dumps([ob.__dict__ for ob in posts])
    print(type(posts))
    print(type(posts_json))
    print(type(json.loads(posts_json)))

    return jsonify({'msg': 'success', 'data': json.loads(posts_json)})
