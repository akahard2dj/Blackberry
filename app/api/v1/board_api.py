from flask_restful import Resource, fields, marshal_with

from app.models.entity.article import Article


post_fields = {
    'title': fields.String,
    'hits': fields.Integer,
    'created_at': fields.DateTime
}


class BoardAPI(Resource):

    @marshal_with(post_fields)
    def get(self, board_id):
        articles = Article.query.all()

        return articles

    def post(self):
        pass