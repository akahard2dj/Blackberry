from flask_restful import Resource, fields, marshal_with
from flask import jsonify

from app.models.post_dao import PostDAO
from app.models.post import Post

post_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'body': fields.String
}


class PostApi(Resource):

    @marshal_with(post_fields)
    def get(self):
        post_dao = PostDAO()
        posts = post_dao.get_posts_obj()
        #posts = Post.query.all()

        return posts

    def post(self):
        pass
