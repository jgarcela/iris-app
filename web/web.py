from flask import Flask, request, render_template, jsonify, session
import configparser
from flask_cors import CORS
from flask_babel import Babel
from flask_babel import gettext as _
import requests
import ast
from analysis import bp as analysis_bp
from report import bp as report_bp


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
app.register_blueprint(report_bp)
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
    print(f"Idioma detectado desde la sesión: {lang}")  # Depuración
    return lang

babel = Babel(app, locale_selector=get_locale)

@app.context_processor
def inject_language():
    return {'current_language': session.get('language', app.config['BABEL_DEFAULT_LOCALE'])}



# ----------------- ENDPOINTS -----------------
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok"})

@app.route('/set_language', methods=['POST'])
def set_language():
    data = request.get_json()
    language = data.get('language')

    if language in ['es', 'en', 'it']:  # Idiomas soportados
        session['language'] = language  # Actualizar idioma en la sesión
        print(f"Idioma actualizado en la sesión: {language}")  # Depuración
        return jsonify(success=True)
    else:
        print("Idioma no válido.")
        return jsonify(success=False), 400


@app.route('/', methods=['GET'])
def home():
    print(f"Idioma actual: {get_locale()}")
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True, host=WEB_HOST, port=WEB_PORT)