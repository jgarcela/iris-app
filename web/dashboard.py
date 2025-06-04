# web/dashboard.py
import json
import re
from flask import Blueprint, render_template, request, jsonify, session
import requests
from flask_babel import get_locale
import configparser
import ast
from web.logger import logger


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


#  ----------------- ENDPOINTS -----------------
@bp.route('/iris', methods=['GET', 'POST'])
def dashboard_iris():
    logger.info(f"[/DASHBOARD/IRIS] Request to dashboard/iris from {request.remote_addr} with method {request.method}")
    logger.info("[/DASHBOARD/IRIS] Rendering dashboard iris template...")
    return render_template("dashboard_iris.html", url=URL_DASHBOARD_IRIS)