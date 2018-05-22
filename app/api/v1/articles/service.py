from flask import g

from app import db
from app.api.v1.articles.models import Article, YesOrNo
from datetime import datetime

from app.api.v1.articles.schema import ArticleSchema
from app.api.v1.boards.models import UserBoardConnector
from app.api.v1.common.exception.exceptions import CommonException, AccountException


def get_article_with_id(request_article_id: int) -> Article:
    article = Article.query.filter(Article.id == request_article_id).first()
    if not article:
        raise CommonException("No article found with articleId: {}".format(request_article_id))

    article_dict = ArticleSchema(only=('title', 'body', 'board_id', 'hits_count', 'created_at')).dump(article).data
    _validate_article_in_board(article_dict)
    _increase_hits_count(article_dict)

    return ArticleSchema(only=('title', 'body', 'board_id', 'hits_count', 'created_at')).dump(article).data


def delete_article_with_id(request_article_id: int) -> None:
    article = Article.query.filter(Article.id == request_article_id).first()
    if not article:
        raise CommonException("No article found with articleId: {}".format(request_article_id))

    article_dict = ArticleSchema().dump(article)
    _validate_article_in_board(article_dict)
    _delete_article(article_dict)


def create_article(title: str, content: str, board_id: int, user_id: int) -> dict:
    if not board_id:
        raise CommonException('board_id is mandatory!')
    _validate_right_board(user_id, board_id)

    article = Article(title=title, body=content, board_id=board_id)
    db.session.add(article)
    db.session.commit()

    return {"id": article.id}


def _validate_right_board(user_id: int, board_id: int) -> None:
    connector = UserBoardConnector.query.filter(UserBoardConnector.user_id == user_id).first()
    if connector is None:
        raise AccountException('Permission denied')
    if not connector.check_board_id(board_id):
        raise AccountException('Permission denied')


def _validate_article_in_board(article: dict) -> None:
    connector = UserBoardConnector.query.filter(UserBoardConnector.user_id == g.current_user.id).first()
    if not connector.check_board_id(article['board_id']):
        raise AccountException('Permission denied')


def _increase_hits_count(article: dict) -> None:
    article['hits_count'] += 1
    article['updated_at'] = str(datetime.utcnow())

    a = ArticleSchema().load(article)
    db.session.add(a.data)
    db.session.commit()


def _delete_article(article: dict) -> None:
    article['deleted'] = YesOrNo.Y
    article['updated_at'] = datetime.utcnow()

    db.session.add(ArticleSchema().load(article))
    db.session.commit()
