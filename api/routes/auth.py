# api/routes/auth.py

# ==================================
#  LIBRARIES 
# ==================================
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from bson import ObjectId
import re

from database.db import db
from api.utils.logger import logger

import api


# ==================================
#  BLUEPRINT 
# ==================================
bp = Blueprint('auth', __name__, url_prefix='/auth')


# ==================================
#  ENDPOINTS 
# ==================================
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True)
    first_name = data.get('first_name', '').strip()
    last_name  = data.get('last_name', '').strip()
    email      = data.get('email', '').strip().lower()
    password   = data.get('password', '')

    # Validaciones
    if not all([first_name, last_name, email, password]):
        return jsonify(msg="Todos los campos son obligatorios"), 400

    # Validación de formato de email con regex:
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify(msg="Formato de correo inválido"), 400

    users = db[api.COLLECTION_USERS]
    if users.find_one({'email': email}):
        return jsonify(msg="El correo ya está en uso"), 409

    pw_hash = generate_password_hash(password)
    users.insert_one({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': pw_hash
    })
    return jsonify(msg="Registro correcto"), 201



@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    email    = data.get('email','').strip().lower()
    password = data.get('password','')

    user = db[api.COLLECTION_USERS].find_one({'email': email})
    if not user or not check_password_hash(user['password'], password):
        return jsonify(msg="Credenciales inválidas"), 401

    access_token = create_access_token(identity=str(user['_id']))
    return jsonify(access_token=access_token), 200



@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = db[api.COLLECTION_USERS].find_one({'_id': ObjectId(user_id)}, {'password': 0})

    if user is None:
        return jsonify(msg="Usuario no existe"), 404

    return jsonify(user={
        'id': str(user['_id']),
        'first_name': user.get('first_name'),
        'last_name':  user.get('last_name'),
        'email':      user.get('email'),
    }), 200


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity     = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200