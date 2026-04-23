"""Конфигурация приложения."""

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super_secret_key')