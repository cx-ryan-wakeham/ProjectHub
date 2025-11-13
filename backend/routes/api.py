# RESTful API endpoints with intentional security vulnerabilities
from flask import Blueprint, request, jsonify
from models import User, Project, Task, Document, Message, Comment, Notification, db
from auth import get_current_user, require_auth
from utils.logger import log_api_request, log_user_action
from sqlalchemy import text

bp = Blueprint('api', __name__)

# VULNERABLE: Some endpoints don't require authentication
# VULNERABLE: SQL Injection in filter parameters
# VULNERABLE: IDOR in all endpoints
# VULNERABLE: Sensitive data exposure in responses

@bp.route('/users', methods=['GET'])
def get_users():
    """Get all users - VULNERABLE: No authentication, sensitive data exposure"""
    # VULNERABLE: No authentication required
    # VULNERABLE: Exposes sensitive user data
    
    search = request.args.get('search', '')
    
    if search:
        # VULNERABLE: SQL Injection
        query = f"SELECT * FROM users WHERE username LIKE '%{search}%' OR email LIKE '%{search}%'"
        result = db.session.execute(text(query))
        users = [dict(row) for row in result]
    else:
        users = User.query.all()
    
    # VULNERABLE: Exposes password hashes and API keys
    return jsonify({
        'users': [u.to_dict() for u in users]
    })

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID - VULNERABLE: No authentication, IDOR, sensitive data exposure"""
    # VULNERABLE: No authentication required
    # VULNERABLE: IDOR - can access any user's data
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # VULNERABLE: Exposes sensitive data
    return jsonify({
        'user': user.to_dict()
    })

@bp.route('/projects', methods=['GET'])
def get_projects_api():
    """Get all projects - VULNERABLE: No authentication, SQL Injection"""
    # VULNERABLE: No authentication required
    
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    if search:
        # VULNERABLE: SQL Injection
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
    """Get project by ID - VULNERABLE: No authentication, IDOR"""
    # VULNERABLE: No authentication required
    # VULNERABLE: IDOR
    
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    return jsonify({
        'project': project.to_dict()
    })

@bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
def get_project_tasks(project_id):
    """Get tasks for a project - VULNERABLE: No authentication, IDOR, SQL Injection"""
    # VULNERABLE: No authentication required
    # VULNERABLE: IDOR
    
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    if search:
        # VULNERABLE: SQL Injection
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
    """Get all tasks - VULNERABLE: No authentication, SQL Injection"""
    # VULNERABLE: No authentication required
    
    search = request.args.get('search', '')
    project_id = request.args.get('project_id')
    assigned_to = request.args.get('assigned_to')
    
    if search:
        # VULNERABLE: SQL Injection
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
    """Get task by ID - VULNERABLE: No authentication, IDOR"""
    # VULNERABLE: No authentication required
    # VULNERABLE: IDOR
    
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({
        'task': task.to_dict()
    })

@bp.route('/tasks/<int:task_id>/comments', methods=['GET'])
def get_task_comments_api(task_id):
    """Get task comments - VULNERABLE: No authentication, IDOR, XSS"""
    # VULNERABLE: No authentication required
    # VULNERABLE: IDOR
    
    comments = Comment.query.filter_by(task_id=task_id).all()
    
    # VULNERABLE: XSS in content
    return jsonify({
        'comments': [c.to_dict() for c in comments]
    })

@bp.route('/documents', methods=['GET'])
def get_documents_api():
    """Get all documents - VULNERABLE: No authentication, IDOR"""
    # VULNERABLE: No authentication required
    
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
    """Get document by ID - VULNERABLE: No authentication, IDOR"""
    # VULNERABLE: No authentication required
    # VULNERABLE: IDOR
    
    document = Document.query.get(document_id)
    
    if not document:
        return jsonify({'error': 'Document not found'}), 404
    
    return jsonify({
        'document': document.to_dict()
    })

@bp.route('/messages', methods=['GET'])
def get_messages_api():
    """Get all messages - VULNERABLE: No authentication, IDOR, XSS"""
    # VULNERABLE: No authentication required
    # VULNERABLE: IDOR - can see all messages
    
    sender_id = request.args.get('sender_id')
    receiver_id = request.args.get('receiver_id')
    
    query = Message.query
    if sender_id:
        query = query.filter_by(sender_id=sender_id)
    if receiver_id:
        query = query.filter_by(receiver_id=receiver_id)
    
    messages = query.all()
    
    # VULNERABLE: XSS in content
    return jsonify({
        'messages': [m.to_dict() for m in messages]
    })

@bp.route('/messages/<int:message_id>', methods=['GET'])
def get_message_api(message_id):
    """Get message by ID - VULNERABLE: No authentication, IDOR, XSS"""
    # VULNERABLE: No authentication required
    # VULNERABLE: IDOR
    
    message = Message.query.get(message_id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    # VULNERABLE: XSS in content
    return jsonify({
        'message': message.to_dict()
    })

@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get application statistics - VULNERABLE: No authentication, information disclosure"""
    # VULNERABLE: No authentication required
    # VULNERABLE: Information disclosure
    
    stats = {
        'total_users': User.query.count(),
        'total_projects': Project.query.count(),
        'total_tasks': Task.query.count(),
        'total_documents': Document.query.count(),
        'total_messages': Message.query.count(),
        # VULNERABLE: Exposes internal statistics
    }
    
    return jsonify(stats)

@bp.route('/search', methods=['GET'])
def global_search():
    """Global search - VULNERABLE: No authentication, SQL Injection, Reflected XSS"""
    # VULNERABLE: No authentication required
    
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    # VULNERABLE: Reflected XSS - query returned in response
    # VULNERABLE: SQL Injection
    results = {
        'query': query,  # VULNERABLE: Reflected XSS
        'users': [],
        'projects': [],
        'tasks': []
    }
    
    # VULNERABLE: SQL Injection in search
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

