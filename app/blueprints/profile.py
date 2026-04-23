"""Профиль пользователя и его посты."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection
from app.utils import role_required  # если понадобится

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/', methods=['GET', 'POST'])
def profile():
    """Просмотр и редактирование профиля (настроение, стиль, любовь)."""
    if 'user_id' not in session:
        flash('Сначала войдите в систему', 'warning')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    posts = conn.execute(
        "SELECT * FROM posts WHERE author_id = ? ORDER BY created_at DESC",
        (session['user_id'],)
    ).fetchall()

    if request.method == 'POST':
        mood = request.form['mood'].strip()
        style = request.form['style'].strip()
        loving = request.form['loving'].strip()
        conn.execute(
            "UPDATE users SET mood = ?, style = ?, loving = ? WHERE id = ?",
            (mood, style, loving, session['user_id'])
        )
        conn.commit()
        flash('Профиль обновлён', 'success')
    conn.close()
    return render_template('profile.html', user=user, posts=posts)
