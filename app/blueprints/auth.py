"""Blueprints для регистрации, входа, выхода и сброса пароля."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
from app.extensions import serializer
from app.models import get_user_by_username

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация нового пользователя."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        if not username or not email or not password:
            flash('Все поля обязательны для заполнения!', 'danger')
            return redirect(url_for('auth.register'))

        password_hash = generate_password_hash(password)
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('auth.login'))
        except Exception:
            flash('Пользователь уже существует!', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Вход пользователя в систему."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        user = get_user_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    """Выход из системы."""
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('main.index'))

@bp.route('/reset', methods=['GET', 'POST'])
def reset_request():
    """Запрос на сброс пароля (показывает ссылку вместо email)."""
    if request.method == 'POST':
        email = request.form['email'].strip()
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        if user:
            token = serializer.dumps(email, salt='password-reset')
            reset_link = url_for('auth.reset_token', token=token, _external=True)
            flash(f'Ссылка для сброса: {reset_link}', 'info')
        else:
            flash('Пользователь с таким email не найден', 'danger')
    return render_template('reset_request.html')

@bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """Установка нового пароля по токену."""
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)
    except Exception:
        flash('Ссылка недействительна или устарела', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        password = request.form['password'].strip()
        if not password:
            flash('Введите пароль', 'danger')
            return redirect(url_for('auth.reset_token', token=token))
        password_hash = generate_password_hash(password)
        conn = get_db_connection()
        conn.execute("UPDATE users SET password_hash = ? WHERE email = ?", (password_hash, email))
        conn.commit()
        conn.close()
        flash('Пароль успешно обновлен', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html')
