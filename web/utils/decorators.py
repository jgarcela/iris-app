# web/decorators.py
from functools import wraps
from flask import abort, request, redirect, url_for, current_app
import requests
from flask_jwt_extended import get_jwt_identity
from bson import ObjectId
from database.db import DB_USERS, DB_ROLES


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token_cookie')
        if not token:
            return redirect(url_for('auth.login'))
        # opcional: validar token con /api/me
        return f(*args, **kwargs)
    return decorated


# def role_required(*required_roles):
#     def wrapper(fn):
#         @wraps(fn)
#         def decorated(*args, **kwargs):
#             user_id = get_jwt_identity()
#             user = DB_USERS.find_one({'_id':ObjectId(user_id)})
#             if not user:
#                 abort(401)
#             if not set(user.get('roles',[])) & set(required_roles):
#                 abort(403)
#             return fn(*args, **kwargs)
#         return decorated
#     return wrapper

# def permission_required(*required_perms):
#     def wrapper(fn):
#         @wraps(fn)
#         def decorated(*args, **kwargs):
#             user_id = get_jwt_identity()
#             user = DB_USERS.find_one({'_id':ObjectId(user_id)})
#             if not user:
#                 abort(401)
#             # recolecta permisos de todos sus roles
#             perms = set()
#             for role_name in user.get('roles',[]):
#                 role = DB_ROLES.find_one({'name':role_name})
#                 if role:
#                     perms |= set(role.get('permissions',[]))
#             if not set(required_perms) <= perms:
#                 abort(403)
#             return fn(*args, **kwargs)
#         return decorated
#     return wrapper

