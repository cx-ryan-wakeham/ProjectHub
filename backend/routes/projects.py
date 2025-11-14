# Project management routes
from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Project, User, db
from auth import require_auth, get_current_user
from utils.logger import log_user_action
from sqlalchemy import text

bp = Blueprint('projects', __name__)

@bp.route('', methods=['GET'])
@require_auth
def get_projects():
    """Get all projects"""
    user = get_current_user()
    
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    
    if search:
        query = f"SELECT * FROM projects WHERE name LIKE '%{search}%' OR description LIKE '%{search}%'"
        result = db.session.execute(text(query))
        projects = [dict(row) for row in result]
    else:
        projects = Project.query.all()
    
    return jsonify({
        'projects': [p.to_dict() for p in projects]
    })

@bp.route('/<int:project_id>', methods=['GET'])
@require_auth
def get_project(project_id):
    """Get project by ID"""
    user = get_current_user()
    
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    log_user_action(user.id, 'view_project', f"Project ID: {project_id}")
    
    return jsonify({
        'project': project.to_dict()
    })

@bp.route('', methods=['POST'])
@require_auth
def create_project():
    """Create project"""
    user = get_current_user()
    data = request.get_json() or request.form
    
    name = data.get('name')
    description = data.get('description', '')
    is_public = data.get('is_public', False)
    
    if not name:
        return jsonify({'error': 'Project name required'}), 400
    
    project = Project(
        name=name,
        description=description,
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
    """Update project"""
    user = get_current_user()
    data = request.get_json() or request.form
    
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    name = data.get('name')
    description = data.get('description')
    is_public = data.get('is_public')
    
    if name:
        project.name = name
    if description is not None:
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
    """Delete project"""
    user = get_current_user()
    
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    db.session.delete(project)
    db.session.commit()
    
    log_user_action(user.id, 'delete_project', f"Project ID: {project_id}")
    
    return jsonify({'message': 'Project deleted successfully'})

@bp.route('/<int:project_id>/dashboard', methods=['GET'])
@require_auth
def get_project_dashboard(project_id):
    """Get project dashboard"""
    user = get_current_user()
    
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    from models import Task, Document
    
    tasks = Task.query.filter_by(project_id=project_id).all()
    documents = Document.query.filter_by(project_id=project_id).all()
    
    return jsonify({
        'project': project.to_dict(),
        'tasks': [t.to_dict() for t in tasks],
        'documents': [d.to_dict() for d in documents],
        'stats': {
            'total_tasks': len(tasks),
            'total_documents': len(documents)
        }
    })

