from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
url_prefix = '/api/v1'


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from app.api.v1.common.views import common_bp
    from app.api.v1.articles.views import article_bp
    from app.api.v1.boards.views import board_bp
    from app.api.v1.users.views import user_bp
    app.register_blueprint(common_bp, url_prefix=url_prefix)
    app.register_blueprint(article_bp, url_prefix=url_prefix + '/articles')
    app.register_blueprint(board_bp, url_prefix=url_prefix + '/boards')
    app.register_blueprint(user_bp, url_prefix=url_prefix + '/users')

    db.init_app(app)

    return app
