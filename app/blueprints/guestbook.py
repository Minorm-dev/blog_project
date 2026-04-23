"""Гостевая книга – добавление и просмотр сообщений."""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db_connection

bp = Blueprint('guestbook', __name__, url_prefix='/guestbook')

@bp.route('/', methods=['GET', 'POST'])
def guestbook():
    """Показывает все сообщения и позволяет добавить новое."""
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name'].strip()
        message = request.form['message'].strip()
        if name and message:
            ip = request.remote_addr
            conn.execute(
                "INSERT INTO guestbook (name, message, ip) VALUES (?, ?, ?)",
                (name, message, ip)
            )
            conn.commit()
            flash('Сообщение добавлено в гостевую книгу', 'success')
        else:
            flash('Заполните имя и сообщение', 'danger')
        return redirect(url_for('guestbook.guestbook'))

    entries = conn.execute(
        "SELECT name, message, created_at FROM guestbook ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return render_template('guestbook.html', entries=entries)

