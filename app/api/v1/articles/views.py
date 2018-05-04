from flask import Blueprint, request, jsonify, g
from flask_restplus import Resource, fields, Api, marshal_with

from app import db
from app.api.v1.authentications.authentication import auth
from app.api.v1.authentications.errors import forbidden
from app.api.v1.boards.models import UserBoardConnector
from app.api.v1.articles.exceptions import ArticleNotFoundException, BoardIdNotExistException
from app.api.v1.articles.models import Article

article_bp = Blueprint('article', __name__)
api = Api(article_bp)

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

article_list_fields = {
        'id': fields.Integer,
        'title': fields.String,
        'hits_count': fields.Integer,
        'created_at': fields.DateTime
}


@api.route('/<int:article_id>')
class ArticleView(Resource):
    decorators = [auth.login_required]
    
    @marshal_with(article_fields)
    def get(self, article_id):
        """ 해당 게시글 리턴한다.

        :param article_id: 게시글 아이디
        :return: 게시글
        """
        article = Article.query.filter(Article.id == article_id).first()
        connector = UserBoardConnector.query.filter(UserBoardConnector.user_id == g.current_user.id).first()

        if not article:
            raise ArticleNotFoundException("No article found with articleId: {}".format(article_id))
        else:
            if connector.check_board_id(article.board_id):
                return article
            else:
                forbidden('Permission denied')


@api.route('')
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


@api.route('')
class ArticleListView(Resource):
    decorators = [auth.login_required]

    @marshal_with(article_list_fields)
    def get(self):
        """ 해당 게시판의 글 목록을 리턴한다.

        :param board_id: 게시판 아이디
        :return: article 리스트
        """
        board_id = request.args.get('board_id')

        connector = UserBoardConnector.query.filter(UserBoardConnector.user_id == g.current_user.id).first()
        if connector.check_board_id(board_id):
            # TODO: pagination is needed
            return Article.query.filter(Article.board_id == board_id).all()
        else:
            forbidden("Permission denied")


@article_bp.errorhandler(ArticleNotFoundException)
def handle_not_found_article_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

