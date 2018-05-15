from flask import request, jsonify, g
from flask_restplus import Resource, fields, marshal_with

from app import db, get_api
from app.api.v1.authentications.authentication import auth
from app.api.v1.authentications.errors import forbidden
from app.api.v1.boards.models import UserBoardConnector
from app.api.v1.articles.exceptions import ArticleNotFoundException, BoardIdNotExistException
from app.api.v1.articles.models import Article

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
    'msg': fields.String,
    'items': fields.Nested(article_fields)
}

article_list_response = {
    'msg': fields.String,
    'items': fields.List(fields.Nested(article_list_fields))
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
            raise ArticleNotFoundException("No article found with articleId: {}".format(article_id))

        if not connector.check_board_id(article.board_id):
            forbidden('Permission denied')

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

        output_dict = dict()
        # TODO: connector 가 None 일 때 처리 필요 -> solved
        if connector is None:
            output_dict['msg'] = 'permission denied: There is no user data on connector table'
            output_dict['items'] = None
            return output_dict, 403

        if not connector.check_board_id(board_id):
            output_dict['msg'] = 'permission denied'
            output_dict['items'] = None
            return output_dict, 403

        # TODO: pagination is needed
        output_dict['msg'] = 'successfully loaded'
        output_dict['items'] = Article.query.filter(Article.board_id == board_id).all()
        return output_dict

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
            raise BoardIdNotExistException('board_id is mandatory!')

        if connector is None:
            return jsonify({'msg': 'permission denied'}), 403

        if not connector.check_board_id(board_id):
            return jsonify({'msg': 'permission denied'}), 403

        article = Article(title=data['title'], body=data['body'], board_id=board_id)

        db.session.add(article)
        db.session.commit()

        return {"id": article.id}


@api.errorhandler(ArticleNotFoundException)
def handle_not_found_article_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

