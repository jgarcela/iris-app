# api/routes/analysis.py

# ==================================
#  LIBRARIES 
# ==================================
from flask import Blueprint, abort, request, jsonify
from datetime import datetime, timezone
from newspaper import Article
from bson import ObjectId

import database.db as db
from api.utils.logger import logger

import api
import api.utils.analysis
import api.utils.highlight

# from api.utils.decorators import role_required, permission_required

# ==================================
#  BLUEPRINT 
# ==================================
bp = Blueprint('analysis', __name__, url_prefix='/analysis')


# ==================================
#  ENDPOINTS 
# ==================================
@bp.route('/analyze', methods=['POST'])
# @role_required('user','admin')
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
        analysis_contenido_general = api.utils.analysis.analyze_text(model, text, title, task="contenido_general")
        analysis_fuentes = api.utils.analysis.analyze_text(model, text, title, task="fuentes")
        analysis_lenguaje = api.utils.analysis.analyze_text(model, text, title, task="lenguaje")

        print("[/ANALYSIS/ANALYZE] Initializing highlight...")
        highlight_contenido_general = api.utils.highlight.highlight_text(analysis_contenido_general, text, task="contenido_general")
        highlight_fuentes = api.utils.highlight.highlight_text(analysis_fuentes, text, task="fuentes")
        highlight_lenguaje = api.utils.highlight.highlight_text(analysis_lenguaje, text, task="lenguaje")

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logger.exception("Error en el análisis")
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
        result = db.DB_ANALYSIS.insert_one(document)
        print(f"[DB] Documento insertado con ID: {result.inserted_id}")
        document['_id'] = str(result.inserted_id)  # para devolverlo como string
    except Exception as e:
        print(f"Error al guardar en MongoDB: {e}")

    # Convertir timestamp a string
    document['timestamp'] = document['timestamp'].isoformat()
    document['status'] = 'ok'

    return jsonify(document), 200


@bp.route('/save_edits', methods=['POST'])
# @role_required('user','admin')
def save_edits():
    data = request.get_json()
    doc_id = data['doc_id']
    section = data['section']
    html = data['edited_highlight_html']

    # Buscar y actualizar el documento
    result = db.DB_ANALYSIS.update_one(
        {'_id': ObjectId(doc_id)},
        {'$set': {f'highlight.edited.{section}': html}}
    )

    if result.modified_count == 1:
        print(f"[DB] Documento actualizado con ID: {doc_id}")
        return jsonify(success=True)
    else:
        return jsonify(success=False, error='No se pudo actualizar el documento')

