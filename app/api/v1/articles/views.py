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
@api.header('Authorization', 'Token 정보', required=True)
class ArticleView(Resource):

    decorators = [auth.login_required]

    @marshal_with(article_response)
    def get(self, article_id: int):
        """ 해당 게시글 리턴한다. """

        article = Article.query.filter(Article.id == article_id).first()
        if not article:
            raise CommonException("No article found with articleId: {}".format(article_id))

        connector = UserBoardConnector.query.filter(UserBoardConnector.user_id == g.current_user.id).first()
        if not connector.check_board_id(article.board_id):
            raise AccountException('Permission denied')

        if not article.increase_hits_count():
            raise CommonException("Server is not response")

        return ResponseWrapper.ok(data=article)

    def put(self):
        pass

    def delete(self):
        pass


@api.route('/articles')
@api.header('Authorization', '발급된 사용자 토큰', required=True)
class ArticleListView(Resource):

    decorators = [auth.login_required]

    parser = api.parser()
    parser.add_argument('board_id', type=int, required=True, help='게시판 아이디')
    parser.add_argument('query_id', type=int)
    parser.add_argument('page', type=int)
    parser.add_argument('articles_per_page', type=int)

    @api.expect(parser)
    @marshal_with(article_list_response)
    def get(self):
        """ 해당 게시판의 글 목록을 리턴한다. """

        query_args = self.parser.parse_args()

        board_id = query_args["board_id"]

        connector = UserBoardConnector.query.filter(UserBoardConnector.user_id == g.current_user.id).first()
        if connector is None:
            raise AccountException('permission denied: There is no user data on connector table')
        if not connector.check_board_id(board_id):
            raise AccountException('permission denied')

        if query_args["page"] is None:
            page = 1
        else:
            page = query_args["page"]

        if query_args["articles_per_page"] is None:
            articles_per_page = 10
        else:
            articles_per_page = query_args["articles_per_page"]

        if page == 1:
            article_query = Article.query\
                .filter(Article.board_id == board_id)\
                .order_by(desc(Article.created_at)).first()
            query_id = article_query.id
        else:
            query_id = query_args["query_id"]

        articles = Article.query\
            .filter(Article.board_id == board_id)\
            .filter(Article.id <= query_id)\
            .order_by(desc(Article.created_at))\
            .limit(articles_per_page)\
            .offset((page-1)*articles_per_page)
        return ResponseWrapper.ok(data=articles)

    parser = api.parser()
    parser.add_argument('board_id', type=int, required=True, help='게시판 아이디')

    article_request_body = api.model('ArticleRequestBody', {
        'title': fields.String,
        'body': fields.String,
    })

    @api.expect(parser, article_request_body)
    def post(self):
        """ 게시판에 글을 작성한다 """

        query_parameter = self.parser.parse_args()
        body_data = request.json
        board_id = query_parameter['board_id']

        if not board_id:
            raise CommonException('board_id is mandatory!')

        connector = UserBoardConnector.query.filter(UserBoardConnector.user_id == g.current_user.id).first()
        if connector is None:
            raise AccountException('Permission denied')
        if not connector.check_board_id(board_id):
            raise AccountException('Permission denied')

        article = Article(title=body_data['title'], body=body_data['body'], board_id=board_id)
        db.session.add(article)
        db.session.commit()

        return ResponseWrapper.ok(data={"id": article.id})


