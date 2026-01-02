# web/decorators.py
from functools import wraps
from flask import abort, request, redirect, url_for, current_app, flash
from flask_babel import gettext as _
import requests
from flask_jwt_extended import get_jwt_identity
from bson import ObjectId
from database.db import DB_USERS, DB_ROLES
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
API_HOST = config['API']['HOST']
API_PORT = config['API']['PORT']
ENDPOINT_AUTH = config['API']['ENDPOINT_AUTH']
ENDPOINT_AUTH_ME = config['API']['ENDPOINT_AUTH_ME']
URL_API_ENDPOINT_AUTH_ME = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_AUTH}/{ENDPOINT_AUTH_ME}"

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token_cookie')
        if not token:
            return redirect(url_for('auth.login'))
        # opcional: validar token con /api/me
        return f(*args, **kwargs)
    return decorated


def challenge_restricted(f):
    """Decorator to restrict access for users with 'challenge' role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get user from session or make API call to get current user
        token = request.cookies.get('access_token_cookie')
        if token:
            try:
                headers = {'Authorization': f'Bearer {token}'}
                resp = requests.get(f"http://{API_HOST}:{API_PORT}/auth/me", headers=headers, timeout=2)

                if resp.ok:
                    user = resp.json().get('user')
                    if user and 'challenge' in user.get('roles', []):
                        abort(403)  # Forbidden for challenge users
            except Exception:
                pass
        return f(*args, **kwargs)
    return decorated


def analyst_or_admin_required(f):
    """
    Decorator that requires the user to have 'analyst' or 'admin' role
    Admins have automatic access
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get user from session or make API call to get current user
        token = request.cookies.get('access_token_cookie')
        if not token:
            flash(_('Debes iniciar sesión para acceder a esta sección'), 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        try:
            headers = {'Authorization': f'Bearer {token}'}
            resp = requests.get(URL_API_ENDPOINT_AUTH_ME, headers=headers, timeout=2)
            
            if resp.ok:
                user = resp.json().get('user')
                if user:
                    user_roles = user.get('roles', [])
                    # Check if user has analyst or admin role
                    if 'admin' in user_roles or 'analyst' in user_roles:
                        return f(*args, **kwargs)
                    else:
                        flash(_('No tienes permisos para acceder a esta sección. Se requiere rol de analista o administrador.'), 'error')
                        return redirect(url_for('home'))
                else:
                    flash(_('No se pudo obtener la información del usuario'), 'error')
                    return redirect(url_for('auth.login'))
            else:
                flash(_('Error de autenticación'), 'error')
                return redirect(url_for('auth.login'))
        except Exception as e:
            flash(_('Error al verificar permisos'), 'error')
            return redirect(url_for('home'))
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

