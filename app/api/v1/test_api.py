from flask_restful import Resource


class TestApi(Resource):

    def get(self):
        return {'hello': 'world'}
