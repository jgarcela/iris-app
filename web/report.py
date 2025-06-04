# web/report.py
from flask import Blueprint, render_template, request, jsonify, session
import requests
from flask_babel import get_locale
import configparser
import ast
from web.logger import logger


# ----------------- BLUEPRINT -----------------
bp = Blueprint(
    'report',
    __name__,
    url_prefix='/report'
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
ENDPOINT_ANALYSIS = config['API']['ENDPOINT_ANALYSIS']
ENDPOINT_ANALYSIS_ANALYZE = config['API']['ENDPOINT_ANALYSIS_ANALYZE']

# ----------------- URLs -----------------
URL_API_ENDPOINT_ANALYSIS_ANALYZE = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_ANALYSIS}/{ENDPOINT_ANALYSIS_ANALYZE}"

#  ----------------- ENDPOINTS -----------------
@bp.route('/create', methods=['GET', 'POST'])
def create():
    logger.info(f"[/REPORT/CREATE] Request to report/create from {request.remote_addr} with method {request.method}")
    logger.info("[/REPORT/CREATE] Rendering report create template...")
    return render_template('report/create_report.html')

