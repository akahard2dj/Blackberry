from flask import request, jsonify, g
from flask_restplus import Resource, fields, marshal_with

from app import db, api_holder
from app.api.v1.authentications.authentication import auth
from app.api.v1.authentications.errors import forbidden
from app.api.v1.boards.models import UserBoardConnector
from app.api.v1.articles.exceptions import ArticleNotFoundException, BoardIdNotExistException
from app.api.v1.articles.models import Article

api = api_holder[0]

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


@api.route('/articles/<int:article_id>')
@api.header('Authorization', 'Token', required=True)
class ArticleView(Resource):
    decorators = [auth.login_required]
    parser = api.parser()
    parser.add_argument('board_id', type=int)

    @api.expect(parser)
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


@api.route('/articles')
@api.header('Authorization', 'Token', required=True)
class ArticleListView(Resource):
    decorators = [auth.login_required]
    parser = api.parser()
    parser.add_argument('board_id', type=int)

    resource_fields = api.model('Resource', {
        'title': fields.String,
        'body': fields.String,
    })

    @api.expect(parser)
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

    @api.expect(parser, resource_fields)
    def post(self):
        """
        게시판에 글을 작성한다

        :param board_id: 게시판 아이디
        :return:
        """
        data = request.json
        board_id = request.args.get('board_id')
        if not board_id:
            raise BoardIdNotExistException('board_id is mandatory!')

        article = Article(title=data['title'], body=data['body'], board_id=board_id)

        db.session.add(article)
        db.session.commit()

        return {"id": article.id}


@api.errorhandler(ArticleNotFoundException)
def handle_not_found_article_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

