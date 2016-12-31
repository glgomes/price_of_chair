from functools import wraps

import src.app
from flask import request
from flask import session
from flask import url_for
from flask import redirect


__author__ = 'glgs'


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        return func(*args, **kwargs)
    return decorated_function


def requires_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in src.app.app.config['ADMINS']:
            return redirect(url_for('users.login_user', message="Admin login required"))
        return func(*args, **kwargs)
    return decorated_function