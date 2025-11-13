# Task management routes with intentional security vulnerabilities
from flask import Blueprint, request, jsonify
from models import Task, Comment, Project, User, db
from auth import require_auth, get_current_user
from utils.logger import log_user_action
from sqlalchemy import text
from datetime import datetime

bp = Blueprint('tasks', __name__)

@bp.route('', methods=['GET'])
@require_auth
def get_tasks():
    """Get all tasks - VULNERABLE: SQL Injection, IDOR, broken access control"""
    user = get_current_user()
    
    # VULNERABLE: SQL Injection in filter parameters
    project_id = request.args.get('project_id')
    status = request.args.get('status', '')
    search = request.args.get('search', '')
    assigned_to = request.args.get('assigned_to')
    
    # VULNERABLE: Raw SQL query with user input (SQL Injection)
    if search:
        # VULNERABLE: Direct string interpolation in SQL
        query = f"SELECT * FROM tasks WHERE title LIKE '%{search}%' OR description LIKE '%{search}%'"
        if project_id:
            query += f" AND project_id = {project_id}"
        result = db.session.execute(text(query))
        tasks = [dict(row) for row in result]
    else:
        # VULNERABLE: Broken access control - users can see all tasks
        query = Task.query
        if project_id:
            query = query.filter_by(project_id=project_id)
        if status:
            query = query.filter_by(status=status)
        if assigned_to:
            query = query.filter_by(assigned_to=assigned_to)
        tasks = query.all()
    
    # VULNERABLE: Exposes all tasks regardless of user permissions
    return jsonify({
        'tasks': [t.to_dict() for t in tasks]
    })

@bp.route('/<int:task_id>', methods=['GET'])
@require_auth
def get_task(task_id):
    """Get task by ID - VULNERABLE: IDOR, broken access control"""
    user = get_current_user()
    
    # VULNERABLE: IDOR - no check if user has access to this task
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # VULNERABLE: Broken access control - allows access to any task
    # Should check project permissions
    
    log_user_action(user.id, 'view_task', f"Task ID: {task_id}")
    
    return jsonify({
        'task': task.to_dict()
    })

@bp.route('', methods=['POST'])
@require_auth
def create_task():
    """Create task - VULNERABLE: No input validation, XSS, broken access control"""
    user = get_current_user()
    data = request.get_json() or request.form
    
    title = data.get('title')
    description = data.get('description', '')
    project_id = data.get('project_id')
    assigned_to = data.get('assigned_to')
    priority = data.get('priority', 'medium')
    due_date = data.get('due_date')
    
    if not title or not project_id:
        return jsonify({'error': 'Title and project_id required'}), 400
    
    # VULNERABLE: No check if user has access to the project
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # VULNERABLE: No input sanitization (XSS in title/description)
    # VULNERABLE: No validation
    
    task = Task(
        title=title,
        description=description,  # VULNERABLE: Stored without sanitization
        project_id=project_id,
        assigned_to=assigned_to,
        created_by=user.id,
        priority=priority
    )
    
    if due_date:
        try:
            task.due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        except:
            pass  # VULNERABLE: Silent failure
    
    db.session.add(task)
    db.session.commit()
    
    log_user_action(user.id, 'create_task', f"Task: {title}")
    
    return jsonify({
        'message': 'Task created successfully',
        'task': task.to_dict()
    }), 201

@bp.route('/<int:task_id>', methods=['PUT'])
@require_auth
def update_task(task_id):
    """Update task - VULNERABLE: Broken access control, IDOR, no input validation"""
    user = get_current_user()
    data = request.get_json() or request.form
    
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # VULNERABLE: Broken access control - any user can modify any task
    # Should check: task.created_by == user.id or user.role in ['admin', 'project_manager']
    
    title = data.get('title')
    description = data.get('description')
    status = data.get('status')
    assigned_to = data.get('assigned_to')
    priority = data.get('priority')
    due_date = data.get('due_date')
    
    if title:
        task.title = title
    if description is not None:
        # VULNERABLE: No input sanitization (XSS)
        task.description = description
    if status:
        task.status = status
    if assigned_to is not None:
        task.assigned_to = assigned_to
    if priority:
        task.priority = priority
    if due_date:
        try:
            task.due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        except:
            pass
    
    db.session.commit()
    
    log_user_action(user.id, 'update_task', f"Task ID: {task_id}")
    
    return jsonify({
        'message': 'Task updated successfully',
        'task': task.to_dict()
    })

@bp.route('/<int:task_id>', methods=['DELETE'])
@require_auth
def delete_task(task_id):
    """Delete task - VULNERABLE: Broken access control, IDOR"""
    user = get_current_user()
    
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # VULNERABLE: Broken access control - any user can delete any task
    # Should check: task.created_by == user.id or user.role == 'admin'
    
    db.session.delete(task)
    db.session.commit()
    
    log_user_action(user.id, 'delete_task', f"Task ID: {task_id}")
    
    return jsonify({'message': 'Task deleted successfully'})

@bp.route('/<int:task_id>/comments', methods=['GET'])
@require_auth
def get_task_comments(task_id):
    """Get task comments - VULNERABLE: IDOR"""
    user = get_current_user()
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # VULNERABLE: IDOR - no access control check
    comments = Comment.query.filter_by(task_id=task_id).all()
    
    return jsonify({
        'comments': [c.to_dict() for c in comments]  # VULNERABLE: XSS in content
    })

@bp.route('/<int:task_id>/comments', methods=['POST'])
@require_auth
def create_task_comment(task_id):
    """Create task comment - VULNERABLE: XSS, no input validation, IDOR"""
    user = get_current_user()
    data = request.get_json() or request.form
    
    content = data.get('content')
    
    if not content:
        return jsonify({'error': 'Comment content required'}), 400
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # VULNERABLE: No input sanitization (XSS)
    # VULNERABLE: IDOR - no access control check
    
    comment = Comment(
        task_id=task_id,
        user_id=user.id,
        content=content  # VULNERABLE: Stored without sanitization
    )
    
    db.session.add(comment)
    db.session.commit()
    
    log_user_action(user.id, 'create_comment', f"Task ID: {task_id}, Content: {content}")
    
    return jsonify({
        'message': 'Comment created successfully',
        'comment': comment.to_dict()
    }), 201

