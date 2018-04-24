from app.models.post import Post


class PostDTO(object):
    def __init__(self, p: Post):
        self.id = p.id
        self.title = p.title
        self.body = p.body
