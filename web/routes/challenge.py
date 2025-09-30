# web/routes/challenge.py
from flask import Blueprint, render_template, request, jsonify, session, abort
from web.utils.logger import logger
from web.utils.decorators import login_required

# ----------------- BLUEPRINT -----------------
bp = Blueprint(
    'challenge',
    __name__,
    url_prefix='/challenge'
)

#  ----------------- ENDPOINTS -----------------
@bp.route('/desafio', methods=['GET'])
@login_required
def desafio():
    logger.info(f"[/CHALLENGE/DESAFIO] Request to challenge/desafio from {request.remote_addr}")
    return render_template('challenge/desafio.html')
