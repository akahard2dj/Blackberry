from flask import jsonify
from flask_restful import Resource, fields, marshal_with, reqparse

from api.v1.models.post import Post
from app import db

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'title', dest='title', type=str
)
post_parser.add_argument(
    'body', dest='body', type=str
)

post_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'body': fields.String
}


class PostApi(Resource):

    @marshal_with(post_fields)
    def get(self):
        #post_dao = PostDAO()
        #posts = post_dao.get_posts_obj()
        posts = Post.query.all()

        return posts

    def post(self):
        args = post_parser.parse_args()
        p = Post()
        p.title = args.title
        p.body = args.body
        db.session.add(p)
        db.session.commit()
        
        return jsonify({'msg': 'success'})
