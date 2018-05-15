class AccountException(Exception):
    """ 계정/인증 오류 """
    status_code = 403

    def __init__(self, message, body=None):
        Exception.__init__(self)
        self.message = message
        self.body = body

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        rv['data'] = self.body
        return rv


class CommonException(Exception):
    """ 서비스 불가능 """
    status_code = 503

    def __init__(self, message, body=None):
        Exception.__init__(self)
        self.message = message
        self.body = body

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        rv['data'] = self.body
        return rv
