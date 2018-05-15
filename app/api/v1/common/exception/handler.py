from app import get_api
from app.api.v1.common.exception.exceptions import AccountException, CommonException

api = get_api()


@api.errorhandler(AccountException)
def handle_account_exception(error):
    return error.to_dict(), error.status_code


@api.errorhandler(CommonException)
def handle_common_exception(error):
    return error.to_dict(), error.status_code
