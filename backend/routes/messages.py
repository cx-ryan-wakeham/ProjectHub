# Messaging routes
from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_ext import db
from models import Message, User
from auth import require_auth, get_current_user
from utils.logger import log_user_action
from datetime import datetime

bp = Blueprint('messages', __name__)

@bp.route('', methods=['GET'])
@require_auth
def get_messages():
    """Get messages"""
    user = get_current_user()
    
    sender_id = request.args.get('sender_id')
    receiver_id = request.args.get('receiver_id')
    
    query = Message.query
    
    if sender_id:
        query = query.filter_by(sender_id=sender_id)
    if receiver_id:
        query = query.filter_by(receiver_id=receiver_id)
    
    messages = query.order_by(Message.created_at.desc()).all()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    total = len(messages)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_messages = messages[start:end]
    
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
    """Get message by ID"""
    user = get_current_user()
    
    message = Message.query.get(message_id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    if message.receiver_id == user.id:
        message.is_read = True
        db.session.commit()
    
    return jsonify({
        'message': message.to_dict()
    })

@bp.route('', methods=['POST'])
@require_auth
def send_message():
    """Send message"""
    user = get_current_user()
    data = request.get_json() or request.form
    
    receiver_id = data.get('receiver_id')
    subject = data.get('subject', '')
    content = data.get('content')
    
    if not receiver_id or not content:
        return jsonify({'error': 'Receiver ID and content required'}), 400
    
    receiver = User.query.get(receiver_id)
    if not receiver:
        return jsonify({'error': 'Receiver not found'}), 404
    
    message = Message(
        sender_id=user.id,
        receiver_id=receiver_id,
        subject=subject,
        content=content
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
    """Delete message"""
    user = get_current_user()
    
    message = Message.query.get(message_id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    db.session.delete(message)
    db.session.commit()
    
    log_user_action(user.id, 'delete_message', f"Message ID: {message_id}")
    
    return jsonify({'message': 'Message deleted successfully'})

@bp.route('/search', methods=['GET'])
@require_auth
def search_messages():
    """Search messages"""
    user = get_current_user()
    
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    from sqlalchemy import text
    sql_query = f"SELECT * FROM messages WHERE content LIKE '%{query}%' OR subject LIKE '%{query}%'"
    result = db.session.execute(text(sql_query))
    messages = [dict(row) for row in result]
    
    return jsonify({
        'query': query,
        'results': messages
    })

