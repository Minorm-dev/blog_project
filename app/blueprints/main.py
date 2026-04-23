"""Главная страница, поиск, счётчик посещений."""

from flask import Blueprint, render_template, request, g
from db import get_db_connection

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    Главная страница со списком опубликованных постов.
    Поддерживает поиск (GET-параметр q) и пагинацию.
    """
    conn = get_db_connection()
    query = request.args.get('q', '').strip()
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page

    base_query = """
        FROM posts
        JOIN users ON posts.author_id = users.id
        WHERE posts.published = 1
    """
    params = []
    if query:
        base_query += " AND (posts.title LIKE ? OR posts.content LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%"])

    total = conn.execute(f"SELECT COUNT(*) {base_query}", params).fetchone()[0]
    posts = conn.execute(
        f"""
            SELECT posts.*, users.username
            {base_query}
            ORDER BY posts.created_at DESC
            LIMIT ? OFFSET ?
        """,
        params + [per_page, offset]
    ).fetchall()
    conn.close()

    total_pages = (total + per_page - 1) // per_page

    # обновляем счётчик посещений
    conn = get_db_connection()
    conn.execute("UPDATE site_stats SET visits = visits + 1 WHERE id = 1")
    conn.commit()
    conn.close()

    return render_template(
        'index.html',
        posts=posts,
        page=page,
        total_pages=total_pages,
        query=query
    )

