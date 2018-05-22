from marshmallow import fields, post_load

from app import ma
from app.api.v1.articles.models import Article


class ArticleListSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'hits_count', 'created_at')


class ArticleSchema(ma.Schema):

    title = fields.Str()
    board_id = fields.Integer()
    body = fields.Str()
    hits_count = fields.Integer()
    updated_at = fields.DateTime()
    created_at = fields.DateTime()
    likes_count = fields.Integer()
    dislike_count = fields.Integer()
    deleted = fields.Str()
    reported = fields.Str()

    @post_load
    def make_article(self, data):
        return Article(**data)
