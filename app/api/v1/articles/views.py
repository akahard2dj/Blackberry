from flask import Blueprint, request, jsonify
from flask_restful import Resource, fields, Api, marshal_with

from app import db
from app.api.v1.articles.exceptions import ArticleNotFoundException, BoardIdNotExistException
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
        article = Article.query.filter(Article.id == article_id).first()
        if not article:
            raise ArticleNotFoundException(f"No article found with articleId: {article_id}")

        return article


class ArticleAdd(Resource):

    def post(self):
        data = request.json
        board_id = request.args.get('board_id')
        if not board_id:
            raise BoardIdNotExistException('board_id is mandatory!')

        article = Article(title=data['title'], body=data['body'], board_id=board_id)

        db.session.add(article)
        db.session.commit()

        return {"id": article.id}


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


@article_bp.errorhandler(ArticleNotFoundException)
def handle_not_found_article_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


article = Api(article_bp)
article.add_resource(ArticleView, '/<int:article_id>')
article.add_resource(ArticleListView, '')
article.add_resource(ArticleAdd, '')

