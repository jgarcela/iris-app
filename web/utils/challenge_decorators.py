# web/utils/challenge_decorators.py
from functools import wraps
from flask import session, redirect, url_for, flash, request, g
from flask_babel import gettext as _
import requests
import configparser

# Configuración para la API
config = configparser.ConfigParser()
config.read('config.ini')
API_HOST = config['API']['HOST']
API_PORT = config['API']['PORT']
ENDPOINT_AUTH = config['API']['ENDPOINT_AUTH']
ENDPOINT_AUTH_ME = config['API']['ENDPOINT_AUTH_ME']
URL_API_ENDPOINT_AUTH_ME = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_AUTH}/{ENDPOINT_AUTH_ME}"

def get_current_user():
    """Obtener el usuario actual desde la API (igual que inject_user)"""
    token = request.cookies.get('access_token_cookie')
    if not token:
        return None
    
    try:
        headers = {'Authorization': f'Bearer {token}'}
        resp = requests.get(URL_API_ENDPOINT_AUTH_ME, headers=headers, timeout=2)
        if resp.ok:
            user = resp.json().get('user')
            return user
    except Exception as e:
        print(f"[DEBUG] Error getting current user: {e}")
        pass
    
    return None

def challenge_required(f):
    """
    Decorador que requiere que el usuario tenga rol 'challenge' o 'admin'
    Los admins tienen acceso automático sin necesidad del rol challenge
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"[DEBUG] challenge_required decorator called")
        
        # Obtener el usuario actual
        current_user = get_current_user()
        print(f"[DEBUG] Current user: {current_user}")
        
        # Verificar si el usuario está autenticado
        if not current_user:
            print("[DEBUG] No current_user, redirecting to login")
            flash(_('Debes iniciar sesión para acceder al desafío'), 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        # Obtener roles del usuario
        user_roles = current_user.get('roles', [])
        print(f"[DEBUG] User roles: {user_roles}")
        
        # Verificar si el usuario tiene rol de desafío o admin
        if 'admin' in user_roles:
            print("[DEBUG] Admin access granted")
            return f(*args, **kwargs)
        elif 'challenge' in user_roles:
            print("[DEBUG] Challenge user access granted")
            return f(*args, **kwargs)
        else:
            print(f"[DEBUG] Access denied. User roles: {user_roles}")
            flash(_('No tienes permisos para acceder al desafío. Contacta al administrador.'), 'error')
            return redirect(url_for('home'))
        
    return decorated_function

def challenge_only(f):
    """
    Decorador que permite acceso a usuarios con rol 'challenge' o 'admin'
    Los admins tienen acceso completo a todas las funcionalidades
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtener el usuario actual
        current_user = get_current_user()
        
        # Verificar si el usuario está autenticado
        if not current_user:
            flash(_('Debes iniciar sesión para acceder al desafío'), 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        # Obtener roles del usuario
        user_roles = current_user.get('roles', [])
        if 'admin' in user_roles:
            # Los admins tienen acceso automático
            return f(*args, **kwargs)
        elif 'challenge' in user_roles:
            # Los usuarios con rol challenge tienen acceso
            return f(*args, **kwargs)
        else:
            flash(_('Acceso restringido al Desafío IRIS. Solo participantes autorizados.'), 'error')
            return redirect(url_for('home'))
        
    return decorated_function

def challenge_admin_required(f):
    """
    Decorador para administradores del desafío
    Permite gestionar usuarios del desafío
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtener el usuario actual
        current_user = get_current_user()
        
        # Verificar si el usuario está autenticado
        if not current_user:
            flash(_('Debes iniciar sesión'), 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        # Obtener roles del usuario
        user_roles = current_user.get('roles', [])
        if 'admin' not in user_roles:
            flash(_('No tienes permisos de administrador del desafío'), 'error')
            return redirect(url_for('home'))
        
        return f(*args, **kwargs)
    return decorated_function
