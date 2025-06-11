# app/web/admin.py

import ast
import configparser
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, current_app
)
from web.utils.decorators import login_required, role_required
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
        'admin_dashboard.html',
        total_users=total_users,
        total_roles=total_roles,
        total_permissions=total_permissions
    )

# ----------------- USERS -----------------
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

    return render_template('admin_users.html', users=users)

# ----------------- ROLES -----------------
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
        'admin_roles.html',
        roles=roles,
        all_permissions=permissions
    )

# ----------------- PERMISSIONS -----------------
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
        'admin_permissions.html',
        permissions=permissions
    )
