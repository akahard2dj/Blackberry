from flask import request, g
from flask_restplus import Resource, fields, marshal_with

from sqlalchemy import desc

from app import db, get_api
from app.api.v1.authentications.authentication import auth
from app.api.v1.boards.models import UserBoardConnector
from app.api.v1.articles.models import Article
from app.api.v1.common.exception.exceptions import AccountException, CommonException
from app.api.v1.common.views import ResponseWrapper

api = get_api()

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

article_response = {
    'message': fields.String,
    'data': fields.Nested(article_fields)
}

article_list_response = {
    'message': fields.String,
    'data': fields.List(fields.Nested(article_list_fields))
}


@api.route('/articles/<int:article_id>')
@api.header('Authorization', 'Token', required=True)
class ArticleView(Resource):
    decorators = [auth.login_required]
    parser = api.parser()
    parser.add_argument('board_id', type=int)

    @api.expect(parser)
    @marshal_with(article_fields)
    def get(self, article_id: int):
        """ 해당 게시글 리턴한다.

        :param article_id: 게시글 아이디
        :return: 게시글
        """
        article = Article.query.filter(Article.id == article_id).first()
        connector = UserBoardConnector.query.filter(UserBoardConnector.user_id == g.current_user.id).first()

        if not article:
            raise CommonException("No article found with articleId: {}".format(article_id))
        if not connector.check_board_id(article.board_id):
            raise AccountException('Permission denied')

        return article


@api.route('/articles')
@api.header('Authorization', '발급된 사용자 토큰', required=True)
class ArticleListView(Resource):
    decorators = [auth.login_required]
    parser = api.parser()
    parser.add_argument('board_id', type=int)

    resource_fields = api.model('Resource', {
        'title': fields.String,
        'body': fields.String,
    })

    @api.expect(parser)
    @marshal_with(article_list_response)
    def get(self):
        """ 해당 게시판의 글 목록을 리턴한다.

        :param board_id: 게시판 아이디
        :return: article list(msg, items)
        """
        board_id = request.args.get('board_id')

        connector = UserBoardConnector.query.filter(UserBoardConnector.user_id == g.current_user.id).first()
        if connector is None:
            raise AccountException('permission denied: There is no user data on connector table')
        if not connector.check_board_id(board_id):
            raise AccountException('permission denied')

        # TODO: pagination is needed
        articles = Article.query.order_by(desc(Article.created_at)).all()
        items = Article.query.filter(Article.board_id == board_id).all()
        return ResponseWrapper.ok('successfully loaded', articles)

    @api.expect(parser, resource_fields)
    def post(self):
        """
        게시판에 글을 작성한다

        :param board_id: 게시판 아이디
        :return:
        """
        data = request.json
        board_id = request.args.get('board_id')
        connector = UserBoardConnector.query.filter(UserBoardConnector.user_id == g.current_user.id).first()

        if not board_id:
            raise CommonException('board_id is mandatory!')
        if connector is None:
            raise AccountException('Permission denied')
        if not connector.check_board_id(board_id):
            raise AccountException('Permission denied')

        article = Article(title=data['title'], body=data['body'], board_id=board_id)

        db.session.add(article)
        db.session.commit()

        return ResponseWrapper.ok('successfully loaded', {"id": article.id})


