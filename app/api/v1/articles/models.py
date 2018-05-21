import enum
from datetime import datetime

from app import db
from app import ma

class YesOrNo(enum.Enum):
    Y = 'Y'
    N = 'N'


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    body = db.Column(db.Text)
    hits_count = db.Column(db.Integer, default=1)
    likes_count = db.Column(db.Integer, default=0)
    dislike_count = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Enum(YesOrNo), default='N')
    reported = db.Column(db.Enum(YesOrNo), default='N')
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class ArticleListSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'hits_count', 'created_at')


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
