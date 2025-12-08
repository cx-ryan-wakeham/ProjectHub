"""
Pytest configuration and fixtures for testing
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_cors import CORS
from models import db, User, Project, Task, Document, Message
from config import Config


class TestConfig(Config):
    """Test configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    # Test secret key - not used in production
    # checkmarx-ignore: Hardcoded Tokens
    JWT_SECRET_KEY = 'test-secret-key-for-unit-testing-only'
    UPLOAD_FOLDER = '/tmp/test_uploads'
    LOG_FILE = '/tmp/test_logs/app.log'


@pytest.fixture(scope='function')
def app():
    """Create and configure a test app instance"""
    test_app = Flask(__name__)
    test_app.config.from_object(TestConfig)
    
    # Simple CORS configuration
    CORS(test_app)
    
    # Initialize database
    db.init_app(test_app)
    
    # Import and register blueprints
    from routes import auth, projects, tasks, documents, messages, api, analytics
    test_app.register_blueprint(auth.bp, url_prefix='/api/auth')
    test_app.register_blueprint(projects.bp, url_prefix='/api/projects')
    test_app.register_blueprint(tasks.bp, url_prefix='/api/tasks')
    test_app.register_blueprint(documents.bp, url_prefix='/api/documents')
    test_app.register_blueprint(messages.bp, url_prefix='/api/messages')
    test_app.register_blueprint(api.bp, url_prefix='/api/v1')
    test_app.register_blueprint(analytics.bp, url_prefix='/api')
    
    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create a test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def db_session(app):
    """Create a database session for testing"""
    with app.app_context():
        yield db.session


@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing"""
    user = User(
        username='testuser',
        email='test@example.com',
        role='team_member'
    )
    user.set_password('password123')
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def admin_user(db_session):
    """Create an admin user for testing"""
    user = User(
        username='admin',
        email='admin@example.com',
        role='admin'
    )
    user.set_password('admin123')
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def sample_project(db_session, sample_user):
    """Create a sample project for testing"""
    project = Project(
        name='Test Project',
        description='A test project',
        owner_id=sample_user.id,
        is_public=False
    )
    db_session.add(project)
    db_session.commit()
    return project


@pytest.fixture
def sample_task(db_session, sample_project, sample_user):
    """Create a sample task for testing"""
    task = Task(
        title='Test Task',
        description='A test task',
        project_id=sample_project.id,
        created_by=sample_user.id,
        status='pending',
        priority='medium'
    )
    db_session.add(task)
    db_session.commit()
    return task


@pytest.fixture
def auth_headers(app, sample_user):
    """Get authentication headers for testing"""
    with app.app_context():
        from auth import generate_token
        token = generate_token(sample_user.id, sample_user.username)
        return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def admin_auth_headers(app, admin_user):
    """Get admin authentication headers for testing"""
    with app.app_context():
        from auth import generate_token
        token = generate_token(admin_user.id, admin_user.username)
        return {'Authorization': f'Bearer {token}'}

