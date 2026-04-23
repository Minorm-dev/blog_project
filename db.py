"""
Модуль для работы с базой данных SQLite.
Содержит функцию подключения и инициализации схемы.
"""

import sqlite3

DATABASE = 'database.db'

def get_db_connection():
    """
    Создаёт и возвращает соединение с базой данных.
    Устанавливает row_factory = sqlite3.Row для доступа по именам колонок.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Инициализирует базу данных: создаёт все необходимые таблицы,
    если они ещё не существуют, и заполняет начальными данными (site_stats).
    Вызывается один раз при старте приложения.
    """
    conn = get_db_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            role TEXT DEFAULT 'author',
            mood TEXT DEFAULT 'сумрачное',
            style TEXT DEFAULT 'готика / html',
            loving TEXT DEFAULT 'тишину и код'
        );

        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            author_id INTEGER,
            published BOOLEAN DEFAULT 1,
            FOREIGN KEY(author_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS site_stats (
            id INTEGER PRIMARY KEY,
            visits INTEGER DEFAULT 0
        );
        INSERT OR IGNORE INTO site_stats (id, visits) VALUES (1, 0);

        CREATE TABLE IF NOT EXISTS guestbook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip TEXT
        );
    """)
    conn.close()