from flask import abort


def bad_request(message):
    return abort(400, message)


def unauthorized(message):
    return abort(401, message)


def forbidden(message):
    return abort(403, message)
