
import ast
import configparser
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from web.utils.logger import logger
from web.utils.decorators import login_required

# ----------------- BLUEPRINT -----------------
bp = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)

bp = Blueprint('auth', __name__, url_prefix='')

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

ENDPOINT_AUTH = config['API']['ENDPOINT_AUTH']
ENDPOINT_AUTH_REGISTER = config['API']['ENDPOINT_AUTH_REGISTER']
ENDPOINT_AUTH_LOGIN = config['API']['ENDPOINT_AUTH_LOGIN']
ENDPOINT_AUTH_ME = config['API']['ENDPOINT_AUTH_ME']
ENDPOINT_AUTH_REFRESH = config['API']['ENDPOINT_AUTH_REFRESH']


# ----------------- URLs -----------------
URL_API_ENDPOINT_AUTH = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_AUTH}"
# URL_API_ENDPOINT_AUTH_REGISTER = f"{URL_API_ENDPOINT_AUTH}/{ENDPOINT_AUTH_REGISTER}"
URL_API_ENDPOINT_AUTH_REGISTER = f"/api/auth/{ENDPOINT_AUTH_REGISTER}"
URL_API_ENDPOINT_AUTH_LOGIN = f"{URL_API_ENDPOINT_AUTH}/{ENDPOINT_AUTH_LOGIN}"
URL_API_ENDPOINT_AUTH_ME = f"{URL_API_ENDPOINT_AUTH}/{ENDPOINT_AUTH_ME}"
URL_API_ENDPOINT_AUTH_REFRESH = f"{URL_API_ENDPOINT_AUTH}/{ENDPOINT_AUTH_REFRESH}"

#  ----------------- ENDPOINTS -----------------
@bp.route('/login', methods=['GET'])
def login():
    # Si ya tienes token en cookie, opcionalmente rediriges a home
    if request.cookies.get('access_token_cookie'):
        return redirect(url_for('home'))
    print(f"{URL_API_ENDPOINT_AUTH_LOGIN=}")
    return render_template('auth/login.html', 
                            api_url_login=URL_API_ENDPOINT_AUTH_LOGIN)


@bp.route('/register', methods=['GET'])
def register():
    if request.cookies.get('access_token_cookie'):
        return redirect(url_for('home'))
    return render_template('auth/register.html',
                           api_url_register=URL_API_ENDPOINT_AUTH_REGISTER)


@bp.route('/logout', methods=['GET'])
def logout():
    # Para “deslogear” borras la cookie de acceso
    resp = make_response(redirect(url_for('auth.login')))
    resp.set_cookie('access_token_cookie', '', expires=0)
    return resp