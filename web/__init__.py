# web/__init__.py

# ==================================
#  LIBRARIES 
# ==================================
from flask import Flask, current_app, redirect, request, render_template, jsonify, session, url_for
from datetime import timezone
try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:
    ZoneInfo = None
import configparser
from flask_cors import CORS
from functools import wraps
from flask_babel import Babel
from flask_babel import gettext as _
import requests
import ast



# ==================================
#  CONFIG 
# ==================================
config = configparser.ConfigParser()
config.read('config.ini')

# ----------------- VARIABLES -----------------
WEB_HOST = config['WEB']['HOST']
WEB_PORT = config['WEB']['PORT']
DEBUG = config['WEB'].getboolean('DEBUG')
API_HOST = config['API']['HOST']
API_PORT = config['API']['PORT']
API_HEADERS_str = config['API']['HEADERS']
API_HEADERS = ast.literal_eval(API_HEADERS_str)
ENDPOINT_ANALYSIS = config['API']['ENDPOINT_ANALYSIS']
ENDPOINT_ANALYSIS_ANALYZE = config['API']['ENDPOINT_ANALYSIS_ANALYZE']
ENDPOINT_AUTH = config['API']['ENDPOINT_AUTH']
ENDPOINT_AUTH_REGISTER = config['API']['ENDPOINT_AUTH_REGISTER']
ENDPOINT_AUTH_LOGIN = config['API']['ENDPOINT_AUTH_LOGIN']
ENDPOINT_AUTH_ME = config['API']['ENDPOINT_AUTH_ME']
ENDPOINT_AUTH_REFRESH = config['API']['ENDPOINT_AUTH_REFRESH']


# ----------------- URLs -----------------
URL_API_ENDPOINT_AUTH = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_AUTH}"
URL_API_ENDPOINT_AUTH_REGISTER = f"{URL_API_ENDPOINT_AUTH}/{ENDPOINT_AUTH_REGISTER}"
URL_API_ENDPOINT_AUTH_LOGIN = f"{URL_API_ENDPOINT_AUTH}/{ENDPOINT_AUTH_LOGIN}"
URL_API_ENDPOINT_AUTH_ME = f"{URL_API_ENDPOINT_AUTH}/{ENDPOINT_AUTH_ME}"
URL_API_ENDPOINT_AUTH_REFRESH = f"{URL_API_ENDPOINT_AUTH}/{ENDPOINT_AUTH_REFRESH}"
URL_API_ENDPOINT_ANALYSIS_ANALYZE = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_ANALYSIS}/{ENDPOINT_ANALYSIS_ANALYZE}"


# ==================================
#  APP 
# ==================================
app = Flask(__name__, static_url_path='/iris/static')
app.config['SECRET_KEY'] = config['DEFAULT']['SECRET_KEY']
app.secret_key = config['DEFAULT']['SECRET_KEY']

# Configuración de idiomas disponibles
app.config['BABEL_TRANSLATION_DIRECTORIES'] = './translations'
app.config['BABEL_DEFAULT_LOCALE'] = 'es'  # Idioma por defecto
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'


# Habilitar CORS para todas las rutas
CORS(app)


# ==================================
#  EXTENSIONES 
# ==================================
# ----------------- LANGUAGE -----------------
# Inicializar Babel con selector de idioma
def get_locale():
    lang = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
    logger.info(f"Language detected: {lang}")
    return lang

babel = Babel(app, locale_selector=get_locale)

@app.context_processor
def inject_language():
    return {'current_language': session.get('language', app.config['BABEL_DEFAULT_LOCALE'])}

@app.context_processor
def inject_config():
    """Inject configuration variables into templates"""
    return {
        'challenge_enabled': config.getboolean('CHALLENGE', 'ENABLED', fallback=False),
        'config': config
    }

@app.context_processor
def inject_admin_unread_contacts():
    """Inject unread contacts count globally (used in navbar/Admin tab)."""
    try:
        from database.db import DB_CONTACT
        unread_count = DB_CONTACT.count_documents({'read': False})
        return {'admin_unread_contacts': int(unread_count)}
    except Exception:
        return {'admin_unread_contacts': 0}

# ==============================
#  JINJA FILTERS
# ==============================
def to_madrid(dt, fmt='%d/%m/%Y %H:%M'):
    """Convert a datetime (assumed UTC if naive) to Europe/Madrid and format.
    Usage in templates: {{ dt|to_madrid('%d/%m/%Y %H:%M') }}
    """
    if not dt:
        return ''
    try:
        if ZoneInfo is None:
            # Fallback: show as-is
            return dt.strftime(fmt)
        # Assume UTC if naive
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        madrid = dt.astimezone(ZoneInfo('Europe/Madrid'))
        return madrid.strftime(fmt)
    except Exception:
        try:
            return dt.strftime(fmt)
        except Exception:
            return ''

app.jinja_env.filters['to_madrid'] = to_madrid


# ----------------- CURRENT USER -----------------
@app.context_processor
def inject_user():
    token = request.cookies.get('access_token_cookie')
    logger.info(f"{token=}")
    if not token:
        return dict(current_user=None)

    try:
        headers = {'Authorization': f'Bearer {token}'}
        resp = requests.get(URL_API_ENDPOINT_AUTH_ME, headers=headers, timeout=2)
        logger.info(f"{resp=}")
        if resp.ok:
            user = resp.json().get('user')
            print(f"{user=}")
            # Store user_id in session for analysis routes
            if user and user.get('_id'):
                session['user_id'] = str(user['_id'])
                session['user_email'] = user.get('email', '')
            return dict(current_user=user)
    except Exception:
        pass

    return dict(current_user=None)


# ----------------- DECORATORS -----------------
from web.utils.decorators import login_required

# ----------------- LOGGER -----------------
from web.utils.logger import logger

# ==================================
#  BLUEPRINTS 
# ==================================
from web.routes.analysis import bp as analysis_bp
from web.routes.dashboard import bp as dashboard_bp
from web.routes.report import bp as report_bp
from web.routes.table import bp as table_bp
from web.routes.auth import bp as auth_bp
from web.routes.contact import bp as contact_bp
from web.routes.admin import bp as admin_bp
# Optional blueprints depending on configuration
try:
    from web.routes.challenge import bp as challenge_bp
except Exception:
    challenge_bp = None
try:
    from web.routes.glossary import bp as glossary_bp
except Exception:
    glossary_bp = None

app.register_blueprint(analysis_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(report_bp)
app.register_blueprint(table_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(admin_bp)

# Register challenge blueprint only if enabled in config
CHALLENGE_ENABLED = config.getboolean('CHALLENGE', 'ENABLED', fallback=False)
if challenge_bp and CHALLENGE_ENABLED:
    app.register_blueprint(challenge_bp)
    print(f"[CONFIG] Challenge module ENABLED")
else:
    print(f"[CONFIG] Challenge module DISABLED")

if glossary_bp:
    app.register_blueprint(glossary_bp)


# ==================================
#  HEALTHCHECK 
# ==================================
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    logger.info("[/HEALTHCHECK] Request to healthcheck from {request.remote_addr} with method {request.method}")
    return jsonify({"status": "ok"})




# ==================================
#  ENDPOINTS 
# ==================================
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    logger.debug(f"[/HOME] Language: {get_locale()}")
    logger.info("[/HOME] Rendering home template...")
    return render_template('index.html')



@app.route('/test', methods=['GET'])
@login_required
def test():
    logger.info("[/TEST] Rendering test template...")
    return render_template('test.html')


@app.route('/set_language', methods=['POST'])
def set_language():
    logger.info(f"[/SET_LANGUAGE] Request to set preferred language from {request.remote_addr} with method {request.method}")

    data = request.get_json()
    language = data.get('language')

    if language in ['es', 'en', 'it']:  # Idiomas soportados
        session['language'] = language  # Actualizar idioma en la sesión
        logger.info(f"[/SET_LANGUAGE] Language updated in session: {language}")
        return jsonify(success=True)
    else:
        print("Idioma no válido.")
        return jsonify(success=False), 400


# Manejadores de error personalizados
@app.errorhandler(502)
def error_mala_conexion_api(error):
    return f"<h1>502 Bad Gateway</h1><p>{error.description}</p>", 502

@app.errorhandler(404)
def error_no_encontrado(error):
    return f"<h1>404 Not Found</h1><p>{error.description}</p>", 404

@app.errorhandler(500)
def error_server_interno(error):
    return f"<h1>500 Internal Server Error</h1><p>{error.description}</p>", 500


# ==================================
#  ENDPOINTS REGISTRADOS
# ==================================
print("\n=== Rutas registradas ===")
for rule in app.url_map.iter_rules():
    methods = ",".join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
    print(f"{rule.endpoint:30s}  {methods:15s}  {rule}")
print("=========================\n")


# ==================================
# RUN 
# ==================================

# Usa SECRET_KEY para Flask-WTF, sesiones, etc.
# app.config['SECRET_KEY'] = config['JWT']['SECRET_KEY']  # o config['WEB']['SECRET_KEY']

app.run(debug=True, host=WEB_HOST, port=WEB_PORT)
