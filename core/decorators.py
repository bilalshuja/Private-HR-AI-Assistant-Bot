from functools import wraps
from flask import abort
from flask_login import current_user

def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
       
        if not current_user.is_authenticated or current_user.role != 'super_admin':
            return abort(403) 
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        if not current_user.is_authenticated or current_user.role != 'admin':
            return abort(403) # Permission Denied
        return f(*args, **kwargs)
    return decorated_function