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
    from datetime import datetime, timezone
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
        'source': 'regular',
        'created_at': datetime.now(timezone.utc),
        'updated_at': datetime.now(timezone.utc)
    }

    # Guardar en MongoDB
    try:
        result = db.DB_ANALYSIS.insert_one(document)
        print(f"[DB] Documento insertado con ID: {result.inserted_id}")
        document['_id'] = str(result.inserted_id)  # para devolverlo como string
    except Exception as e:
        print(f"Error al guardar en MongoDB: {e}")

    # Convertir timestamps a string
    document['created_at'] = document['created_at'].isoformat()
    document['updated_at'] = document['updated_at'].isoformat()
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


@bp.route('/save_annotations', methods=['POST'])
# @role_required('user','admin')
def save_annotations():
    """Save analysis and manual annotations to database"""
    try:
        data = request.get_json()
        doc_id = data.get('doc_id')
        analysis = data.get('analysis')
        annotations = data.get('annotations', [])
        highlight_html = data.get('highlight_html', {})
        timestamp = data.get('timestamp')
        
        print(f"[SAVE_ANNOTATIONS] Received data:")
        print(f"  - doc_id: {doc_id}")
        print(f"  - annotations count: {len(annotations)}")
        print(f"  - highlight_html keys: {list(highlight_html.keys())}")
        print(f"  - timestamp: {timestamp}")
        
        if not doc_id:
            return jsonify(success=False, error='Document ID is required'), 400
        
        # Prepare update data
        update_data = {
            'analysis.original': analysis,
            'annotations': annotations,
            'highlight.edited': highlight_html,
            'updated_at': datetime.now(timezone.utc)
        }
        
        # If it's a new document (no existing doc_id), create it
        if doc_id == 'new' or not ObjectId.is_valid(doc_id):
            # Create new document
            new_doc = {
                'analysis': {
                    'original': analysis,
                    'edited': None
                },
                'annotations': annotations,
                'highlight': {
                    'original': {},
                    'edited': highlight_html
                },
                'created_at': datetime.now(timezone.utc),
                'updated_at': datetime.now(timezone.utc),
                'status': 'draft'
            }
            
            print(f"[SAVE_ANNOTATIONS] Creating new document with {len(annotations)} annotations")
            result = db.DB_ANALYSIS.insert_one(new_doc)
            new_doc_id = str(result.inserted_id)
            
            print(f"[DB] ✅ New document created with ID: {new_doc_id}")
            print(f"[DB] Document contains {len(annotations)} annotations")
            return jsonify(success=True, doc_id=new_doc_id)
        
        else:
            # Update existing document
            print(f"[SAVE_ANNOTATIONS] Updating existing document {doc_id} with {len(annotations)} annotations")
            result = db.DB_ANALYSIS.update_one(
                {'_id': ObjectId(doc_id)},
                {'$set': update_data}
            )
            
            if result.modified_count == 1:
                print(f"[DB] ✅ Document updated with ID: {doc_id}")
                print(f"[DB] Document now contains {len(annotations)} annotations")
                return jsonify(success=True, doc_id=doc_id)
            else:
                print(f"[DB] ❌ Failed to update document {doc_id}")
                return jsonify(success=False, error='No se pudo actualizar el documento')
                
    except Exception as e:
        print(f"[ERROR] Error saving annotations: {str(e)}")
        return jsonify(success=False, error=f'Error interno: {str(e)}'), 500

