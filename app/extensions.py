"""Инициализация внешних библиотек."""

from itsdangerous import URLSafeTimedSerializer
from flask import current_app

serializer = None

def init_serializer(app):
    global serializer
    serializer = URLSafeTimedSerializer(app.secret_key)