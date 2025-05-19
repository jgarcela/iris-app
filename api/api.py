import json
from flask import Flask, render_template, request, jsonify
import configparser
import utils

from flask_cors import CORS, cross_origin


# ----------------- CONFIG -----------------
config = configparser.ConfigParser()
config.read('config.ini')

WEB_HOST = config['WEB']['HOST']
WEB_PORT = config['WEB']['PORT']
DEBUG = config['WEB'].getboolean('DEBUG')
API_HOST = config['API']['HOST']
API_PORT = config['API']['PORT']


app = Flask(__name__)
# Habilitar CORS para todas las rutas
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

language_map = {
            "es": "español",
            "en": "inglés",
        }

# ----------------- ENDPOINTS -----------------
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok"})

@app.route('/analysis/analyze', methods=['POST'])
def analysis_analyze():
    # Obtener y validar JSON
    print(request)
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Payload inválido. Debe ser JSON.'}), 400

    model = data.get('model')
    text  = data.get('text')

    if not model or not text:
        return jsonify({
            'error': 'Faltan campos obligatorios. Se requieren "model" y "text".'
        }), 400

    # Ejecutar el análisis
    try:
        resultado_contenido_general = utils.analyze_contenido_general(model, text)
    except ValueError as ve:
        # por si analyze_text lanza errores de validación de parámetros
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        # error inesperado
        app.logger.exception("Error en el análisis")
        return jsonify({'error': 'Error interno en el servidor.'}), 500

    # Devolver resultado estructurado
    return jsonify({
        'status': 'ok',
        'model': model,
        'resultado_contenido_general': resultado_contenido_general
    }), 200   


if __name__ == '__main__':
    app.run(debug=True, host=API_HOST, port=API_PORT)

    app.config['SECRET_KEY'] = config['DEFAULT']['SECRET_KEY']