from flask import jsonify, Response
from flask_restful import Resource, marshal_with, fields

import json

from app import db
from app.api.v1.posts import post_fields
from app.models.post import Post

class Pen:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Desk:
    def __init__(self, pen):
        self.pen = pen

    def __str__(self):
        return self.pen.name


class House:
    def __init__(self, desk):
        self.desk = desk


post_fields = {
    'desk': fields.String
}


def get_obj_to_dict(obj):

    posts_json = json.dumps([ob.__dict__ for ob in obj])

    return json.loads(posts_json)

class PostController(Resource):

    ''''@marshal_with(post_fields)
    def get(self):
        data = House(Desk(Pen("pen name")))
        return data'''

    def get(self):
        pen_list = list()
        pen_list.append(Pen("pen1"))
        pen_list.append(Pen("pen2"))


        pen_json = get_obj_to_dict(pen_list)

        return jsonify(pen_json)
