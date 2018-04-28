from flask_restful import Resource


class HelloController(Resource):

    def get(self):
        """
            health check 용 api. 지우지 말것
        """
        return "hello"
