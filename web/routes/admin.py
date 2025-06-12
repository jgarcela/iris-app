# app/web/admin.py

import ast
import configparser
from bson import ObjectId
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, current_app
)
from werkzeug.security import generate_password_hash

from web.utils.decorators import login_required #, role_required
import database.db as db

# ----------------- BLUEPRINT -----------------
bp = Blueprint('admin', __name__, url_prefix='/admin')

# ----------------- DASHBOARD -----------------
@bp.route('/dashboard')
@login_required
# @role_required('admin')
def admin_dashboard():
    total_users       = db.DB_USERS.count_documents({})
    total_roles       = db.DB_ROLES.count_documents({})
    total_permissions = db.DB_PERMISSIONS.count_documents({})
    return render_template(
        'admin/admin_dashboard.html',
        total_users=total_users,
        total_roles=total_roles,
        total_permissions=total_permissions
    )

# ----------------- USERS -----------------
# Listar users
@bp.route('/users')
@login_required
# @role_required('admin')
def list_users():
    raw_users = list(db.DB_USERS.find({}, {'password_hash': 0}))
    users = []

    # Para cada usuario, recolectamos permisos de sus roles
    for u in raw_users:
        perms = set()
        for role_name in u.get('roles', []):
            role = db.DB_ROLES.find_one({'name': role_name})
            if role:
                perms.update(role.get('permissions', []))
        # Serializamos _id para la plantilla y añadimos 'permissions'
        users.append({
            '_id': str(u['_id']),
            'first_name': u.get('first_name'),
            'last_name':  u.get('last_name'),
            'email':      u.get('email'),
            'roles':      u.get('roles', []),
            'permissions': sorted(perms)
        })

    return render_template('admin/admin_users.html', users=users)


# Crear user
@bp.route('/users/create', methods=['GET','POST'])
@login_required
# @role_required('admin')
def create_user():
    roles = [r['name'] for r in db.DB_ROLES.find({}, {'name':1})]
    if request.method == 'POST':
        first = request.form['first_name'].strip()
        last  = request.form['last_name'].strip()
        email = request.form['email'].strip().lower()
        pwd   = request.form['password']
        chosen_roles = request.form.getlist('roles')
        if not all([first,last,email,pwd]):
            flash('Todos los campos son obligatorios','warning')
            return redirect(url_for('admin.create_user'))
        if db.DB_USERS.find_one({'email':email}):
            flash('El correo ya existe','danger')
            return redirect(url_for('admin.create_user'))
        db.DB_USERS.insert_one({
            'first_name': first,
            'last_name': last,
            'email': email,
            'password_hash': generate_password_hash(pwd),
            'roles': chosen_roles
        })
        flash('Usuario creado','success')
        return redirect(url_for('admin.list_users'))
    return render_template('admin/admin_user_form.html', roles=roles, action='create')


# Editar user
@bp.route('/users/<user_id>/edit', methods=['GET','POST'])
@login_required
# @role_required('admin')
def edit_user(user_id):
    user = db.DB_USERS.find_one({'_id': ObjectId(user_id)}, {'password_hash':0})
    if not user:
        flash('Usuario no encontrado','danger')
        return redirect(url_for('admin.list_users'))
    roles = [r['name'] for r in db.DB_ROLES.find({}, {'name':1})]
    if request.method=='POST':
        # actualiza campos (sin contraseña si está vacío)
        data = {
            'first_name': request.form['first_name'].strip(),
            'last_name' : request.form['last_name'].strip(),
            'email'     : request.form['email'].strip().lower(),
            'roles'     : request.form.getlist('roles')
        }
        pwd = request.form['password']
        if pwd:
            data['password_hash'] = generate_password_hash(pwd)
        db.DB_USERS.update_one({'_id':ObjectId(user_id)}, {'$set':data})
        flash('Usuario actualizado','success')
        return redirect(url_for('admin.list_users'))
    # convierte ObjectId y envía
    user['_id'] = str(user['_id'])
    return render_template('admin/admin_user_form.html', roles=roles, user=user, action='edit')

# Borrar user
@bp.route('/users/<user_id>/delete', methods=['POST'])
@login_required
# @role_required('admin')
def delete_user(user_id):
    db.DB_USERS.delete_one({'_id': ObjectId(user_id)})
    flash('Usuario borrado','info')
    return redirect(url_for('admin/admin.list_users'))


# ----------------- ROLES -----------------
# Listar roles
@bp.route('/roles', methods=['GET', 'POST'])
@login_required
# @role_required('admin')
def list_roles():
    if request.method == 'POST':
        name        = request.form.get('name', '').strip()
        permissions = request.form.getlist('permissions')
        if not name:
            flash('El nombre de rol es obligatorio.', 'warning')
        else:
            if db.DB_ROLES.find_one({'name': name}):
                flash('Ese rol ya existe.', 'danger')
            else:
                db.DB_ROLES.insert_one({'name': name, 'permissions': permissions})
                flash(f'Rol "{name}" creado.', 'success')
        return redirect(url_for('admin.list_roles'))

    roles       = list(db.DB_ROLES.find({}, {'_id': 0}))
    permissions = [p['name'] for p in db.DB_PERMISSIONS.find({}, {'name': 1})]
    return render_template(
        'admin/admin_roles.html',
        roles=roles,
        all_permissions=permissions
    )


# Crear rol
@bp.route('/roles/create', methods=['GET', 'POST'])
@login_required
# @role_required('admin')
def create_role():
    all_permissions = [p['name'] for p in db.DB_PERMISSIONS.find({}, {'name': 1})]
    if request.method == 'POST':
        name = request.form['name'].strip()
        permissions = request.form.getlist('permissions')
        if not name:
            flash('El nombre del rol es obligatorio.', 'warning')
            return redirect(url_for('admin.create_role'))
        if db.DB_ROLES.find_one({'name': name}):
            flash('Ese rol ya existe.', 'danger')
            return redirect(url_for('admin.create_role'))
        db.DB_ROLES.insert_one({'name': name, 'permissions': permissions})
        flash(f'Rol "{name}" creado correctamente.', 'success')
        return redirect(url_for('admin.list_roles'))
    return render_template(
        'admin/admin_role_form.html',
        action='create',
        all_permissions=all_permissions
    )

# Editar rol
@bp.route('/roles/<role_name>/edit', methods=['GET', 'POST'])
@login_required
# @role_required('admin')
def edit_role(role_name):
    role = db.DB_ROLES.find_one({'name': role_name}, {'_id': 0})
    if not role:
        flash('Rol no encontrado.', 'danger')
        return redirect(url_for('admin.list_roles'))
    all_permissions = [p['name'] for p in db.DB_PERMISSIONS.find({}, {'name': 1})]
    if request.method == 'POST':
        permissions = request.form.getlist('permissions')
        db.DB_ROLES.update_one(
            {'name': role_name},
            {'$set': {'permissions': permissions}}
        )
        flash(f'Rol "{role_name}" actualizado.', 'success')
        return redirect(url_for('admin.list_roles'))
    return render_template(
        'admin/admin_role_form.html',
        action='edit',
        role=role,
        all_permissions=all_permissions
    )

# Borrar rol
@bp.route('/roles/<role_name>/delete', methods=['POST'])
@login_required
# @role_required('admin')
def delete_role(role_name):
    result = db.DB_ROLES.delete_one({'name': role_name})
    if result.deleted_count:
        flash(f'Rol "{role_name}" eliminado.', 'info')
    else:
        flash('No se encontró el rol a eliminar.', 'warning')
    return redirect(url_for('admin.list_roles'))


# ----------------- PERMISSIONS -----------------
# Listar permissions
@bp.route('/permissions', methods=['GET', 'POST'])
@login_required
# @role_required('admin')
def list_permissions():
    if request.method == 'POST':
        name        = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        if not name:
            flash('El nombre del permiso es obligatorio.', 'warning')
        else:
            if db.DB_PERMISSIONS.find_one({'name': name}):
                flash('Ese permiso ya existe.', 'danger')
            else:
                db.DB_PERMISSIONS.insert_one({'name': name, 'description': description})
                flash(f'Permiso "{name}" creado.', 'success')
        return redirect(url_for('admin.list_permissions'))

    permissions = list(db.DB_PERMISSIONS.find({}, {'_id': 0}))
    return render_template(
        'admin/admin_permissions.html',
        permissions=permissions
    )


# Crear permissions
@bp.route('/permissions/create', methods=['GET', 'POST'])
@login_required
# @role_required('admin')
def create_permission():
    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form.get('description', '').strip()
        if not name:
            flash('El nombre del permiso es obligatorio.', 'warning')
            return redirect(url_for('admin.create_permission'))
        if db.DB_PERMISSIONS.find_one({'name': name}):
            flash('Ese permiso ya existe.', 'danger')
            return redirect(url_for('admin.create_permission'))
        db.DB_PERMISSIONS.insert_one({
            'name': name,
            'description': description
        })
        flash(f'Permiso "{name}" creado correctamente.', 'success')
        return redirect(url_for('admin.list_permissions'))
    return render_template(
        'admin/admin_permission_form.html',
        action='create'
    )

# Editar permissions
@bp.route('/permissions/<perm_name>/edit', methods=['GET', 'POST'])
@login_required
# @role_required('admin')
def edit_permission(perm_name):
    permission = db.DB_PERMISSIONS.find_one({'name': perm_name}, {'_id': 0})
    if not permission:
        flash('Permiso no encontrado.', 'danger')
        return redirect(url_for('admin.list_permissions'))
    if request.method == 'POST':
        description = request.form.get('description', '').strip()
        db.DB_PERMISSIONS.update_one(
            {'name': perm_name},
            {'$set': {'description': description}}
        )
        flash(f'Permiso "{perm_name}" actualizado.', 'success')
        return redirect(url_for('admin.list_permissions'))
    return render_template(
        'admin/admin_permission_form.html',
        action='edit',
        permission=permission
    )

# Borrar permissions
@bp.route('/permissions/<perm_name>/delete', methods=['POST'])
@login_required
# @role_required('admin')
def delete_permission(perm_name):
    result = db.DB_PERMISSIONS.delete_one({'name': perm_name})
    if result.deleted_count:
        flash(f'Permiso "{perm_name}" eliminado.', 'info')
    else:
        flash('No se encontró el permiso a eliminar.', 'warning')
    return redirect(url_for('admin.list_permissions'))