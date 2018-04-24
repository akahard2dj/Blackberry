from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from app.api.v1_0 import api_bp as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1')

    db.init_app(app)

    return app
