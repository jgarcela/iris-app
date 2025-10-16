# web/table.py
import json
import re
from flask import Blueprint, render_template, request, jsonify, session, abort
import requests
from flask_babel import get_locale
import configparser
import ast
from datetime import datetime

from web.utils.logger import logger

from web.utils.decorators import login_required, challenge_restricted

# ----------------- BLUEPRINT -----------------
bp = Blueprint(
    'table',
    __name__,
    url_prefix='/table'
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

ENDPOINT_DATA = config['API']['ENDPOINT_DATA']
ENDPOINT_DATA_GET_CONTEXTO = config['API']['ENDPOINT_DATA_GET_CONTEXTO']
ENDPOINT_DASHBOARD = config['API']['ENDPOINT_DASHBOARD']

COLLECTION_DATA = config['DATABASE']['COLLECTION_DATA']
CONTEXTO_DATA = config['DATABASE']['CONTEXTO_DATA']

# ----------------- URLs -----------------
URL_API_ENDPOINT_DATA = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_DATA}"
URL_API_ENDPOINT_DATA_COLLECTION = f"{URL_API_ENDPOINT_DATA}/{COLLECTION_DATA}"
URL_API_ENDPOINT_DATA_GET_CONTEXTO = f"{URL_API_ENDPOINT_DATA}/{ENDPOINT_DATA_GET_CONTEXTO}"

#  ----------------- ENDPOINTS -----------------
@bp.route("/iris")
@login_required
@challenge_restricted
def table_iris():

    logger.info(f"[/TABLE/IRIS] Request from {request.remote_addr} [{request.method}]")

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


    # 6) Modificar formato de las columnas a mostrar o ocultar y el orden
    exclude_cols = [
               'textonoticia',
               'nombre_periodista',
               '_id',
               'Tipo de elemento',
               'Ruta de acceso',
               'NombreUsuario',
               'Contenido',
               'verificacion'
            ]
    
    order_cols = [
              'contexto',
              'IdNoticia',
              'MES',
              'Fecha',
              'MMCC',
              'Pagina',
              'Titular',
              'Autor',
              'Caracteres'
            ]
    
    input_filter_cols = [
        'Autor',
        'Caracteres',
        'Fecha',
        'IdNoticia',
        'Pagina',
        'Ruta de acceso',
        'Tipo de elemento',
        'Titular',
        'nombre_propio_titular',
        'numero_caracteres'
    ]
    
    # 7) Finalmente renderizamos el template pasando la lista de noticias
    return render_template("table/table_iris.html", 
                            data=data, 
                            exclude_cols=exclude_cols, 
                            order_cols=order_cols,
                            input_filter_cols=input_filter_cols,
                            contextos=contextos,
                            selected_context=selected_context)