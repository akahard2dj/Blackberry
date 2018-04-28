from flask import Blueprint

common_bp = Blueprint('common', __name__)


@common_bp.route('/hello')
def hello():
    return "hello"
