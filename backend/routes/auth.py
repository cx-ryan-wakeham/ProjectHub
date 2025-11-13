# Authentication routes with intentional security vulnerabilities
from flask import Blueprint, request, jsonify, session
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import User, db
from auth import generate_token, get_current_user
from config import Config
from utils.logger import log_login_attempt, log_user_action
from sqlalchemy import func
import hashlib

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    """User registration - VULNERABLE: No rate limiting, weak validation"""
    data = request.get_json() or request.form
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # VULNERABLE: Weak validation
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # VULNERABLE: No password strength requirements
    # VULNERABLE: No email validation
    # VULNERABLE: No CAPTCHA
    
    # Check if user exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create user
    user = User(username=username, email=email, role='team_member')
    user.set_password(password)  # VULNERABLE: Uses MD5 hashing
    
    # VULNERABLE: Generate API key in plain text
    user.api_key = f"{username}_api_key_{hashlib.md5(password.encode()).hexdigest()}"
    
    db.session.add(user)
    db.session.commit()
    
    # VULNERABLE: Log sensitive information
    log_user_action(user.id, 'register', f"Username: {username}, Email: {email}, Password: {password}")
    
    token = generate_token(user.id, user.username)
    
    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': user.to_dict()  # VULNERABLE: Exposes sensitive data
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    """User login - VULNERABLE: No rate limiting, session fixation, logs passwords"""
    data = request.get_json() or request.form
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    # VULNERABLE: No rate limiting on login attempts
    # VULNERABLE: No CAPTCHA after failed attempts
    
    # Allow login with either username or email (case-insensitive)
    user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
    if not user:
        user = User.query.filter(func.lower(User.email) == func.lower(username)).first()
    
    if not user or not user.check_password(password):
        # VULNERABLE: Logs password in plain text
        log_login_attempt(username, password, success=False)
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # VULNERABLE: Session fixation - doesn't regenerate session ID
    # VULNERABLE: No MFA
    
    # VULNERABLE: Logs password in plain text
    log_login_attempt(username, password, success=True)
    log_user_action(user.id, 'login', f"IP: {request.remote_addr}")
    
    # Update last login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    token = generate_token(user.id, user.username)
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()  # VULNERABLE: Exposes sensitive data
    })

@bp.route('/logout', methods=['POST'])
def logout():
    """User logout - VULNERABLE: Doesn't invalidate token"""
    # VULNERABLE: Tokens are stateless and never expire, so logout doesn't work
    user = get_current_user()
    if user:
        log_user_action(user.id, 'logout')
    
    return jsonify({'message': 'Logged out'})

@bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Password reset - VULNERABLE: No validation, no CAPTCHA, no rate limiting"""
    data = request.get_json() or request.form
    
    email = data.get('email')
    new_password = data.get('new_password')
    
    if not email or not new_password:
        return jsonify({'error': 'Email and new password required'}), 400
    
    # VULNERABLE: No email verification
    # VULNERABLE: No token-based reset flow
    # VULNERABLE: No CAPTCHA
    # VULNERABLE: No rate limiting
    # VULNERABLE: Weak password validation
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        # VULNERABLE: Information disclosure - reveals if email exists
        return jsonify({'error': 'User not found'}), 404
    
    # VULNERABLE: Allows password reset without verification
    user.set_password(new_password)
    db.session.commit()
    
    log_user_action(user.id, 'password_reset', f"New password: {new_password}")
    
    return jsonify({'message': 'Password reset successfully'})

@bp.route('/me', methods=['GET'])
def get_current_user_info():
    """Get current user info - VULNERABLE: Exposes sensitive data"""
    user = get_current_user()
    
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    return jsonify({
        'user': user.to_dict()  # VULNERABLE: Exposes password hash and API key
    })

