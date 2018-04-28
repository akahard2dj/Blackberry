import json

from api.v1.models.post import Post
from api.v1.models.post_dto import PostDTO


class PostDAO(object):
    def __init__(self):
        self.__post = None

    def get_posts_obj(self):
        q = Post.query.all()
        posts = list()
        for p in q:
            post_dto = PostDTO(p)
            posts.append(post_dto)

        return posts

    def get_posts_dict(self):
        q = Post.query.all()
        posts = list()
        for p in q:
            post_dto = PostDTO(p)
            posts.append(post_dto)

        posts_json = json.dumps([ob.__dict__ for ob in posts])

        return json.loads(posts_json)
