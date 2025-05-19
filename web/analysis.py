# web/analysis.py
import re
from flask import Blueprint, render_template, request, jsonify, session
import requests
from flask_babel import get_locale
import configparser
import ast

# ----------------- BLUEPRINT -----------------
bp = Blueprint(
    'analysis',               # nombre interno del blueprint
    __name__,                 # paquete actual
    url_prefix='/analysis'    # prefijo para todas las rutas
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

# Mapeo de categorías a clases de color
CATEGORY_COLOR_MAP = {
    'nombre_propio_titular': 'color-1',
    'cita_textual_titular': 'color-2',
    'personas_mencionadas': 'color-3',
}


#  ----------------- ENDPOINTS -----------------
@bp.route('/analyze', methods=['GET', 'POST'])
def analyze():
    # Leer datos enviados
    text = request.form.get('text', '')
    model = request.form.get('model', '')

    app = bp.get_app() if hasattr(bp, 'get_app') else None
    # debug
    print(f"Texto recibido: {text}")
    print(f"Modelo recibido: {model}")

    # Preparar JSON
    payload = {'text': text, 'model': model}

    # Llamada a la API
    resp = requests.post(URL_API_ENDPOINT_ANALYSIS_ANALYZE, json=payload, headers=API_HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        print(f"Respuesta de la API: {data}")

        original_text = text
        highlighted = original_text
        
        # Accedemos al dict anidado
        nested = data['resultado_contenido_general']

        # Para evitar parches anidados, procesamos primero las frases más largas
        all_phrases = []
        for campo, frases in nested.items():
            # solo campos que tengan mapeo de color
            if campo in CATEGORY_COLOR_MAP:
                all_phrases += [(campo, f) for f in frases]

        # Ordenar por longitud de frase (descendente)
        all_phrases.sort(key=lambda cf: len(cf[1]), reverse=True)

        # Reemplazar cada frase en el texto
        for campo, frase in all_phrases:
            css = CATEGORY_COLOR_MAP[campo]
            clases = f"{css}"
            # re.escape para no romper la regex; sin \b para capturar espacios/puntuación
            pattern = re.escape(frase)
            highlighted = re.sub(
                pattern,
                fr'<mark class="{clases}">{frase}</mark>',
                highlighted
            )






        return render_template(
            'analysis.html',
            text=text,
            model_name=model,
            language=get_locale(),
            data=data,
            text_highlighted=highlighted
        )
    else:
        return jsonify({"error": "Error en la solicitud al API"}), 500
