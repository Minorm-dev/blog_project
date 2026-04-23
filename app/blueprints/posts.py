"""Управление постами (CRUD)."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from db import get_db_connection
from app.utils import role_required, check_author

bp = Blueprint('posts', __name__, url_prefix='/posts')

@bp.route('/create', methods=['GET', 'POST'])
@role_required('author', 'moderator', 'admin')
def create():
    """Создание нового поста."""
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        published = 1 if request.form.get('published') else 0
        if not title or not content:
            flash('Заполните все поля', 'danger')
            return redirect(url_for('posts.create'))
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO posts (title, content, author_id, published) VALUES (?, ?, ?, ?)",
            (title, content, session['user_id'], published)
        )
        conn.commit()
        conn.close()
        flash('Пост создан!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_post.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Редактирование существующего поста (только автор или модератор/админ)."""
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (id,)).fetchone()
    if not post:
        abort(404)
    check_author(post)   # проверка прав

    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        conn.execute("UPDATE posts SET title=?, content=? WHERE id = ?", (title, content, id))
        conn.commit()
        conn.close()
        flash('Пост обновлен', 'success')
        return redirect(url_for('main.index'))
    conn.close()
    return render_template('edit_post.html', post=post)

@bp.route('/delete/<int:id>')
def delete(id):
    """Удаление поста (только автор или модератор/админ)."""
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (id,)).fetchone()
    if not post:
        abort(404)
    check_author(post)
    conn.execute("DELETE FROM posts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Пост удален', 'info')
    return redirect(url_for('main.index'))

