from flask import abort


# TODO: CommonException 으로 교체.
def bad_request(message):
    return abort(400, message)
