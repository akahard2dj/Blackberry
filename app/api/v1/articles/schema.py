from app import ma


class ArticleListSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'hits_count', 'created_at')
