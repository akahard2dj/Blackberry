from flask import Blueprint, request
from flask_restful import Resource, fields, Api, marshal_with

from app.api.v1.articles.models import Article

article_bp = Blueprint('article', __name__)


class ArticleView(Resource):

    article_fields = {
        'status': fields.String(attribute=lambda x: x.status.name),
        'board_id': fields.Integer,
        'title': fields.String,
        'body': fields.String,
        'hits_count': fields.Integer,
        'likes_count': fields.Integer,
        'dislike_count': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    @marshal_with(article_fields)
    def get(self, article_id):
        """ 해당 게시글 리턴한다.

        :param article_id: 게시글 아이디
        :return: 게시글
        """
        return Article.query.filter(Article.id == article_id).first()

    def post(self):
        pass


class ArticleListView(Resource):

    article_list_fields = {
        'title': fields.String,
        'hits_count': fields.Integer,
        'created_at': fields.DateTime
    }

    @marshal_with(article_list_fields)
    def get(self):
        """ 해당 게시판의 글 목록을 리턴한다.

        :param board_id: 게시판 아이디
        :return: article 리스트
        """

        board_id = request.args.get('board_id')
        return Article.query.filter(Article.board_id == board_id).all()


article = Api(article_bp)
article.add_resource(ArticleView, '/<int:article_id>')
article.add_resource(ArticleListView, '')

