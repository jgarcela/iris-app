# web/routes/challenge.py
from flask import Blueprint, render_template, request, jsonify, url_for
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
        redirect_url = url_for('challenge.ai_results', text_id=text_id)
        print(f"[CHALLENGE/ANALYZE-AI] Redirect URL: {redirect_url}")
        
        return jsonify(success=True, redirect_url=redirect_url)

    except Exception as e:
        print(f"[CHALLENGE/ANALYZE-AI] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify(success=False, error=str(e)), 500


@bp.route('/ai-results/<text_id>', methods=['GET'])
@challenge_required
def ai_results(text_id):
    """Render comparison page: manual vs AI analysis for a given text."""
    try:
        print(f"[CHALLENGE/AI-RESULTS] Fetching text_id: {text_id}")
        
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
            print(f"[CHALLENGE/AI-RESULTS] Text not found for id: {text_id}")
            return "Texto no encontrado", 404
        
        # Convert ObjectId to string for JSON serialization
        text_doc['_id'] = str(text_doc['_id'])
        # Also convert any other ObjectId fields that might exist
        for key, value in text_doc.items():
            if hasattr(value, '__class__') and value.__class__.__name__ == 'ObjectId':
                text_doc[key] = str(value)
            
        print(f"[CHALLENGE/AI-RESULTS] Found text: {text_doc.get('title', 'No title')}")
    except Exception as e:
        print(f"[CHALLENGE/AI-RESULTS] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}", 500

    # Map difficulty to key to pick AI analysis
    difficulty_label = text_doc.get('difficulty', '').strip()
    difficulty_map = {
        'Fácil': 'easy',
        'Medio': 'medium',
        'Difícil': 'hard'
    }
    difficulty_key = difficulty_map.get(difficulty_label, 'medium')

    # Get all AI analyses from the existing analysis structure
    # The AI analysis is stored in analysis.easy/medium/hard depending on difficulty
    analysis_data = text_doc.get('analysis', {})
    ai_analysis_easy = analysis_data.get('easy', {})
    ai_analysis_medium = analysis_data.get('medium', {})
    ai_analysis_hard = analysis_data.get('hard', {})

    print(f"[CHALLENGE/AI-RESULTS] AI analysis: {ai_analysis_easy}, {ai_analysis_medium}, {ai_analysis_hard}")
    
    # Get the main comparison analysis (matches text difficulty)
    main_ai_analysis = analysis_data.get(difficulty_key, {})
    
    # Get manual annotations from challenge analyses collection (user-specific)
    from database.db import DB_ANALYSIS_SEMANA_CIENCIA
    from web.utils.challenge_decorators import get_current_user
    current_user = get_current_user()
    user_id = current_user.get('id') if current_user else None
    
    # Find the user's analysis for this text
    manual_annotations = []
    if user_id:
        user_analysis = DB_ANALYSIS_SEMANA_CIENCIA.find_one({
            'text_id': text_id,
            'user_id': user_id
        })
        if user_analysis:
            manual_annotations = user_analysis.get('manual_annotations', [])
            print(f"[CHALLENGE/AI-RESULTS] Found user analysis with {len(manual_annotations)} annotations")
    
    # Fallback: try to get from original document if no user analysis found (for backwards compatibility)
    if not manual_annotations:
        manual_annotations = text_doc.get('manual_annotations', [])

    print(f"[CHALLENGE/AI-RESULTS] Manual analysis: {manual_annotations}")

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

    return render_template(
        'challenge/challenge_ai_results.html',
        text_data=text_data,
        main_ai_analysis=main_ai_analysis,
        # Back-compat for current template variables
        analysis_data=analysis_data,
        ai_analysis=main_ai_analysis,
        ai_analysis_easy=ai_analysis_easy,
        ai_analysis_medium=ai_analysis_medium,
        ai_analysis_hard=ai_analysis_hard,
        current_difficulty=difficulty_key,
        manual_annotations=manual_annotations,
        language=get_locale()
    )

