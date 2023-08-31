from functools import wraps
from flask_login import current_user, login_required
from flask import current_app, abort


def admin_required(f):
    '''
    Check if a user is admin, if not, return 401
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(404)
        if current_user.admin == False:
            abort(404)
        return f(*args, **kwargs)

    return decorated_function
