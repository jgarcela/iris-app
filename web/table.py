# web/dashboard.py
import json
import re
from flask import Blueprint, render_template, request, jsonify, session, abort
import requests
from flask_babel import get_locale
import configparser
import ast
from web.logger import logger


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
def table_iris():
    """
    1) Hace petición GET a URL_API_ENDPOINT_DATA_NOTICIAS
    2) Comprueba si el status_code es 200. Si no, aborta con error.
    3) Asume que la respuesta es un JSON con un array de objetos.
    4) Toma la lista y la pasa al template como 'noticias'.
    """

    try:
        respuesta = requests.get(URL_API_ENDPOINT_DATA_COLLECTION, timeout=5)
    except requests.RequestException as e:
        # Si falla la conexión, devolvemos error 502 Bad Gateway (la API no responde)
        abort(502, description=f"No se pudo conectar a la API: {e}")

    if respuesta.status_code != 200:
        # Si la API devuelve un error, por ejemplo 404 o 500, rebotamos ese código
        abort(respuesta.status_code, description="Error al obtener datos desde la API")

    # Asumimos que JSON es una lista de documentos (diccionarios):
    try:
        lista_noticias = respuesta.json()
    except ValueError:
        # Si la API no devuelve un JSON válido, devolvemos un 500 Interno
        abort(500, description="Respuesta de la API no es un JSON válido")

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
    
    # Finalmente renderizamos el template pasando la lista de noticias
    return render_template("table_iris.html", 
                           noticias=lista_noticias, 
                           exclude_cols=exclude_cols, 
                           order_cols=order_cols,
                           input_filter_cols=input_filter_cols)