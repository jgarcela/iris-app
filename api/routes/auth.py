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

import database.db as db
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

    users = db.DB_USERS
    if users.find_one({'email': email}):
        return jsonify(msg="El correo ya está en uso"), 409

    pw_hash = generate_password_hash(password)
    users.insert_one({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': pw_hash,
        'roles': ['user']      # rol base
    })
    return jsonify(msg="Registro correcto"), 201



@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    email    = data.get('email','').strip().lower()
    password = data.get('password','')

    user = db.DB_USERS.find_one({'email': email})
    if not user or not check_password_hash(user['password'], password):
        return jsonify(msg="Credenciales inválidas"), 401

    access_token = create_access_token(identity=str(user['_id']))
    return jsonify(access_token=access_token), 200



@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    # Recuperamos el doc completo excepto la contraseña
    user = db.DB_USERS.find_one(
        {'_id': ObjectId(user_id)},
        {'password': 0}
    )

    if not user:
        return jsonify(msg="Usuario no existe"), 404

    # Serializamos dinámicamente
    user['id'] = str(user.pop('_id'))
    # Eliminamos cualquier otro campo sensible si hiciera falta
    # ej. user.pop('some_other_sensitive_field', None)

    return jsonify(user=user), 200



@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity     = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200


@bp.route('/roles/list_roles', methods=['GET'])
def list_roles():
    roles = list(db.DB_ROLES.find({}, {'_id':0}))
    return jsonify(roles=roles), 200


@bp.route('/roles/create_role', methods=['POST'])
def create_role():
    data = request.get_json(force=True)
    name = data.get('name','').strip()
    perms = data.get('permissions', [])
    if not name:
        return jsonify(msg="Nombre del rol es obligatorio"),400
    if db.DB_ROLES.find_one({'name':name}):
        return jsonify(msg="Rol ya existe"),409
    db.DB_ROLES.insert_one({'name':name,'permissions':perms})
    return jsonify(msg="Rol creado"),201


@bp.route('/roles/update_role/<name>', methods=['PUT'])
def update_role(name):
    data = request.get_json(force=True)
    perms = data.get('permissions')
    if perms is None:
        return jsonify(msg="permissions es obligatorio"),400
    res = db.DB_ROLES.update_one({'name':name},{'$set':{'permissions':perms}})
    if res.matched_count==0:
        return jsonify(msg="Rol no encontrado"),404
    return jsonify(msg="Rol actualizado"),200

@bp.route('/permissions/list_permissions', methods=['GET'])
def list_permissions():
    perms = list(db.DB_PERMISSIONS.find({}, {'_id':0}))
    return jsonify(permissions=perms),200

@bp.route('/permissions/create_permission', methods=['POST'])
def create_permission():
    data = request.get_json(force=True)
    name = data.get('name','').strip()
    desc = data.get('description','').strip()
    if not name:
        return jsonify(msg="Nombre es obligatorio"),400
    if db.DB_PERMISSIONS.find_one({'name':name}):
        return jsonify(msg="Permiso ya existe"),409
    db.DB_PERMISSIONS.insert_one({'name':name,'description':desc})
    return jsonify(msg="Permiso creado"),201