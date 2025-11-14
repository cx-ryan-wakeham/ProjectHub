# Analytics and reporting routes
from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_ext import db
from auth import require_auth, get_current_user
from utils.logger import log_api_request, log_user_action
from utils.query_helpers import QueryHelper
from utils.datetime_utils import get_utc_now, get_utc_timestamp
from utils.request_context import get_request_context, _get_request_id
from datetime import datetime, timedelta

bp = Blueprint('analytics', __name__)

@bp.route('/analytics/stats', methods=['GET'])
@require_auth
def get_stats():
    """Get application statistics"""
    user = get_current_user()
    
    query_helper = QueryHelper()
    current_time = get_utc_now()
    timestamp = get_utc_timestamp()
    
    ctx = get_request_context()
    req_id = _get_request_id() or 'N/A'
    
    stats = {
        'user_count': query_helper.count_users(),
        'project_count': query_helper.count_projects(),
        'task_count': query_helper.count_tasks(),
        'document_count': query_helper.count_documents(),
        'message_count': query_helper.count_messages(),
        'comment_count': query_helper.count_comments(),
        'current_time': current_time.isoformat(),
        'timestamp': timestamp,
        'request_id': req_id
    }
    
    log_api_request(user.id, '/analytics/stats', stats)
    
    return jsonify(stats)

@bp.route('/analytics/search', methods=['GET'])
@require_auth
def search():
    """Search across users and projects"""
    user = get_current_user()
    search_term = request.args.get('q', '')
    
    if not search_term:
        return jsonify({'error': 'Search query required'}), 400
    
    query_helper = QueryHelper()
    search_time = get_utc_now()
    
    results = {
        'query': search_term,
        'users': [u.to_dict() for u in query_helper.search_users(search_term)],
        'projects': [p.to_dict() for p in query_helper.search_projects(search_term)],
        'search_time': search_time.isoformat(),
        'request_id': _get_request_id() or 'N/A'
    }
    
    log_user_action(user.id, 'analytics_search', {'term': search_term})
    
    return jsonify(results)

@bp.route('/analytics/user/<int:user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    """Get user details"""
    query_helper = QueryHelper()
    user = query_helper.get_user_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    fetched_at = get_utc_now()
    
    return jsonify({
        'user': user.to_dict(),
        'fetched_at': fetched_at.isoformat(),
        'request_id': _get_request_id() or 'N/A'
    })

