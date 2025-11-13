# Messaging routes with intentional security vulnerabilities (XSS)
from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Message, User, db
from auth import require_auth, get_current_user
from utils.logger import log_user_action
from datetime import datetime

bp = Blueprint('messages', __name__)

@bp.route('', methods=['GET'])
@require_auth
def get_messages():
    """Get messages - VULNERABLE: IDOR, broken access control"""
    user = get_current_user()
    
    # VULNERABLE: Users can see all messages by changing query parameters
    sender_id = request.args.get('sender_id')
    receiver_id = request.args.get('receiver_id')
    
    query = Message.query
    
    # VULNERABLE: IDOR - users can access other users' messages
    if sender_id:
        query = query.filter_by(sender_id=sender_id)
    if receiver_id:
        query = query.filter_by(receiver_id=receiver_id)
    
    # VULNERABLE: Should filter by current user, but allows seeing all messages
    # Order by most recent first
    messages = query.order_by(Message.created_at.desc()).all()
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Calculate pagination
    total = len(messages)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_messages = messages[start:end]
    
    # VULNERABLE: XSS in content - no sanitization
    return jsonify({
        'messages': [m.to_dict() for m in paginated_messages],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    })

@bp.route('/<int:message_id>', methods=['GET'])
@require_auth
def get_message(message_id):
    """Get message by ID - VULNERABLE: IDOR"""
    user = get_current_user()
    
    # VULNERABLE: IDOR - no check if user is sender or receiver
    message = Message.query.get(message_id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    # VULNERABLE: Broken access control - any user can read any message
    # Should check: message.sender_id == user.id or message.receiver_id == user.id
    
    # Mark as read if user is receiver
    if message.receiver_id == user.id:
        message.is_read = True
        db.session.commit()
    
    return jsonify({
        'message': message.to_dict()  # VULNERABLE: XSS in content
    })

@bp.route('', methods=['POST'])
@require_auth
def send_message():
    """Send message - VULNERABLE: XSS, no input validation, IDOR"""
    user = get_current_user()
    data = request.get_json() or request.form
    
    receiver_id = data.get('receiver_id')
    subject = data.get('subject', '')
    content = data.get('content')
    
    if not receiver_id or not content:
        return jsonify({'error': 'Receiver ID and content required'}), 400
    
    # VULNERABLE: No input sanitization (XSS in subject and content)
    # VULNERABLE: No validation
    
    receiver = User.query.get(receiver_id)
    if not receiver:
        return jsonify({'error': 'Receiver not found'}), 404
    
    message = Message(
        sender_id=user.id,
        receiver_id=receiver_id,
        subject=subject,  # VULNERABLE: Stored without sanitization
        content=content  # VULNERABLE: Stored without sanitization (XSS)
    )
    
    db.session.add(message)
    db.session.commit()
    
    log_user_action(user.id, 'send_message', f"To: {receiver_id}, Subject: {subject}, Content: {content}")
    
    return jsonify({
        'message': 'Message sent successfully',
        'message_data': message.to_dict()
    }), 201

@bp.route('/<int:message_id>', methods=['DELETE'])
@require_auth
def delete_message(message_id):
    """Delete message - VULNERABLE: Broken access control, IDOR"""
    user = get_current_user()
    
    message = Message.query.get(message_id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    # VULNERABLE: Broken access control - any user can delete any message
    # Should check: message.sender_id == user.id or message.receiver_id == user.id
    
    db.session.delete(message)
    db.session.commit()
    
    log_user_action(user.id, 'delete_message', f"Message ID: {message_id}")
    
    return jsonify({'message': 'Message deleted successfully'})

@bp.route('/search', methods=['GET'])
@require_auth
def search_messages():
    """Search messages - VULNERABLE: Reflected XSS, SQL Injection"""
    user = get_current_user()
    
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    # VULNERABLE: Reflected XSS - query is returned in response without sanitization
    # VULNERABLE: SQL Injection in search
    from sqlalchemy import text
    sql_query = f"SELECT * FROM messages WHERE content LIKE '%{query}%' OR subject LIKE '%{query}%'"
    result = db.session.execute(text(sql_query))
    messages = [dict(row) for row in result]
    
    # VULNERABLE: Returns search query in response (reflected XSS)
    return jsonify({
        'query': query,  # VULNERABLE: Reflected XSS
        'results': messages  # VULNERABLE: XSS in message content
    })

