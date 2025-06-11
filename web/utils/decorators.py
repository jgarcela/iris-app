# web/decorators.py
from functools import wraps
from flask import request, redirect, url_for, current_app
import requests

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token_cookie')
        if not token:
            return redirect(url_for('auth.login'))
        # opcional: validar token con /api/me
        return f(*args, **kwargs)
    return decorated
