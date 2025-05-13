from functools import wraps
from flask import redirect, url_for, session

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for("auth_routes.login"))
            if role and session.get("role") != role:
                return redirect(url_for("auth_routes.login"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
