from sqlalchemy.exc import SQLAlchemyError

from app import get_api
from app.api.v1.common.exception.exceptions import AccountException, CommonException

api = get_api()


@api.errorhandler(AccountException)
def handle_account_exception(error):
    return error.to_dict(), error.status_code


@api.errorhandler(CommonException)
def handle_common_exception(error):
    return error.to_dict(), error.status_code


@api.errorhandler(SQLAlchemyError)
def handle_sql_exception(error):
    return {'message:' 'SQL 오류가 발생했습니다.'}, 500
