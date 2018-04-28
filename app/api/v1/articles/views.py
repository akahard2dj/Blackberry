from flask import Blueprint
from flask_restful import Resource, fields, Api, marshal_with

from app.api.v1.articles.models import Article

article_bp = Blueprint('article', __name__)


class ArticleView(Resource):

    post_fields = {
        'title': fields.String,
        'hits': fields.Integer,
        'created_at': fields.DateTime
    }

    @marshal_with(post_fields)
    def get(self):
        """ 해당 게시판의 글 목록을 리턴한다.

        :param board_id: 게시판 아이디
        :return: article 리스트
        """
        articles = Article.query.all()

        return articles

    def post(self):
        pass


article = Api(article_bp)
article.add_resource(ArticleView, '')
