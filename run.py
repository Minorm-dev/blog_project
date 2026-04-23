#!/usr/bin/env python
"""
Точка входа в приложение.
Инициализирует базу данных (создаёт таблицы) и запускает Flask-сервер.
"""

from app import create_app
from db import init_db

app = create_app()

if __name__ == '__main__':
    init_db()          # гарантирует наличие всех таблиц
    app.run(debug=True)