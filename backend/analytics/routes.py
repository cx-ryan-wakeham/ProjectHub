from flask import jsonify, request
from analytics import bp
from analytics.service import AnalyticsService
from auth import require_auth


@bp.route('/tasks/by-status', methods=['GET'])
@require_auth
def get_tasks_by_status():
    """Get task counts grouped by status"""
    try:
        data = AnalyticsService.get_tasks_by_status()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/tasks/average-completion-time', methods=['GET'])
@require_auth
def get_average_completion_time():
    """Get average time to complete tasks"""
    try:
        data = AnalyticsService.get_average_completion_time()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/projects/summary', methods=['GET'])
@require_auth
def get_projects_summary():
    """Get summary of all projects with task counts"""
    try:
        data = AnalyticsService.get_projects_summary()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/users/<int:user_id>/productivity', methods=['GET'])
@require_auth
def get_user_productivity(user_id):
    """Get productivity metrics for a specific user"""
    try:
        data = AnalyticsService.get_user_productivity(user_id)
        if data is None:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/tasks/by-priority', methods=['GET'])
@require_auth
def get_tasks_by_priority():
    """Get task distribution and metrics by priority level"""
    try:
        data = AnalyticsService.get_tasks_by_priority()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/projects/<int:project_id>/timeline', methods=['GET'])
@require_auth
def get_project_timeline(project_id):
    """Get timeline of tasks for a specific project"""
    try:
        data = AnalyticsService.get_project_timeline(project_id)
        if data is None:
            return jsonify({
                'success': False,
                'error': 'Project not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/messaging/activity', methods=['GET'])
@require_auth
def get_messaging_activity():
    """Get messaging activity over time"""
    try:
        data = AnalyticsService.get_messaging_activity()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

