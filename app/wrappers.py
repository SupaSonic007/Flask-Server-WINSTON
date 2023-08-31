from functools import wraps
from flask_login import current_user
from flask import abort


def admin_required(function):
    '''
    Check if a user is admin, if not, return 401
    '''
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.admin == False:
            abort(401)
        return function(*args, **kwargs)

    return decorated_function
