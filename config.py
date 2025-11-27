import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'minha-chave-secreta'
    JWT_SECRET_KEY = 'minha-jwt-secreta'
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    DB_PATH = 'database/db.json'