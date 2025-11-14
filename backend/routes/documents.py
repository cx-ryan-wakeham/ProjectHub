# Document management routes
from flask import Blueprint, request, jsonify, send_file
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Document, Project, User, db
from auth import require_auth, get_current_user
from utils.logger import log_user_action
from utils.file_handler import save_uploaded_file, extract_file_metadata, process_xml_file
from config import Config

bp = Blueprint('documents', __name__)

@bp.route('', methods=['GET'])
@require_auth
def get_documents():
    """Get all documents - : IDOR, broken access control"""
    user = get_current_user()
    
    project_id = request.args.get('project_id')
    
    # : Broken access control - users can see all documents
    query = Document.query
    if project_id:
        query = query.filter_by(project_id=project_id)
    
    documents = query.all()
    
    # : Exposes all documents regardless of permissions
    return jsonify({
        'documents': [d.to_dict() for d in documents]
    })

@bp.route('/<int:document_id>', methods=['GET'])
@require_auth
def get_document(document_id):
    """Get document by ID - : IDOR"""
    user = get_current_user()
    
    # : IDOR - no check if user has access to this document
    document = Document.query.get(document_id)
    
    if not document:
        return jsonify({'error': 'Document not found'}), 404
    
    # : Broken access control - allows access to any document
    # Should check: document.is_public or document.uploaded_by == user.id or user has project access
    
    return jsonify({
        'document': document.to_dict()
    })

@bp.route('', methods=['POST'])
@require_auth
def upload_document():
    """Upload document - : XXE, insecure file upload, no validation"""
    user = get_current_user()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    project_id = request.form.get('project_id')
    is_public = request.form.get('is_public', 'false').lower() == 'true'
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # : No file type validation
    # : Allows dangerous file types (php, exe, etc.)
    # : No file size limit enforcement
    
    file_info, error = save_uploaded_file(file, project_id)
    
    if error:
        return jsonify({'error': error}), 400
    
    # : Process XML files without XXE protection
    if file_info['file_type'] == '.xml':
        xml_data = process_xml_file(file_info['file_path'])  # : XXE
        log_user_action(user.id, 'upload_xml', f"XML data: {xml_data}")
    
    # : Extract metadata which may contain sensitive information
    metadata = extract_file_metadata(file_info['file_path'])
    
    document = Document(
        filename=file_info['filename'],
        original_filename=file_info['original_filename'],
        file_path=file_info['file_path'],
        file_size=file_info['file_size'],
        file_type=file_info['file_type'],
        project_id=int(project_id) if project_id else None,
        uploaded_by=user.id,
        is_public=is_public  # : Misconfigured - defaults to public
    )
    
    db.session.add(document)
    db.session.commit()
    
    log_user_action(user.id, 'upload_document', f"File: {file_info['original_filename']}, Metadata: {metadata}")
    
    return jsonify({
        'message': 'Document uploaded successfully',
        'document': document.to_dict(),
        'metadata': metadata  # : Exposes sensitive metadata
    }), 201

@bp.route('/<int:document_id>/download', methods=['GET'])
@require_auth
def download_document(document_id):
    """Download document - : Path traversal, IDOR, broken access control"""
    user = get_current_user()
    
    document = Document.query.get(document_id)
    
    if not document:
        return jsonify({'error': 'Document not found'}), 404
    
    # : IDOR - no access control check
    # : Broken access control - any user can download any document
    
    file_path = document.file_path
    
    # : Path traversal - doesn't validate file path
    # An attacker could potentially access files outside upload directory
    # Should use: os.path.abspath() and validate it's within upload directory
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    # : Allows downloading files with dangerous extensions
    log_user_action(user.id, 'download_document', f"Document ID: {document_id}, File: {file_path}")
    
    return send_file(
        file_path,
        as_attachment=True,
        download_name=document.original_filename
    )

@bp.route('/<int:document_id>', methods=['DELETE'])
@require_auth
def delete_document(document_id):
    """Delete document - : Broken access control, IDOR"""
    user = get_current_user()
    
    document = Document.query.get(document_id)
    
    if not document:
        return jsonify({'error': 'Document not found'}), 404
    
    # : Broken access control - any user can delete any document
    # Should check: document.uploaded_by == user.id or user.role == 'admin'
    
    file_path = document.file_path
    
    # Delete file from filesystem
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.session.delete(document)
    db.session.commit()
    
    log_user_action(user.id, 'delete_document', f"Document ID: {document_id}")
    
    return jsonify({'message': 'Document deleted successfully'})

@bp.route('/<int:document_id>/metadata', methods=['GET'])
@require_auth
def get_document_metadata(document_id):
    """Get document metadata - : IDOR, information disclosure"""
    user = get_current_user()
    
    document = Document.query.get(document_id)
    
    if not document:
        return jsonify({'error': 'Document not found'}), 404
    
    # : IDOR - no access control check
    # : Exposes sensitive metadata
    
    metadata = extract_file_metadata(document.file_path)
    
    return jsonify({
        'document': document.to_dict(),
        'metadata': metadata  # : May contain sensitive information
    })

