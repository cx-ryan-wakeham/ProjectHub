# Main Flask application
import sys
import os

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db
from database import init_db

# Import route handlers
from routes import auth, projects, tasks, documents, messages, api
from utils.logger import setup_logger

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

# Register blueprints
app.register_blueprint(auth.bp, url_prefix='/api/auth')
app.register_blueprint(projects.bp, url_prefix='/api/projects')
app.register_blueprint(tasks.bp, url_prefix='/api/tasks')
app.register_blueprint(documents.bp, url_prefix='/api/documents')
app.register_blueprint(messages.bp, url_prefix='/api/messages')
app.register_blueprint(api.bp, url_prefix='/api/v1')

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
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

