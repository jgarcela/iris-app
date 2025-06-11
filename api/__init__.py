# api/__init__.py

# ==================================
#  LIBRARIES 
# ==================================
import configparser
import ast
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# importamos tu conexión a MongoDB
from database.db import db

# ==================================
#  CONFIG 
# ==================================
config = configparser.ConfigParser()
config.read('config.ini')

WEB_HOST = config['WEB']['HOST']
WEB_PORT = config['WEB']['PORT']
DEBUG = config['WEB'].getboolean('DEBUG')
API_HOST = config['API']['HOST']
API_PORT = config['API']['PORT']

COLLECTION_DATA = config['DATABASE']['COLLECTION_DATA']
COLLECTION_USERS = config['DATABASE']['COLLECTION_USERS']
CONTEXTO_DATA  = config['DATABASE']['CONTEXTO_DATA']

GENERO_NOMBRE_PROPIO_TITULAR  = ast.literal_eval(config['CONTENIDO_GENERAL']['GENERO_NOMBRE_PROPIO_TITULAR'])
CITA_TITULAR                 = ast.literal_eval(config['CONTENIDO_GENERAL']['CITA_TITULAR'])
TEMA                         = ast.literal_eval(config['CONTENIDO_GENERAL']['TEMA'])
MENCIONA_IA                  = ast.literal_eval(config['CONTENIDO_GENERAL']['MENCIONA_IA'])
IA_TEMA_CENTRAL              = ast.literal_eval(config['CONTENIDO_GENERAL']['IA_TEMA_CENTRAL'])
SIGNIFICADO_IA               = ast.literal_eval(config['CONTENIDO_GENERAL']['SIGNIFICADO_IA'])
GENERO_PERSONAS_MENCIONADAS  = ast.literal_eval(config['CONTENIDO_GENERAL']['GENERO_PERSONAS_MENCIONADAS'])
EXTENSION_NOTICIA            = ast.literal_eval(config['CONTENIDO_GENERAL']['EXTENSION_NOTICIA'])
GENERO_PERIODISTA            = ast.literal_eval(config['CONTENIDO_GENERAL']['GENERO_PERIODISTA'])


# ==================================
#  APP 
# ==================================
app = Flask(__name__, 
            template_folder='templates', 
            static_folder='static')

# Configuración básica de Flask
app.config.update({
    'JWT_SECRET_KEY': config['JWT']['SECRET_KEY'],     # Define en config.ini
    'JWT_ACCESS_TOKEN_EXPIRES': int(config['JWT']['ACCESS_EXPIRES']),
    'JWT_REFRESH_TOKEN_EXPIRES': int(config['JWT']['REFRESH_EXPIRES']),
})

# Habilitar CORS para todas las rutas
CORS(app, 
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])

app.config['CORS_HEADERS'] = 'Content-Type'

# Mapeo de idiomas
language_map = {
    "es": "español",
    "en": "inglés",
}

# ==================================
#  EXTENSIONES 
# ==================================
jwt   = JWTManager(app)

# ==================================
#  BLUEPRINTS 
# ==================================
from api.routes.auth import bp as auth_bp
from api.routes.data import bp as data_bp
from api.routes.dashboard import bp as dashboard_bp
from api.routes.analysis import bp as analysis_bp


app.register_blueprint(auth_bp)
app.register_blueprint(data_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(analysis_bp)




# ==================================
#  HEALTHCHECK 
# ==================================
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok"})


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
app.config['SECRET_KEY'] = config['JWT']['SECRET_KEY']  # o config['WEB']['SECRET_KEY']

app.run(debug=True, host=API_HOST, port=API_PORT)