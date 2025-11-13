# Project management routes with intentional security vulnerabilities
from flask import Blueprint, request, jsonify
from models import Project, User, db
from auth import require_auth, get_current_user
from utils.logger import log_user_action
from sqlalchemy import text  # VULNERABLE: For raw SQL queries

bp = Blueprint('projects', __name__)

@bp.route('', methods=['GET'])
@require_auth
def get_projects():
    """Get all projects - VULNERABLE: SQL Injection, IDOR, broken access control"""
    user = get_current_user()
    
    # VULNERABLE: SQL Injection in search parameter
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    
    # VULNERABLE: Raw SQL query with user input (SQL Injection)
    if search:
        # VULNERABLE: Direct string interpolation in SQL
        query = f"SELECT * FROM projects WHERE name LIKE '%{search}%' OR description LIKE '%{search}%'"
        result = db.session.execute(text(query))
        projects = [dict(row) for row in result]
    else:
        # VULNERABLE: Broken access control - users can see all projects
        # Should filter by user's projects or role
        projects = Project.query.all()
    
    # VULNERABLE: Exposes all projects regardless of ownership
    return jsonify({
        'projects': [p.to_dict() for p in projects]
    })

@bp.route('/<int:project_id>', methods=['GET'])
@require_auth
def get_project(project_id):
    """Get project by ID - VULNERABLE: IDOR, broken access control"""
    user = get_current_user()
    
    # VULNERABLE: IDOR - no check if user has access to this project
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # VULNERABLE: Broken access control - allows access to private projects
    # Should check: project.owner_id == user.id or project.is_public or user.role == 'admin'
    
    log_user_action(user.id, 'view_project', f"Project ID: {project_id}")
    
    return jsonify({
        'project': project.to_dict()
    })

@bp.route('', methods=['POST'])
@require_auth
def create_project():
    """Create project - VULNERABLE: No input validation, XSS"""
    user = get_current_user()
    data = request.get_json() or request.form
    
    name = data.get('name')
    description = data.get('description', '')
    is_public = data.get('is_public', False)
    
    if not name:
        return jsonify({'error': 'Project name required'}), 400
    
    # VULNERABLE: No input sanitization (XSS in description)
    # VULNERABLE: No validation of name/description length
    
    project = Project(
        name=name,
        description=description,  # VULNERABLE: Stored without sanitization
        owner_id=user.id,
        is_public=is_public
    )
    
    db.session.add(project)
    db.session.commit()
    
    log_user_action(user.id, 'create_project', f"Project: {name}")
    
    return jsonify({
        'message': 'Project created successfully',
        'project': project.to_dict()
    }), 201

@bp.route('/<int:project_id>', methods=['PUT'])
@require_auth
def update_project(project_id):
    """Update project - VULNERABLE: Broken access control, IDOR, no input validation"""
    user = get_current_user()
    data = request.get_json() or request.form
    
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # VULNERABLE: Broken access control - non-owners can modify projects
    # Should check: project.owner_id == user.id or user.role == 'admin'
    # Currently allows any authenticated user to modify any project
    
    name = data.get('name')
    description = data.get('description')
    is_public = data.get('is_public')
    
    if name:
        project.name = name
    if description is not None:
        # VULNERABLE: No input sanitization (XSS)
        project.description = description
    if is_public is not None:
        project.is_public = is_public
    
    db.session.commit()
    
    log_user_action(user.id, 'update_project', f"Project ID: {project_id}")
    
    return jsonify({
        'message': 'Project updated successfully',
        'project': project.to_dict()
    })

@bp.route('/<int:project_id>', methods=['DELETE'])
@require_auth
def delete_project(project_id):
    """Delete project - VULNERABLE: Broken access control, IDOR"""
    user = get_current_user()
    
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # VULNERABLE: Broken access control - non-owners can delete projects
    # Should check: project.owner_id == user.id or user.role == 'admin'
    # Currently allows any authenticated user to delete any project
    
    db.session.delete(project)
    db.session.commit()
    
    log_user_action(user.id, 'delete_project', f"Project ID: {project_id}")
    
    return jsonify({'message': 'Project deleted successfully'})

@bp.route('/<int:project_id>/dashboard', methods=['GET'])
@require_auth
def get_project_dashboard(project_id):
    """Get project dashboard - VULNERABLE: IDOR, broken access control, sensitive data exposure"""
    user = get_current_user()
    
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # VULNERABLE: IDOR - no access control check
    # VULNERABLE: Exposes sensitive project data to unauthorized users
    
    from models import Task, Document
    
    tasks = Task.query.filter_by(project_id=project_id).all()
    documents = Document.query.filter_by(project_id=project_id).all()
    
    # VULNERABLE: Exposes all tasks and documents regardless of user permissions
    return jsonify({
        'project': project.to_dict(),
        'tasks': [t.to_dict() for t in tasks],
        'documents': [d.to_dict() for d in documents],
        'stats': {
            'total_tasks': len(tasks),
            'total_documents': len(documents)
        }
    })

