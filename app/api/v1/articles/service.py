from flask import g

from app import db
from app.api.v1.articles.models import Article, YesOrNo
from datetime import datetime

from app.api.v1.boards.models import UserBoardConnector
from app.api.v1.common.exception.exceptions import CommonException, AccountException


def get_article_with_id(request_article_id: int) -> Article:
    article = Article.query.filter(Article.id == request_article_id).first()
    if not article:
        raise CommonException("No article found with articleId: {}".format(request_article_id))

    _validate_article_in_board(article)
    _increase_hits_count(article)

    return article


def delete_article_with_id(request_article_id: int) -> None:
    article = Article.query.filter(Article.id == request_article_id).first()
    if not article:
        raise CommonException("No article found with articleId: {}".format(request_article_id))

    _validate_article_in_board(article)
    _delete_article(article)


def _validate_article_in_board(article) -> None:
    connector = UserBoardConnector.query.filter(UserBoardConnector.user_id == g.current_user.id).first()
    if not connector.check_board_id(article.board_id):
        raise AccountException('Permission denied')


def _increase_hits_count(article: Article) -> None:
    article.hits_count = article.hits_count + 1
    article.updated_at = datetime.utcnow()
    db.session.add(article)
    db.session.commit()


def _delete_article(article: Article) -> None:
    article.deleted = YesOrNo.Y
    article.updated_at = datetime.utcnow()
    db.session.add(article)
    db.session.commit()
