# web/dashboard.py
import json
import re
from flask import Blueprint, render_template, request, jsonify, session, abort
import requests
from flask_babel import get_locale
import configparser
import ast
from collections import Counter
from datetime import datetime

from web.utils.logger import logger
from web.utils.decorators import login_required

# ----------------- BLUEPRINT -----------------
bp = Blueprint(
    'dashboard',
    __name__,
    url_prefix='/dashboard'
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
URL_DASHBOARD_IRIS = config['VARIABLES']['URL_DASHBOARD_IRIS']
ENDPOINT_DATA = config['API']['ENDPOINT_DATA']
ENDPOINT_DATA_GET_CONTEXTO = config['API']['ENDPOINT_DATA_GET_CONTEXTO']
ENDPOINT_DASHBOARD = config['API']['ENDPOINT_DASHBOARD']

COLLECTION_DATA = config['DATABASE']['COLLECTION_DATA']
CONTEXTO_DATA = config['DATABASE']['CONTEXTO_DATA']

# ----------------- URLs -----------------
URL_API_ENDPOINT_DATA = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_DATA}"
URL_API_ENDPOINT_DATA_COLLECTION = f"{URL_API_ENDPOINT_DATA}/{COLLECTION_DATA}"
URL_API_ENDPOINT_DATA_GET_CONTEXTO = f"{URL_API_ENDPOINT_DATA}/{ENDPOINT_DATA_GET_CONTEXTO}"
URL_API_ENDPOINT_DASHBOARD_DATA = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_DASHBOARD}/{ENDPOINT_DATA}"


#  ----------------- ENDPOINTS -----------------
@bp.route('/iris/old', methods=['GET', 'POST'])
@login_required
def dashboard_iris_old():
    logger.info(f"[/DASHBOARD/IRIS/OLD] Request to dashboard/iris from {request.remote_addr} with method {request.method}")
    logger.info("[/DASHBOARD/IRIS/OLD] Rendering dashboard iris template...")
    return render_template("dashboard/dashboard_iris_old.html", url=URL_DASHBOARD_IRIS)


@bp.route('/iris', methods=['GET', 'POST'])
@login_required
def dashboard_iris():
    logger.info(f"[/DASHBOARD/IRIS] Request from {request.remote_addr} [{request.method}]")

    # 1) Obtén los datos base (sin filtrar)
    try:
        res_data = requests.get(URL_API_ENDPOINT_DATA_COLLECTION, timeout=5)
        res_data.raise_for_status()
        raw_data = res_data.json()
    except Exception as e:
        abort(502, description=f"No se pudo conectar a la API de noticias: {e}")

    # 2) Obtén los contextos únicos
    try:
        res_contexto = requests.get(URL_API_ENDPOINT_DATA_GET_CONTEXTO, timeout=5)
        res_contexto.raise_for_status()
        contexto_payload = res_contexto.json()  # {"contextos": [...]}
        contextos = contexto_payload.get('contextos', [])
    except Exception as e:
        abort(502, description=f"No se pudo obtener contextos: {e}")

    # 3) Lee el filtro de contexto y fecha desde args
    selected_context = request.args.get('context', '').strip()
    fd = request.args.get('fecha_desde')  # formato 'YYYY-MM-DD'
    fh = request.args.get('fecha_hasta')  # formato 'YYYY-MM-DD'

    
    # 4) Filtra por contexto si se ha seleccionado uno
    if selected_context:
        data = [item for item in raw_data if item.get('contexto') == selected_context]
    else:
        data = raw_data

    def parse_fecha_str(s):
        # Asume que en data['Fecha'] está en 'DD/MM/YYYY'
        return datetime.strptime(s, '%d/%m/%Y').date()

    # 5) Filtrar por fechas si se proporcionan
    if fd:
        dt_desde = datetime.strptime(fd, '%Y-%m-%d').date()
        data = [d for d in data if parse_fecha_str(d['Fecha']) >= dt_desde]
    if fh:
        dt_hasta = datetime.strptime(fh, '%Y-%m-%d').date()
        data = [d for d in data if parse_fecha_str(d['Fecha']) <= dt_hasta]

    total_count = len(data) or 1

    # 6) Llama a tu API interna de dashboard-data
    try:
        res_chart = requests.post(
            URL_API_ENDPOINT_DASHBOARD_DATA,
            json={'data': data, 'total_count': total_count},
            timeout=5
        )
        res_chart.raise_for_status()
        payload = res_chart.json()
    except Exception as e:
        abort(502, description=f"No se pudo obtener chart_data: {e}")

    chart_data = payload.get('chart_data', {})

    return render_template(
        'dashboard/dashboard_iris.html',
        total_count=total_count,
        chart_data=chart_data,
        contextos=contextos,
        selected_context=selected_context
    )