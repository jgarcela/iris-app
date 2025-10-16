# 🎯 Event Decorators Template
# Copia este archivo y renómbralo según tu evento
# Ejemplo: web/utils/concurso_literario_decorators.py

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
    """Obtener el usuario actual desde la API"""
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

def event_required(f):
    """
    Decorador que requiere que el usuario tenga rol específico del evento o 'admin'
    Los admins tienen acceso automático sin necesidad del rol específico
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"[DEBUG] event_required decorator called")
        
        # Obtener el usuario actual
        current_user = get_current_user()
        print(f"[DEBUG] Current user: {current_user}")
        
        # Verificar si el usuario está autenticado
        if not current_user:
            print("[DEBUG] No current_user, redirecting to login")
            flash(_('Debes iniciar sesión para acceder al evento'), 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        # Obtener roles del usuario
        user_roles = current_user.get('roles', [])
        print(f"[DEBUG] User roles: {user_roles}")
        
        # Verificar si el usuario tiene rol del evento o admin
        if 'admin' in user_roles:
            print("[DEBUG] Admin access granted")
            return f(*args, **kwargs)
        elif 'nombre_evento' in user_roles:  # Cambiar por el nombre del rol específico
            print("[DEBUG] Event user access granted")
            return f(*args, **kwargs)
        else:
            print(f"[DEBUG] Access denied. User roles: {user_roles}")
            flash(_('No tienes permisos para acceder a este evento. Contacta al administrador.'), 'error')
            return redirect(url_for('home'))
        
    return decorated_function

def event_only(f):
    """
    Decorador que permite acceso solo a usuarios con rol específico del evento o 'admin'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtener el usuario actual
        current_user = get_current_user()
        
        # Verificar si el usuario está autenticado
        if not current_user:
            flash(_('Debes iniciar sesión para acceder al evento'), 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        # Obtener roles del usuario
        user_roles = current_user.get('roles', [])
        if 'admin' in user_roles:
            # Los admins tienen acceso automático
            return f(*args, **kwargs)
        elif 'nombre_evento' in user_roles:  # Cambiar por el nombre del rol específico
            # Los usuarios con rol específico tienen acceso
            return f(*args, **kwargs)
        else:
            flash(_('Acceso restringido al evento. Solo participantes autorizados.'), 'error')
            return redirect(url_for('home'))
        
    return decorated_function

def event_admin_required(f):
    """
    Decorador para administradores del evento
    Permite gestionar usuarios del evento
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
            flash(_('No tienes permisos de administrador del evento'), 'error')
            return redirect(url_for('home'))
        
        return f(*args, **kwargs)
    return decorated_function
