# Notification routes (separate from messages for organization)
from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Notification, User, db
from auth import require_auth, get_current_user
from utils.logger import log_user_action

bp = Blueprint('notifications', __name__)

@bp.route('', methods=['GET'])
@require_auth
def get_notifications():
    """Get notifications - VULNERABLE: XSS in notification messages"""
    user = get_current_user()
    
    is_read = request.args.get('is_read')
    
    query = Notification.query.filter_by(user_id=user.id)
    
    if is_read is not None:
        query = query.filter_by(is_read=is_read.lower() == 'true')
    
    notifications = query.order_by(Notification.created_at.desc()).all()
    
    # VULNERABLE: XSS in message - no sanitization
    return jsonify({
        'notifications': [n.to_dict() for n in notifications]
    })

@bp.route('/<int:notification_id>', methods=['GET'])
@require_auth
def get_notification(notification_id):
    """Get notification by ID - VULNERABLE: IDOR"""
    user = get_current_user()
    
    notification = Notification.query.get(notification_id)
    
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    
    # VULNERABLE: IDOR - no check if notification belongs to user
    # Should check: notification.user_id == user.id
    
    return jsonify({
        'notification': notification.to_dict()  # VULNERABLE: XSS in message
    })

