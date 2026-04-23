"""Фабрика Flask-приложения."""

from flask import Flask, render_template, session
from db import get_db_connection
from app.config import Config
from app.extensions import init_serializer

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    # инициализируем расширения
    init_serializer(app)

    # регистрируем blueprints
    from app.blueprints import auth, main, profile, posts, admin, guestbook
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(posts.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(guestbook.bp)

    # контекстный процессор для текущего пользователя и статистики
    @app.context_processor
    def inject_user():
        """
        Добавляет в каждый шаблон переменные:
        - current_user: данные текущего пользователя (или None)
        - stats: словарь с количеством пользователей, постов и посещений
        """
        user = None
        stats = {}
        conn = get_db_connection()
        if 'user_id' in session:
            user = conn.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],)).fetchone()
        stats = {
            "users": conn.execute("SELECT COUNT(*) FROM users").fetchone()[0],
            "posts": conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0],
            "comments": 0,
            "visits": conn.execute("SELECT visits FROM site_stats WHERE id = 1").fetchone()[0]
        }
        conn.close()
        return dict(current_user=user, stats=stats)

    # обработчик ошибки 403
    @app.errorhandler(403)
    def forbidden(e):
        """Страница для ошибки доступа."""
        return render_template('403.html'), 403

    return app

