# Authentication utilities with intentional security vulnerabilities
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from config import Config
from models import User, db
from utils.logger import log_login_attempt, log_user_action

# VULNERABLE: Weak JWT secret
JWT_SECRET = Config.JWT_SECRET_KEY

def generate_token(user_id, username):
    """Generate JWT token - VULNERABLE: No expiration or very long expiration"""
    # VULNERABLE: Tokens never expire (expiration set to None in config)
    payload = {
        'user_id': user_id,
        'username': username,
        'iat': datetime.utcnow(),
        # No 'exp' field - tokens never expire
    }
    
    # VULNERABLE: Using weak secret
    token = jwt.encode(payload, JWT_SECRET, algorithm=Config.JWT_ALGORITHM)
    # Fix: PyJWT 1.6.4 returns bytes, need to decode to string for JSON serialization
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def verify_token(token):
    """Verify JWT token - VULNERABLE: Weak validation"""
    try:
        # VULNERABLE: No expiration check, weak secret
        payload = jwt.decode(token, JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        return None

def get_current_user():
    """Get current user from token - VULNERABLE: No proper validation"""
    token = None
    
    # VULNERABLE: Token can be passed in multiple insecure ways
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            token = auth_header  # VULNERABLE: Accepts token without Bearer prefix
    
    # Also check query parameter - VULNERABLE
    if not token:
        token = request.args.get('token')
    
    # Also check form data - VULNERABLE
    if not token:
        token = request.form.get('token')
    
    if not token:
        return None
    
    payload = verify_token(token)
    if not payload:
        return None
    
    user = User.query.get(payload.get('user_id'))
    return user

def require_auth(f):
    """Decorator to require authentication - VULNERABLE: Weak validation"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def require_role(required_role):
    """Decorator to require specific role - VULNERABLE: Broken access control"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
            
            # VULNERABLE: Role check can be bypassed
            # Admin can do anything
            if user.role == 'admin':
                return f(*args, **kwargs)
            
            # VULNERABLE: Weak role checking
            if required_role == 'project_manager' and user.role in ['admin', 'project_manager']:
                return f(*args, **kwargs)
            
            if user.role != required_role:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

