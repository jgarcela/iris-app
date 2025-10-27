# web/routes/challenge.py
from flask import Blueprint, render_template, request, jsonify, url_for, redirect
from flask_babel import get_locale, _
from web.utils.challenge_decorators import challenge_required
from database.db import DB_SEMANA_CIENCIA
from datetime import datetime, timezone
import configparser
import ast
import requests

bp = Blueprint('challenge', __name__, url_prefix='/challenge')

# ----------------- CONFIG -----------------
config = configparser.ConfigParser()
config.read('config.ini')

API_HOST = config['API']['HOST']
API_PORT = config['API']['PORT']
API_HEADERS_str = config['API']['HEADERS']
API_HEADERS = ast.literal_eval(API_HEADERS_str)

ENDPOINT_ANALYSIS = config['API']['ENDPOINT_ANALYSIS'] if 'ENDPOINT_ANALYSIS' in config['API'] else 'analysis'
URL_API_ENDPOINT_ANALYSIS_ANALYZE = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_ANALYSIS}/analyze"

def get_challenge_texts():
    """Fetch challenge texts from MongoDB database with all attributes"""
    try:
        # Debug: Check what collections exist
        print(f"Database name: {DB_SEMANA_CIENCIA.database.name}")
        print(f"Collection name: {DB_SEMANA_CIENCIA.name}")
        
        # Debug: Check total count
        total_count = DB_SEMANA_CIENCIA.count_documents({})
        
        # Debug: Check if there are documents with 'id' field
        id_count = DB_SEMANA_CIENCIA.count_documents({"id": {"$exists": True}})
        
        # Get only documents with 'id' field (actual challenge texts, not init documents)
        texts_cursor = DB_SEMANA_CIENCIA.find({"id": {"$exists": True}}).sort('id', 1)  # Sort by id ascending
        
        texts = list(texts_cursor)
        
        # Convert ObjectId to string for JSON serialization
        for text in texts:
            if '_id' in text:
                text['_id'] = str(text['_id'])
        
        # If no texts found in database, return empty list
        if not texts:
            return []
            
        return texts
        
    except Exception as e:
        print(f"Error fetching challenge texts from database: {e}")
        return []




@bp.route('/')
@challenge_required
def challenge_home():
    """Página principal del desafío"""
    texts = get_challenge_texts()
    return render_template('challenge/challenge_home.html', 
                         texts=texts,
                         language=get_locale())

@bp.route('/analyze/<text_id>')
@challenge_required
def analyze_text(text_id):
    """Página de análisis individual"""
    try:
        # Try to find text by _id (ObjectId string) first
        from bson import ObjectId
        text_doc = DB_SEMANA_CIENCIA.find_one({'_id': ObjectId(text_id)})
        
        if text_doc:
            # Convert ObjectId to string for JSON serialization
            text_doc['_id'] = str(text_doc['_id'])
            # Also convert any other ObjectId fields that might exist
            for key, value in text_doc.items():
                if hasattr(value, '__class__') and value.__class__.__name__ == 'ObjectId':
                    text_doc[key] = str(value)
            return render_template('challenge/challenge_analysis.html', 
                                 text_data=text_doc,
                                 language=get_locale())
        
        # Fallback: try to find by integer id
        try:
            int_id = int(text_id)
            texts = get_challenge_texts()
            text_data = next((text for text in texts if text.get('id') == int_id), None)
            if text_data:
                return render_template('challenge/challenge_analysis.html', 
                                     text_data=text_data,
                                     language=get_locale())
        except ValueError:
            pass
            
        return "Texto no encontrado", 404
        
    except Exception as e:
        print(f"Error in analyze_text: {e}")
        return f"Error: {str(e)}", 500




# ----------------- NEW: AI analysis and comparison flow -----------------
@bp.route('/test-ai', methods=['GET'])
@challenge_required
def test_ai():
    """Test route to verify the endpoint is working"""
    return jsonify(success=True, message="Test route working")

@bp.route('/analyze-ai', methods=['POST'])
@challenge_required
def analyze_ai():
    """Store manual annotations and redirect to comparison with existing AI analysis."""
    try:
        print(f"[CHALLENGE/ANALYZE-AI] Received request from {request.remote_addr}")
        
        payload = request.get_json(force=True)
        print(f"[CHALLENGE/ANALYZE-AI] Payload: {payload}")
        
        text_id = payload.get('text_id')
        manual_annotations = payload.get('manual_annotations', [])
        
        # If text_id is None, try to get it from text_data
        if not text_id:
            text_data_payload = payload.get('text_data', {})
            text_id = text_data_payload.get('_id')
            print(f"[CHALLENGE/ANALYZE-AI] Got text_id from text_data: {text_id}")
        
        if not text_id:
            return jsonify(success=False, error="text_id is required"), 400
        
        print(f"[CHALLENGE/ANALYZE-AI] Processing text_id: {text_id}, annotations: {len(manual_annotations)}")
        
        # Get current user info
        from web.utils.challenge_decorators import get_current_user
        current_user = get_current_user()
        user_id = current_user.get('id') if current_user else None
        username = current_user.get('username') if current_user else None
        
        print(f"[CHALLENGE/ANALYZE-AI] User: {username} (ID: {user_id})")
        
        # Import DB_ANALYSIS_SEMANA_CIENCIA
        from database.db import DB_ANALYSIS_SEMANA_CIENCIA
        
        # Get original text data
        from bson import ObjectId
        try:
            text_data = DB_SEMANA_CIENCIA.find_one({'_id': ObjectId(text_id)})
        except:
            text_data = None
        
        if not text_data:
            # Try with integer id
            try:
                int_id = int(text_id)
                text_data = DB_SEMANA_CIENCIA.find_one({'id': int_id})
            except (ValueError, TypeError):
                pass
        
        if not text_data:
            return jsonify(success=False, error="Text not found"), 404
        
        # Create a new analysis document (copies original text + adds user analysis)
        analysis_document = {
            'text_id': text_id,
            'text_data': {
                'title': text_data.get('title'),
                'text': text_data.get('text'),
                'difficulty': text_data.get('difficulty'),
                'url': text_data.get('url'),
                'authors': text_data.get('authors'),
                'date': text_data.get('date')
            },
            'manual_annotations': manual_annotations,
            'user_id': user_id,
            'username': username,
            'created_at': datetime.now(timezone.utc)
        }
        
        # Insert into challenge analyses collection
        result = DB_ANALYSIS_SEMANA_CIENCIA.insert_one(analysis_document)
        print(f"[CHALLENGE/ANALYZE-AI] New analysis created with ID: {result.inserted_id}")

        # Redirect to comparison page
        redirect_url = url_for('challenge.iris_results', text_id=text_id)
        print(f"[CHALLENGE/ANALYZE-AI] Redirect URL: {redirect_url}")
        
        return jsonify(success=True, redirect_url=redirect_url)

    except Exception as e:
        print(f"[CHALLENGE/ANALYZE-AI] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify(success=False, error=str(e)), 500


@bp.route('/iris-results/<text_id>', methods=['GET'])
@challenge_required
def iris_results(text_id):
    """Render comparison page: manual vs AI analysis for a given text."""
    try:
        print(f"[CHALLENGE/IRIS-RESULTS] Fetching text_id: {text_id}")
        
        # Try to find by _id (ObjectId) first
        from bson import ObjectId
        text_doc = DB_SEMANA_CIENCIA.find_one({'_id': ObjectId(text_id)})
        
        if not text_doc:
            # Fallback: try to find by integer id
            try:
                int_id = int(text_id)
                text_doc = DB_SEMANA_CIENCIA.find_one({'id': int_id})
            except ValueError:
                pass
                
        if not text_doc:
            print(f"[CHALLENGE/IRIS-RESULTS] Text not found for id: {text_id}")
            return "Texto no encontrado", 404
        
        # Convert ObjectId to string for JSON serialization
        text_doc['_id'] = str(text_doc['_id'])
        # Also convert any other ObjectId fields that might exist
        for key, value in text_doc.items():
            if hasattr(value, '__class__') and value.__class__.__name__ == 'ObjectId':
                text_doc[key] = str(value)
            
        print(f"[CHALLENGE/IRIS-RESULTS] Found text: {text_doc.get('title', 'No title')}")
    except Exception as e:
        print(f"[CHALLENGE/IRIS-RESULTS] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}", 500

    # Get analysis data if it exists (not used for comparison anymore)
    analysis_data = text_doc.get('analysis', {}) or {}
    main_iris_analysis = {}
    
    # Get manual annotations from challenge analyses collection (user-specific)
    from database.db import DB_ANALYSIS_SEMANA_CIENCIA
    from web.utils.challenge_decorators import get_current_user
    current_user = get_current_user()
    user_id = current_user.get('id') if current_user else None
    
    # Find the user's analysis for this text - user must have their own analysis
    # Get the most recent analysis if there are multiple
    manual_annotations = []
    if user_id:
        user_analysis = DB_ANALYSIS_SEMANA_CIENCIA.find_one(
            {
                'text_id': text_id,
                'user_id': user_id
            },
            sort=[('created_at', -1)]  # Sort by created_at descending to get the most recent
        )
        if user_analysis:
            manual_annotations = user_analysis.get('manual_annotations', [])
            print(f"[CHALLENGE/IRIS-RESULTS] Found most recent user analysis with {len(manual_annotations)} annotations")
        else:
            # User hasn't analyzed this text yet - redirect to analysis page
            print(f"[CHALLENGE/IRIS-RESULTS] No analysis found for user_id={user_id}, redirecting to analyze page")
            from flask import flash
            flash(_('Debes completar el análisis de este texto antes de ver los resultados'), 'info')
            return redirect(url_for('challenge.analyze_text', text_id=text_id))
    else:
        # No user logged in
        print(f"[CHALLENGE/IRIS-RESULTS] No user logged in")
        from flask import flash
        flash(_('Debes iniciar sesión para ver los resultados'), 'warning')
        return redirect(url_for('challenge.challenge_home'))

    print(f"[CHALLENGE/IRIS-RESULTS] Manual analysis: {manual_annotations}")

    # Get the original annotations from text_doc (ground truth manual annotations)
    original_annotations = text_doc.get('annotations', [])
    print(f"[CHALLENGE/IRIS-RESULTS] Original annotations count: {len(original_annotations)}")

    print(analysis_data)

    # Minimal structure for template consumption
    text_data = {
        'id': text_doc.get('id'),
        'title': text_doc.get('title'),
        'text': text_doc.get('text'),
        'difficulty': text_doc.get('difficulty'),
        'difficulty_reason': text_doc.get('difficulty_reason'),
        'categories': text_doc.get('categories', [])
    }
    
    # Get the next text id using the defined sequence order
    current_object_id = text_doc.get('_id')  # Already converted to string
    next_text = None
    
    print(f"[CHALLENGE/IRIS-RESULTS] Current text _id: {current_object_id}")
    
    # Define the same order as in the frontend
    ordered_ids = [
        '68f9e5a22e476535f8a73ec4', # Paloma Lago
        '68f9e5a22e476535f8a73ec2', # Paula Badosa
        '68f9e5a22e476535f8a73ec3', # Ariarne Titmus
        '68f9e5a22e476535f8a73ec1', # Begoña Aramendía
        '68f9e5a22e476535f8a73ec6', # Michelle Jenner
        '68f9e5a22e476535f8a73ec5'  # Álvaro Bilbao
    ]
    
    try:
        # Find current index in sequence
        current_index = ordered_ids.index(current_object_id)
        
        # Check each remaining text in order to find the first incomplete one
        for i in range(current_index + 1, len(ordered_ids)):
            text_id_to_check = ordered_ids[i]
            # Check if user has completed this text
            existing_analysis = DB_ANALYSIS_SEMANA_CIENCIA.find_one(
                {
                    'text_id': text_id_to_check,
                    'user_id': user_id
                },
                sort=[('created_at', -1)]
            )
            
            # If no analysis exists for this text, this is our next text
            if not existing_analysis:
                next_text = text_id_to_check
                print(f"[CHALLENGE/IRIS-RESULTS] Found next incomplete text at index {i}: {next_text}")
                break
        
        # If all remaining texts are complete, check if current is last
        if next_text is None:
            if current_index + 1 >= len(ordered_ids):
                print(f"[CHALLENGE/IRIS-RESULTS] Last text in sequence")
            else:
                print(f"[CHALLENGE/IRIS-RESULTS] All remaining texts are complete")
    except ValueError:
        print(f"[CHALLENGE/IRIS-RESULTS] Current text not in sequence")
    except Exception as e:
        print(f"[CHALLENGE/IRIS-RESULTS] Error getting next text: {e}")

    return render_template(
        'challenge/challenge_iris_results.html',
        text_data=text_data,
        manual_annotations=manual_annotations,
        original_annotations=original_annotations,  # Ground truth annotations
        next_text_id=next_text,  # Next text ID or None
        language=get_locale()
    )

