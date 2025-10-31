
import ast
import configparser
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from web.utils.logger import logger
from web.utils.decorators import login_required
import database.db as db

# ----------------- BLUEPRINT -----------------
bp = Blueprint('contact', __name__, url_prefix='/contact')


@bp.route('/', methods=['GET'])
def contact_iris():
    logger.info("[/CONTACT] Rendering contacto template...")
    return render_template('contact/contact.html')


@bp.route('/send', methods=['POST'])
def contact_send():
    """Save contact form to database."""
    try:
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        message = (request.form.get('message') or '').strip()

        # Validar que haya mensaje
        if not message:
            flash('Por favor, escribe un mensaje.', 'warning')
            return redirect(url_for('contact.contact_iris'))

        # Guardar en base de datos
        contact_data = {
            'name': name,
            'email': email,
            'message': message,
            'created_at': datetime.utcnow(),
            'read': False
        }
        
        db.DB_CONTACT.insert_one(contact_data)
        
        logger.info(f"[/CONTACT] Contact message saved: {email or 'No email'}")
        flash('Mensaje enviado correctamente. Te responderemos pronto.', 'success')
        
    except Exception as e:
        logger.error(f"[/CONTACT] Error saving contact message: {e}", exc_info=True)
        flash('Ha ocurrido un error. Por favor, inténtalo de nuevo más tarde.', 'danger')

    return redirect(url_for('contact.contact_iris'))
