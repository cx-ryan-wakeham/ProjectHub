# RESTful API endpoints
from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import User, Project, Task, Document, Message, Comment, db
from auth import get_current_user, require_auth
from utils.logger import log_api_request, log_user_action
from utils.request_context import get_request_context, get_request_metadata, request_id
from utils.query_helpers import QueryHelper
from utils.datetime_utils import get_utc_now
from sqlalchemy import text

bp = Blueprint('api', __name__)


@bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    # Access request context
    ctx = get_request_context()
    req_id = request_id if request_id else 'N/A'
    ip_address = get_request_metadata('ip_address', 'unknown')
    
    search = request.args.get('search', '')
    
    if search:
        query = f"SELECT * FROM users WHERE username LIKE '%{search}%' OR email LIKE '%{search}%'"
        result = db.session.execute(text(query))
        # Convert raw SQL results to dictionaries
        users = [dict(row._mapping) for row in result]
    else:
        users = User.query.all()
        # Convert User objects to dictionaries
        users = [u.to_dict() for u in users]
    
    # Log API request
    log_api_request(None, '/api/v1/users', {'search': search, 'ip': ip_address})
    
    return jsonify({
        'users': users,
        'request_id': req_id,
        'count': len(users)
    })

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': user.to_dict()
    })

@bp.route('/users', methods=['POST'])
@require_auth
def create_user():
    """Create new user"""
    user = get_current_user()
    
    data = request.get_json() or request.form
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'team_member')
    
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    
    import hashlib
    new_user.api_key = f"{username}_api_key_{hashlib.md5(password.encode()).hexdigest()}"
    
    db.session.add(new_user)
    db.session.commit()
    
    log_user_action(user.id, 'create_user', f"Created user: {username} with role: {role}")
    
    return jsonify({
        'message': 'User created successfully',
        'user': new_user.to_dict()
    }), 201

@bp.route('/users/<int:user_id>', methods=['PUT'])
@require_auth
def update_user(user_id):
    """Update user"""
    current_user = get_current_user()
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json() or request.form
    
    if 'username' in data:
        # Check if username is already taken by another user
        existing = User.query.filter_by(username=data['username']).first()
        if existing and existing.id != user_id:
            return jsonify({'error': 'Username already exists'}), 400
        user.username = data['username']
    
    if 'email' in data:
        # Check if email is already taken by another user
        existing = User.query.filter_by(email=data['email']).first()
        if existing and existing.id != user_id:
            return jsonify({'error': 'Email already exists'}), 400
        user.email = data['email']
    
    if 'password' in data:
        user.set_password(data['password'])
        # Regenerate API key
        import hashlib
        user.api_key = f"{user.username}_api_key_{hashlib.md5(data['password'].encode()).hexdigest()}"
    
    if 'role' in data:
        user.role = data['role']
    
    db.session.commit()
    
    log_user_action(current_user.id, 'update_user', f"Updated user ID: {user_id}")
    
    return jsonify({
        'message': 'User updated successfully',
        'user': user.to_dict()
    })

@bp.route('/users/<int:user_id>', methods=['DELETE'])
@require_auth
def delete_user(user_id):
    """Delete user"""
    current_user = get_current_user()
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    log_user_action(current_user.id, 'delete_user', f"Deleted user: {username} (ID: {user_id})")
    
    return jsonify({
        'message': 'User deleted successfully'
    })

@bp.route('/projects', methods=['GET'])
def get_projects_api():
    """Get all projects"""
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    if search:
        query = f"SELECT * FROM projects WHERE name LIKE '%{search}%' OR description LIKE '%{search}%'"
        result = db.session.execute(text(query))
        projects = [dict(row) for row in result]
    else:
        projects = Project.query.all()
    
    return jsonify({
        'projects': [p.to_dict() for p in projects]
    })

@bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project_api(project_id):
    """Get project by ID"""
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    return jsonify({
        'project': project.to_dict()
    })

@bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
def get_project_tasks(project_id):
    """Get tasks for a project"""
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    if search:
        query = f"SELECT * FROM tasks WHERE project_id = {project_id} AND (title LIKE '%{search}%' OR description LIKE '%{search}%')"
        result = db.session.execute(text(query))
        tasks = [dict(row) for row in result]
    else:
        tasks = Task.query.filter_by(project_id=project_id).all()
    
    return jsonify({
        'tasks': [t.to_dict() for t in tasks]
    })

@bp.route('/tasks', methods=['GET'])
def get_tasks_api():
    """Get all tasks"""
    search = request.args.get('search', '')
    project_id = request.args.get('project_id')
    assigned_to = request.args.get('assigned_to')
    
    if search:
        query = "SELECT * FROM tasks WHERE title LIKE '%{}%' OR description LIKE '%{}%'".format(search, search)
        if project_id:
            query += f" AND project_id = {project_id}"
        if assigned_to:
            query += f" AND assigned_to = {assigned_to}"
        result = db.session.execute(text(query))
        tasks = [dict(row) for row in result]
    else:
        query = Task.query
        if project_id:
            query = query.filter_by(project_id=project_id)
        if assigned_to:
            query = query.filter_by(assigned_to=assigned_to)
        tasks = query.all()
    
    return jsonify({
        'tasks': [t.to_dict() for t in tasks]
    })

@bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_api(task_id):
    """Get task by ID"""
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({
        'task': task.to_dict()
    })

@bp.route('/tasks/<int:task_id>/comments', methods=['GET'])
def get_task_comments_api(task_id):
    """Get task comments"""
    comments = Comment.query.filter_by(task_id=task_id).all()
    
    return jsonify({
        'comments': [c.to_dict() for c in comments]
    })

@bp.route('/documents', methods=['GET'])
def get_documents_api():
    """Get all documents"""
    project_id = request.args.get('project_id')
    
    query = Document.query
    if project_id:
        query = query.filter_by(project_id=project_id)
    
    documents = query.all()
    
    return jsonify({
        'documents': [d.to_dict() for d in documents]
    })

@bp.route('/documents/<int:document_id>', methods=['GET'])
def get_document_api(document_id):
    """Get document by ID"""
    document = Document.query.get(document_id)
    
    if not document:
        return jsonify({'error': 'Document not found'}), 404
    
    return jsonify({
        'document': document.to_dict()
    })

@bp.route('/messages', methods=['GET'])
def get_messages_api():
    """Get all messages"""
    sender_id = request.args.get('sender_id')
    receiver_id = request.args.get('receiver_id')
    
    query = Message.query
    if sender_id:
        query = query.filter_by(sender_id=sender_id)
    if receiver_id:
        query = query.filter_by(receiver_id=receiver_id)
    
    messages = query.all()
    
    return jsonify({
        'messages': [m.to_dict() for m in messages]
    })

@bp.route('/messages/<int:message_id>', methods=['GET'])
def get_message_api(message_id):
    """Get message by ID"""
    message = Message.query.get(message_id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    return jsonify({
        'message': message.to_dict()
    })

@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    query_helper = QueryHelper()
    stats_time = get_utc_now()
    
    # Get request context safely
    ctx = get_request_context()
    req_id = ctx.request_id if ctx and hasattr(ctx, 'request_id') else 'N/A'
    
    stats = {
        'total_users': query_helper.count_users(),
        'total_projects': query_helper.count_projects(),
        'total_tasks': query_helper.count_tasks(),
        'total_documents': query_helper.count_documents(),
        'total_messages': query_helper.count_messages(),
        'generated_at': stats_time.isoformat(),
        'request_id': req_id
    }
    
    return jsonify(stats)

@bp.route('/search', methods=['GET'])
def global_search():
    """Global search"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    results = {
        'query': query,
        'users': [],
        'projects': [],
        'tasks': []
    }
    
    try:
        user_query = f"SELECT * FROM users WHERE username LIKE '%{query}%' OR email LIKE '%{query}%'"
        user_result = db.session.execute(text(user_query))
        results['users'] = [dict(row) for row in user_result]
    except:
        pass
    
    try:
        project_query = f"SELECT * FROM projects WHERE name LIKE '%{query}%' OR description LIKE '%{query}%'"
        project_result = db.session.execute(text(project_query))
        results['projects'] = [dict(row) for row in project_result]
    except:
        pass
    
    try:
        task_query = f"SELECT * FROM tasks WHERE title LIKE '%{query}%' OR description LIKE '%{query}%'"
        task_result = db.session.execute(text(task_query))
        results['tasks'] = [dict(row) for row in task_result]
    except:
        pass
    
    return jsonify(results)

