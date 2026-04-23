"""Вспомогательные функции и декораторы."""

from functools import wraps
from flask import session, flash, redirect, url_for, abort

def role_required(*roles):
    """
    Декоратор для ограничения доступа по ролям.
    Пример: @role_required('admin', 'moderator')
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'user_id' not in session:
                flash('Сначала войдите', 'warning')
                return redirect(url_for('auth.login'))
            if session.get('role') not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator

def check_author(post):
    """
    Проверяет, имеет ли текущий пользователь право редактировать/удалять пост.
    Если нет – вызывает 403.
    """
    if post['author_id'] != session.get('user_id'):
        # Если не автор, но админ или модератор – пропускаем
        if not has_role('admin', 'moderator'):
            abort(403)

def has_role(*roles):
    """Проверяет, есть ли у текущего пользователя одна из переданных ролей."""
    return session.get('role') in roles