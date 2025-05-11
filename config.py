import os

class Config:
    # SQLite database configuration for easier setup in this environment
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///vitalsoft.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'vitalsoft_secure_key_2024'  # Fixed secret key for session management
