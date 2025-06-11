import json
from flask import Flask, render_template, request, jsonify, Response, stream_with_context, abort
from flask_cors import CORS, cross_origin
import configparser
from datetime import datetime, timezone
from newspaper import Article
from bson import ObjectId
from collections import Counter
import ast

import api.analyze
import api.highlight
import api.dashboard
from database.db import db 
from api.logger import logger


# ==============================
# =========== CONFIG ===========
# ==============================
config = configparser.ConfigParser()
config.read('config.ini')

WEB_HOST = config['WEB']['HOST']
WEB_PORT = config['WEB']['PORT']
DEBUG = config['WEB'].getboolean('DEBUG')
API_HOST = config['API']['HOST']
API_PORT = config['API']['PORT']

COLLECTION_DATA = config['DATABASE']['COLLECTION_DATA']
CONTEXTO_DATA = config['DATABASE']['CONTEXTO_DATA']

GENERO_NOMBRE_PROPIO_TITULAR = ast.literal_eval(config['CONTENIDO_GENERAL']['GENERO_NOMBRE_PROPIO_TITULAR'])
CITA_TITULAR = ast.literal_eval(config['CONTENIDO_GENERAL']['CITA_TITULAR'])
TEMA = ast.literal_eval(config['CONTENIDO_GENERAL']['TEMA'])
MENCIONA_IA = ast.literal_eval(config['CONTENIDO_GENERAL']['MENCIONA_IA'])
IA_TEMA_CENTRAL = ast.literal_eval(config['CONTENIDO_GENERAL']['IA_TEMA_CENTRAL'])
SIGNIFICADO_IA = ast.literal_eval(config['CONTENIDO_GENERAL']['SIGNIFICADO_IA'])
GENERO_PERSONAS_MENCIONADAS = ast.literal_eval(config['CONTENIDO_GENERAL']['GENERO_PERSONAS_MENCIONADAS'])
EXTENSION_NOTICIA = ast.literal_eval(config['CONTENIDO_GENERAL']['EXTENSION_NOTICIA'])
GENERO_PERIODISTA = ast.literal_eval(config['CONTENIDO_GENERAL']['GENERO_PERIODISTA'])


# ===========================
# =========== APP ===========
# ===========================
app = Flask(__name__)
# Habilitar CORS para todas las rutas
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

language_map = {
            "es": "español",
            "en": "inglés",
        }

# =================================
# =========== ENDPOINTS ===========
# =================================


# ===========
# HEALTHCHECK
# ===========
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok"})



# ===========
# DATA
# ===========
@app.route("/data/get_contexto", methods=["GET"])
def get_contexto():
    try:
        # 1. Seleccionamos la colección específica
        collection = db[COLLECTION_DATA]

        # 2. Devuelve una lista de strings con los valores únicos.
        contextos_unicos = collection.distinct(CONTEXTO_DATA)

    except Exception as e:
        # En caso de error, devolvemos un 500 con el mensaje
        return jsonify({"error": str(e)}), 500

    # 3. Devolvemos la lista de contextos únicos en formato JSON
    return jsonify({"contextos": contextos_unicos})


# Dado que Flask jsonify no sabe serializar ObjectId, definimos
# un pequeño helper que itera un documento y reemplaza el campo "_id".
def serialize_doc(doc: dict) -> dict:
    """
    Recibe un documento recibido de MongoDB (con ObjectId en '_id')
    y devuelve un dict con '_id' convertido a str, y el resto de campos tal cual.
    """
    salida = {}
    for clave, valor in doc.items():
        if isinstance(valor, ObjectId):
            salida[clave] = str(valor)
        else:
            salida[clave] = valor
    return salida

@app.route("/data/<collection_name>", methods=["GET"]) # Aquí añadimos el parámetro <collection_name>
def get_data_from_collection(collection_name): # El nombre de la colección se pasa como argumento
    """
    Este endpoint devuelve una lista con todos los documentos de la colección especificada por 'collection_name'.
    Cada documento se serializa convirtiendo el ObjectId a string.
    """
    try:
        # 3.1. Obtenemos la colección dinámicamente
        # Usamos db[collection_name] para seleccionar la colección
        cursor = db[collection_name].find({})
    except Exception as e:
        # Si ocurre un error en la consulta a Mongo, devolvemos un 500
        abort(500, description=f"Error al consultar la base de datos o colección '{collection_name}': {e}")

    # 3.2. Convertimos el cursor a lista, serializando cada doc
    lista_documentos = []
    for doc in cursor:
        lista_documentos.append(serialize_doc(doc))

    # 3.3. Devolvemos el JSON con la lista completa
    return jsonify(lista_documentos), 200


# ===========
# DASHBOARD
# ===========
@app.route("/dashboard/data", methods=["POST"])
def dashboard_data():
    """
    Espera un JSON con:
    {
        "data": [...],
        "total_count": N
    }
    """
    payload = request.get_json(silent=True)
    if not payload or 'data' not in payload or 'total_count' not in payload:
        abort(400, "Se requieren 'data' y 'total_count' en el cuerpo JSON")

    data = payload['data']
    total_count = payload['total_count'] or 1

    # 1) Nombre propio titular
    cnt = Counter(item.get('nombre_propio_titular') for item in data)
    labels_npt, values_npt = api.dashboard.prepare_chart(cnt, GENERO_NOMBRE_PROPIO_TITULAR)
    perc_npt = [round(v/total_count*100,1) for v in values_npt]

    # 2) Cita en el titular
    cnt = Counter(item.get('cita_titular') for item in data)
    labels_ct, values_ct = api.dashboard.prepare_chart(cnt, CITA_TITULAR)
    perc_ct = [round(v/total_count*100,1) for v in values_ct]

    # 3) Temática de las Noticias
    cnt = Counter(item.get('tema') for item in data)
    labels_tema, values_tema = api.dashboard.prepare_chart(cnt, TEMA)
    perc_tema = [round(v/total_count*100,1) for v in values_tema]

    # 4) Menciona IA
    cnt = Counter(item.get('menciona_ia') for item in data)
    labels_mia, values_mia = api.dashboard.prepare_chart(cnt, MENCIONA_IA)
    perc_mia = [round(v/total_count*100,1) for v in values_mia]

    # 5) IA Tema principal
    cnt = Counter(item.get('ia_tema_central') for item in data)
    labels_itc, values_itc = api.dashboard.prepare_chart(cnt, IA_TEMA_CENTRAL)
    perc_itc = [round(v/total_count*100,1) for v in values_itc]

    # 6) Explicación Significado IA
    cnt = Counter(item.get('significado_ia') for item in data)
    labels_sia, values_sia = api.dashboard.prepare_chart(cnt, SIGNIFICADO_IA)
    perc_sia = [round(v/total_count*100,1) for v in values_sia]

    # 7) Género de las personas
    cnt = Counter(item.get('genero_personas') for item in data)
    labels_gp, values_gp = api.dashboard.prepare_chart(cnt, GENERO_PERSONAS_MENCIONADAS)
    perc_gp = [round(v/total_count*100,1) for v in values_gp]

    # 8) Extensión de la noticia
    lengths = []
    for item in data:
        nc_raw = item.get('Caracteres')
        try:
            nc = int(nc_raw)
        except (TypeError, ValueError):
            texto = item.get('textonoticia') or ''
            nc = len(texto)
        lengths.append(nc)
    cnt_ext = Counter()
    thresholds = sorted(EXTENSION_NOTICIA.keys())
    for l in lengths:
        for thr in reversed(thresholds):
            if l >= thr:
                cnt_ext[thr] += 1
                break
    cnt_ext_str = Counter({ str(k): v for k,v in cnt_ext.items() })
    mapping_ext = { str(k): EXTENSION_NOTICIA[k] for k in thresholds }
    labels_en, values_en = api.dashboard.prepare_chart(cnt_ext_str, mapping_ext)
    perc_en = [round(v/total_count*100,1) for v in values_en]

    # 9) Género periodista
    cnt = Counter(item.get('genero_periodista') for item in data)
    labels_per, values_per = api.dashboard.prepare_chart(cnt, GENERO_PERIODISTA)
    perc_per = [round(v/total_count*100,1) for v in values_per]

    # Armamos y devolvemos JSON
    dashboard = {
        "total_count": total_count,
        "chart_data": {
            'nombreTitular':   {'type':'bar',      'labels':labels_npt, 'data':values_npt, 'percent':perc_npt, 'colors': api.dashboard.generate_colors(len(labels_npt))},
            'citaTitular':     {'type':'bar',      'labels':labels_ct,  'data':values_ct,  'percent':perc_ct,  'colors': api.dashboard.generate_colors(len(labels_ct))},
            'tematica':        {'type':'bar',      'labels':labels_tema,'data':values_tema,'percent':perc_tema,'colors': api.dashboard.generate_colors(len(labels_tema))},
            'mencionaIA':      {'type':'doughnut', 'labels':labels_mia, 'data':values_mia, 'percent':perc_mia, 'colors': api.dashboard.generate_colors(len(labels_mia))},
            'iaTemaPrincipal': {'type':'doughnut', 'labels':labels_itc, 'data':values_itc, 'percent':perc_itc, 'colors': api.dashboard.generate_colors(len(labels_itc))},
            'significadoIA':   {'type':'doughnut', 'labels':labels_sia, 'data':values_sia, 'percent':perc_sia, 'colors': api.dashboard.generate_colors(len(labels_sia))},
            'generoPersonas':  {'type':'doughnut', 'labels':labels_gp,  'data':values_gp,  'percent':perc_gp,  'colors': api.dashboard.generate_colors(len(labels_gp))},
            'extensionNoticia':{'type':'doughnut', 'labels':labels_en,  'data':values_en,  'percent':perc_en,  'colors': api.dashboard.generate_colors(len(labels_en))},
            'generoPeriodista':{'type':'bar',      'labels':labels_per, 'data':values_per,'percent':perc_per,  'colors': api.dashboard.generate_colors(len(labels_per))}
        }
    }

    return jsonify(dashboard)




# ANALYSIS
# ===========
@app.route('/analysis/analyze', methods=['POST'])
def analysis_analyze():
    print("[/ANALYSIS/ANALYZE] Receiving data from web...")
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Payload inválido. Debe ser JSON.'}), 400

    model = data['model']
    text  = data['text']
    title = data['title']
    authors = data['authors']
    url = data['url']

    if not model.strip():
        return jsonify({
            'error': 'El campo "model" no puede estar vacío.',
            'received': {
                'model': bool(model.strip()),
                'text': bool(text.strip()),
                'url': bool(url.strip())
            }
        }), 400

    if not text.strip() and not url.strip():
        return jsonify({
            'error': 'Se requiere al menos un campo no vacío: "text" o "url".',
            'received': {
                'model': bool(model.strip()),
                'text': bool(text.strip()),
                'url': bool(url.strip())
            }
        }), 400

    if url.strip():
        print(f"{url=}")
        try:
            article = Article(url)
            article.download()
            article.parse()
            text = article.text
            title = title or article.title
            authors = authors or article.authors
            print(f"{text=}")
        except Exception as e:
            return jsonify({'error': f'Error al procesar la URL: {str(e)}'}), 500

    try:
        print("[/ANALYSIS/ANALYZE] Initializing analysis...")
        analysis_contenido_general = api.analyze.analyze_text(model, text, title, task="contenido_general")
        analysis_fuentes = api.analyze.analyze_text(model, text, title, task="fuentes")
        analysis_lenguaje = api.analyze.analyze_text(model, text, title, task="lenguaje")

        print("[/ANALYSIS/ANALYZE] Initializing highlight...")
        highlight_contenido_general = api.highlight.highlight_text(analysis_contenido_general, text, task="contenido_general")
        highlight_fuentes = api.highlight.highlight_text(analysis_fuentes, text, task="fuentes")
        highlight_lenguaje = api.highlight.highlight_text(analysis_lenguaje, text, task="lenguaje")

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        app.logger.exception("Error en el análisis")
        return jsonify({'error': 'Error interno en el servidor.'}), 500

    # Estructura editable
    document = {
        'model': model,
        'text': text,
        'title': title,
        'authors': authors,
        'url': url,
        'analysis': {
            'original': {
                'contenido_general': analysis_contenido_general,
                'fuentes': analysis_fuentes,
                'lenguaje': analysis_lenguaje
            },
            'edited': {
                'contenido_general': None,
                'fuentes': None,
                'lenguaje': None
            }
        },
        'highlight': {
            'original': {
                'contenido_general': highlight_contenido_general,
                'fuentes': highlight_fuentes,
                'lenguaje': highlight_lenguaje
            },
            'edited': {
                'contenido_general': None,
                'fuentes': None,
                'lenguaje': None
            }
        },
        'timestamp': datetime.now(timezone.utc)
    }

    # Guardar en MongoDB
    try:
        result = db.iris_analysis.insert_one(document)
        print(f"[DB] Documento insertado con ID: {result.inserted_id}")
        document['_id'] = str(result.inserted_id)  # para devolverlo como string
    except Exception as e:
        print(f"Error al guardar en MongoDB: {e}")

    # Convertir timestamp a string
    document['timestamp'] = document['timestamp'].isoformat()
    document['status'] = 'ok'

    return jsonify(document), 200


@app.route('/analysis/save_edits', methods=['POST'])
def save_edits():
    data = request.get_json()
    doc_id = data['doc_id']
    section = data['section']
    html = data['edited_highlight_html']

    # Buscar y actualizar el documento
    result = db.iris_analysis.update_one(
        {'_id': ObjectId(doc_id)},
        {'$set': {f'highlight.edited.{section}': html}}
    )

    if result.modified_count == 1:
        print(f"[DB] Documento actualizado con ID: {doc_id}")
        return jsonify(success=True)
    else:
        return jsonify(success=False, error='No se pudo actualizar el documento')




if __name__ == '__main__':
    app.run(debug=True, host=API_HOST, port=API_PORT)

    app.config['SECRET_KEY'] = config['DEFAULT']['SECRET_KEY']