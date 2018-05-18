import enum
import json
from datetime import datetime

from app import db


class ArticleStatus(enum.Enum):
    USE = 'USE',
    DELETED = 'DELETED',
    REPORTED = 'REPORTED'


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(ArticleStatus), default='USE')
    title = db.Column(db.Text)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    body = db.Column(db.Text)
    hits_count = db.Column(db.Integer, default=1)
    likes_count = db.Column(db.Integer, default=0)
    dislike_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

        return True

    def increase_hits_count(self):
        self.hits_count = self.hits_count + 1
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            return False

        return True


'''
class ArticleDTO(object):
    def __init__(self, p: Article):
        self.id = p.id
        self.title = p.title
        self.body = p.body


class ArticleDAO(object):
    def __init__(self):
        self.__post = None

    def get_articles_obj(self):
        q = Article.query.all()
        posts = list()
        for p in q:
            post_dto = ArticleDTO(p)
            posts.append(post_dto)

        return posts

    def get_articles_dict(self):
        q = Article.query.all()
        articles = list()
        for p in q:
            article_dto = ArticleDTO(p)
            articles.append(article_dto)

        posts_json = json.dumps([ob.__dict__ for ob in articles])

        return json.loads(posts_json)'''
