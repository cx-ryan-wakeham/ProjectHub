# Configuration file with intentional security vulnerabilities
# WARNING: This file contains hardcoded secrets for demonstration purposes only

import os

class Config:
    # Hardcoded JWT secret - VULNERABLE
    JWT_SECRET_KEY = "secret_key_12345"
    
    # Hardcoded database credentials - VULNERABLE
    DATABASE_URL = os.environ.get('DATABASE_URL') or "postgresql://projecthub:password123@localhost:5432/projecthub"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://projecthub:password123@localhost:5432/projecthub"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Hardcoded API keys - VULNERABLE
    AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
    AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    AWS_S3_BUCKET = "projecthub-files-public"
    
    # Hardcoded admin credentials - VULNERABLE
    ADMIN_EMAIL = "admin@projecthub.com"
    ADMIN_PASSWORD = "admin123"
    
    # Session configuration - VULNERABLE (no expiration)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
    PERMANENT_SESSION_LIFETIME = None  # Sessions never expire
    
    # JWT configuration - VULNERABLE
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_DELTA = None  # Tokens never expire
    
    # File upload configuration - VULNERABLE
    UPLOAD_FOLDER = "/app/uploads"
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'xml', 'php', 'exe', 'sh'}
    
    # CORS configuration - VULNERABLE (allows all origins)
    CORS_ORIGINS = "*"
    
    # Logging configuration
    LOG_LEVEL = "DEBUG"
    LOG_FILE = "/app/logs/app.log"
    
    # Encryption - VULNERABLE (using weak algorithm)
    PASSWORD_HASH_ALGORITHM = "md5"  # Should use bcrypt or argon2
    
    # API configuration - VULNERABLE
    API_RATE_LIMIT = None  # No rate limiting

