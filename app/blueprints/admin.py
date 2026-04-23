"""Управление пользователями (только для admin)."""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db_connection
from app.utils import role_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/users')
@role_required('admin')
def manage_users():
    """Список всех пользователей."""
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template('admin_users.html', users=users)

@bp.route('/set_role/<int:user_id>', methods=['POST'])
@role_required('admin')
def set_role(user_id):
    """Назначение роли пользователю."""
    new_role = request.form['role']
    conn = get_db_connection()
    conn.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    conn.commit()
    conn.close()
    flash('Роль обновлена', 'success')
    return redirect(url_for('admin.manage_users'))

