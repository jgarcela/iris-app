
import ast
import configparser
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from web.utils.logger import logger
from web.utils.decorators import login_required

# ----------------- BLUEPRINT -----------------
bp = Blueprint('contact', __name__, url_prefix='/contact')


@bp.route('/', methods=['GET'])
def contact_iris():
    logger.info("[/CONTACT] Rendering contacto template...")
    return render_template('contact/contact.html')
