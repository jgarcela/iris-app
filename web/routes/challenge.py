# web/routes/challenge.py
from flask import Blueprint, render_template
from flask_babel import get_locale, _
from web.utils.challenge_decorators import challenge_required
from database.db import DB_SEMANA_CIENCIA

bp = Blueprint('challenge', __name__, url_prefix='/challenge')

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

@bp.route('/analyze/<int:text_id>')
@challenge_required
def analyze_text(text_id):
    """Página de análisis individual"""
    texts = get_challenge_texts()
    text_data = next((text for text in texts if text['id'] == text_id), None)
    if not text_data:
        return "Texto no encontrado", 404
    
    return render_template('challenge/challenge_analysis.html', 
                         text_data=text_data,
                         language=get_locale())

@bp.route('/results')
@challenge_required
def results():
    """Página de resultados y ranking"""
    return render_template('challenge/challenge_results.html', 
                         language=get_locale())


