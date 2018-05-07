from flask import abort
from flask import jsonify

def bad_request(message):
    return abort(400, message)


def unauthorized(message):
    return abort(401, message)


def forbidden(message):
    #return abort(403, )
    return jsonify({'CODE': 'USER_NOT_EXISTS', 'data': None}), 403
'''
HTTP Status: 200, 401, 500, 503...

{
    code: 'USER_NOT_EXISTS',
    data: {
    
            ////
    }



}



'''