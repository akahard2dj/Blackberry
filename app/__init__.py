from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from app.api.v1.controller import api_bp

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.register_blueprint(api_bp, url_prefix='/api/v1')

    db.init_app(app)

    return app
