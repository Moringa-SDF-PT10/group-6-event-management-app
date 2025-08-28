import os
from dotenv import load_dotenv
from datetime import timedelta

# Loads the environment variables from the .env file
load_dotenv()

class Config:
    # Get the absolute path of the directory containing the current file
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Configured the database URI for SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, '..', 'instance', 'app.db')
    
    # Disabled modification tracking for SQLAlchemy to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Ensure the JSON responses are not sorted by key, preserving order
    JSON_SORT_KEYS = False
    
    # use a secret key from .en file for session management and JWT
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

    # Token expiration times
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Token blocklisting on logout
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

# Test configuration class 
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    TESTING = True
    SECRET_KEY = 'test-secret-key'
    JWT_SECRET_KEY = 'test-jwt-secret-key'