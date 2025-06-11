from flask import Flask, request, render_template, jsonify, session
import configparser
from flask_cors import CORS
from flask_babel import Babel
from flask_babel import gettext as _
import requests
import ast
from web.analysis import bp as analysis_bp
from web.dashboard import bp as dashboard_bp
from web.report import bp as report_bp
from web.table import bp as table_bp
from web.logger import logger


# ----------------- CONFIG -----------------
config = configparser.ConfigParser()
config.read('config.ini')

WEB_HOST = config['WEB']['HOST']
WEB_PORT = config['WEB']['PORT']
DEBUG = config['WEB'].getboolean('DEBUG')
API_HOST = config['API']['HOST']
API_PORT = config['API']['PORT']
API_HEADERS_str = config['API']['HEADERS']
API_HEADERS = ast.literal_eval(API_HEADERS_str)
ENDPOINT_ANALYSIS = config['API']['ENDPOINT_ANALYSIS']
ENDPOINT_ANALYSIS_ANALYZE = config['API']['ENDPOINT_ANALYSIS_ANALYZE']

# ----------------- ENDPOINTS -----------------
URL_API_ENDPOINT_ANALYSIS_ANALYZE = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_ANALYSIS}/{ENDPOINT_ANALYSIS_ANALYZE}"


# ----------------- APP -----------------
app = Flask(__name__)
app.config['SECRET_KEY'] = config['DEFAULT']['SECRET_KEY']
app.secret_key = config['DEFAULT']['SECRET_KEY']


# ----------------- BLUEPRINTS ------------------
app.register_blueprint(analysis_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(report_bp)
app.register_blueprint(table_bp)
# app.register_blueprint(bp_users)


# Habilitar CORS para todas las rutas
CORS(app)

# Configuración de idiomas disponibles
app.config['BABEL_TRANSLATION_DIRECTORIES'] = './translations'
app.config['BABEL_DEFAULT_LOCALE'] = 'es'  # Idioma por defecto
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'


# Inicializar Babel con selector de idioma
def get_locale():
    lang = session.get('language', app.config['BABEL_DEFAULT_LOCALE'])
    logger.info(f"Language detected: {lang}")
    return lang

babel = Babel(app, locale_selector=get_locale)

@app.context_processor
def inject_language():
    return {'current_language': session.get('language', app.config['BABEL_DEFAULT_LOCALE'])}



# ----------------- ENDPOINTS -----------------
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    logger.info("[/HEALTHCHECK] Request to healthcheck from {request.remote_addr} with method {request.method}")
    return jsonify({"status": "ok"})

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

# Rutas
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    logger.debug(f"[/HOME] Language: {get_locale()}")
    logger.info("[/HOME] Rendering home template...")
    return render_template('index.html')

@app.route('/contacto', methods=['GET'])
def contacto():
    logger.info("[/CONTACTO] Rendering contacto template...")
    return render_template('contacto.html')

@app.route('/v0', methods=['GET'])
def home_v0():
    logger.debug(f"[/V0] Language: {get_locale()}")
    logger.info("[/V0] Rendering home v0 template...")
    return render_template('index_v0.html')

@app.route('/test', methods=['GET'])
def test():
    logger.info("[/TEST] Rendering test template...")
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True, host=WEB_HOST, port=WEB_PORT)