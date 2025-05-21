# web/analysis.py
import re
from flask import Blueprint, render_template, request, jsonify, session
import requests
from flask_babel import get_locale
import configparser
import ast

# ----------------- BLUEPRINT -----------------
bp = Blueprint(
    'analysis',
    __name__,
    url_prefix='/analysis'
)

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

# ----------------- URLs -----------------
URL_API_ENDPOINT_ANALYSIS_ANALYZE = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_ANALYSIS}/{ENDPOINT_ANALYSIS_ANALYZE}"

#  ----------------- ENDPOINTS -----------------
@bp.route('/analyze', methods=['GET', 'POST'])
def analyze():
    # Leer datos enviados
    text = request.form.get('text', '')
    model = request.form.get('model', '')

    app = bp.get_app() if hasattr(bp, 'get_app') else None

    # Preparar JSON
    payload = {'text': text, 'model': model}

    # Llamada a la API
    print(f"[/ANALYZE] Sending request to API ({URL_API_ENDPOINT_ANALYSIS_ANALYZE})...")
    resp = requests.post(URL_API_ENDPOINT_ANALYSIS_ANALYZE, json=payload, headers=API_HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        print(f"Respuesta de la API: {data}")

        return render_template(
            'analysis.html',
            text=text,
            model_name=model,
            language=get_locale(),
            data=data
        )
    else:
        return jsonify({"error": "Error en la solicitud al API"}), 500
