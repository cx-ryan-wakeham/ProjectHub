# Authentication routes
from flask import Blueprint, request, jsonify, session
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_ext import db
from models import User
from auth import generate_token, get_current_user
from config import Config
from utils.logger import log_login_attempt, log_user_action
from sqlalchemy import func
import hashlib

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    """User registration"""
    data = request.get_json() or request.form
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create user
    user = User(username=username, email=email, role='team_member')
    user.set_password(password)
    user.api_key = f"{username}_api_key_{hashlib.md5(password.encode()).hexdigest()}"
    
    db.session.add(user)
    db.session.commit()
    
    log_user_action(user.id, 'register', f"Username: {username}, Email: {email}, Password: {password}")
    
    token = generate_token(user.id, user.username)
    
    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': user.to_dict()
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json() or request.form
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    # Allow login with either username or email (case-insensitive)
    user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
    if not user:
        user = User.query.filter(func.lower(User.email) == func.lower(username)).first()
    
    if not user or not user.check_password(password):
        log_login_attempt(username, password, success=False)
        return jsonify({'error': 'Invalid credentials'}), 401
    
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
        'user': user.to_dict()
    })

@bp.route('/logout', methods=['POST'])
def logout():
    """User logout"""
    user = get_current_user()
    if user:
        log_user_action(user.id, 'logout')
    
    return jsonify({'message': 'Logged out'})

@bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Password reset"""
    data = request.get_json() or request.form
    
    email = data.get('email')
    new_password = data.get('new_password')
    
    if not email or not new_password:
        return jsonify({'error': 'Email and new password required'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.set_password(new_password)
    db.session.commit()
    
    log_user_action(user.id, 'password_reset', f"New password: {new_password}")
    
    return jsonify({'message': 'Password reset successfully'})

@bp.route('/me', methods=['GET'])
def get_current_user_info():
    """Get current user info"""
    user = get_current_user()
    
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    return jsonify({
        'user': user.to_dict()
    })

