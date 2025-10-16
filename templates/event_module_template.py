# 🎯 Event Module Template
# Copia este archivo y renómbralo según tu evento
# Ejemplo: web/routes/concurso_literario.py

from flask import Blueprint, render_template, request, jsonify, url_for
from flask_babel import get_locale, _
from web.utils.event_decorators import event_required  # Renombrar según tu evento
from database.db import DB_EVENT_COLLECTION  # Renombrar según tu evento
from datetime import datetime, timezone
import configparser
import ast
import requests

# ----------------- BLUEPRINT -----------------
bp = Blueprint('nombre_evento', __name__, url_prefix='/nombre_evento')  # Cambiar nombre

# ----------------- CONFIG -----------------
config = configparser.ConfigParser()
config.read('config.ini')

API_HOST = config['API']['HOST']
API_PORT = config['API']['PORT']
API_HEADERS_str = config['API']['HEADERS']
API_HEADERS = ast.literal_eval(API_HEADERS_str)

# ----------------- HELPER FUNCTIONS -----------------
def get_event_data():
    """Fetch event data from database"""
    try:
        # Implementar lógica específica del evento
        data = DB_EVENT_COLLECTION.find({}).sort('id', 1)
        return list(data)
    except Exception as e:
        print(f"Error fetching event data: {e}")
        return []

# ----------------- ROUTES -----------------
@bp.route('/')
@event_required
def event_home():
    """Página principal del evento"""
    data = get_event_data()
    return render_template('nombre_evento/event_home.html', 
                         data=data,
                         language=get_locale())

@bp.route('/participate/<int:item_id>')
@event_required
def participate(item_id):
    """Página de participación individual"""
    data = get_event_data()
    item_data = next((item for item in data if item['id'] == item_id), None)
    if not item_data:
        return "Item no encontrado", 404
    
    return render_template('nombre_evento/event_participate.html', 
                         item_data=item_data,
                         language=get_locale())

@bp.route('/results')
@event_required
def results():
    """Página de resultados"""
    return render_template('nombre_evento/event_results.html', 
                         language=get_locale())

# ----------------- API ENDPOINTS -----------------
@bp.route('/submit', methods=['POST'])
@event_required
def submit():
    """Submit event participation"""
    try:
        payload = request.get_json(force=True)
        # Implementar lógica de envío
        return jsonify(success=True, message="Submission successful")
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500
