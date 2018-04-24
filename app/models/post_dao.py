from app.models.post import Post
from app.models.post_dto import PostDTO

from app import db

class PostDAO(object):
    def __init__(self):
        self.__post = None

    def get_posts(self):
        q = Post.query.all()
        posts = list()
        for p in q:
            post_dto = PostDTO()
            post_dto.id = p.id
            post_dto.title = p.title
            post_dto.body = p.body
            posts.append(post_dto)

        return posts
