from flask import Flask, Blueprint
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

from werkzeug.contrib.cache import SimpleCache

from config import config

db = SQLAlchemy()
cache = SimpleCache()
_api_holder = []


def get_api():
    return _api_holder[0]


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api = Api(api_blueprint, title='Blackberry', default='API',
              default_label='전체 리스트',
              doc='/docs')
    app.register_blueprint(api_blueprint)
    _api_holder.append(api)

    from app.api.v1.common.views import api
    from app.api.v1.articles.views import api
    from app.api.v1.authentications.views import api
    from app.api.v1.boards.views import api
    from app.api.v1.users.views import api
    from app.api.v1.common.exception import handler

    db.init_app(app)

    return app
