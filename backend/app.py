# Main Flask application
import sys
import os

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from config import Config
from models import db, User, Project, Task
from database import init_db

# Import route handlers
from routes import auth, projects, tasks, documents, messages, api
from utils.logger import setup_logger
from utils.request_context import _get_request_id, get_request_context, set_request_metadata, get_request_start_time
from utils.jinja_filters import format_datetime, user_display_name, truncate, md5_hash, request_id_filter, format_file_size, role_badge

app = Flask(__name__)
app.config.from_object(Config)

# Simple CORS configuration that works with Flask-CORS 3.0.7
CORS(app, 
     resources={r"/*": {
         "origins": "*",
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
         "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Accept"],
         "expose_headers": ["Content-Type", "Authorization"],
         "supports_credentials": False
     }})

# Initialize database
db.init_app(app)
init_db(app)

# Setup logging
logger = setup_logger(app)

# Register Jinja2 template filters
app.jinja_env.filters['format_datetime'] = format_datetime
app.jinja_env.filters['user_display_name'] = user_display_name
app.jinja_env.filters['truncate'] = truncate
app.jinja_env.filters['md5_hash'] = md5_hash
app.jinja_env.filters['request_id_filter'] = request_id_filter
app.jinja_env.filters['format_file_size'] = format_file_size
app.jinja_env.filters['role_badge'] = role_badge

# Initialize request context
@app.before_request
def init_request_context():
    """Initialize request context"""
    from flask import _request_ctx_stack
    ctx = _request_ctx_stack.top
    if ctx is not None:
        # Initialize request ID
        _get_request_id()
        # Set request start time
        get_request_start_time()
        # Store request metadata
        set_request_metadata('ip_address', request.remote_addr)
        set_request_metadata('user_agent', request.headers.get('User-Agent', 'Unknown'))
        set_request_metadata('method', request.method)
        set_request_metadata('path', request.path)

# Register blueprints
app.register_blueprint(auth.bp, url_prefix='/api/auth')
app.register_blueprint(projects.bp, url_prefix='/api/projects')
app.register_blueprint(tasks.bp, url_prefix='/api/tasks')
app.register_blueprint(documents.bp, url_prefix='/api/documents')
app.register_blueprint(messages.bp, url_prefix='/api/messages')
app.register_blueprint(api.bp, url_prefix='/api/v1')

# Register analytics routes
from routes import analytics
app.register_blueprint(analytics.bp, url_prefix='/api')

# Create upload directory
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)

@app.route('/')
def index():
    return jsonify({
        'message': 'ProjectHub API',
        'version': '1.0.0',
        'status': 'running'
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    from utils.request_context import get_request_context
    ctx = get_request_context()
    request_id = ctx.request_id if ctx and hasattr(ctx, 'request_id') else 'N/A'
    
    # Support both JSON and HTML responses
    if request.headers.get('Accept', '').startswith('text/html'):
        return render_template('error.html', 
                             error_code=404,
                             error_message='Page Not Found',
                             error_details='The requested resource could not be found.',
                             request_id=request_id), 404
    return jsonify({'error': 'Not found', 'request_id': request_id}), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    db.session.rollback()
    from utils.request_context import get_request_context
    ctx = get_request_context()
    request_id = ctx.request_id if ctx and hasattr(ctx, 'request_id') else 'N/A'
    
    logger.error(f"[{request_id}] Internal error: {str(error)}")
    
    # Support both JSON and HTML responses
    if request.headers.get('Accept', '').startswith('text/html'):
        return render_template('error.html',
                             error_code=500,
                             error_message='Internal Server Error',
                             error_details='An unexpected error occurred. Please try again later.',
                             request_id=request_id), 500
    return jsonify({'error': 'Internal server error', 'request_id': request_id}), 500

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    from utils.request_context import get_request_context
    ctx = get_request_context()
    request_id = ctx.request_id if ctx and hasattr(ctx, 'request_id') else 'N/A'
    
    # Get data
    users = User.query.all()
    projects = Project.query.all()
    tasks = Task.query.all()
    
    return render_template('admin.html',
                         users=users,
                         projects=projects,
                         tasks=tasks,
                         request_id=request_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

