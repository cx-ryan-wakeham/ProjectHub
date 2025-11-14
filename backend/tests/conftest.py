import pytest
import sys
import os

# Add backend directory to path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from db_ext import db
from models import User, Project, Task, Message, Comment
from datetime import datetime, timedelta

# Import app after setting up path
from app import app as flask_app


@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(app):
    """Create a test user and return authorization headers"""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@projecthub.com',
            role='admin'
        )
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        
        from auth import generate_token
        token = generate_token(user.id, user.username)
        
        return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def sample_data(app):
    """Create sample data for testing analytics"""
    with app.app_context():
        user1 = User(username='user1', email='user1@test.com', role='admin')
        user1.set_password('pass1')
        user2 = User(username='user2', email='user2@test.com', role='team_member')
        user2.set_password('pass2')
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        project1 = Project(
            name='Project A',
            description='Test project A',
            owner_id=user1.id
        )
        project2 = Project(
            name='Project B',
            description='Test project B',
            owner_id=user1.id
        )
        
        db.session.add(project1)
        db.session.add(project2)
        db.session.commit()
        
        base_time = datetime.utcnow() - timedelta(days=10)
        
        task1 = Task(
            title='Task 1',
            description='Test task 1',
            project_id=project1.id,
            assigned_to=user1.id,
            created_by=user1.id,
            status='completed',
            priority='high',
            created_at=base_time,
            updated_at=base_time + timedelta(days=2)
        )
        
        task2 = Task(
            title='Task 2',
            description='Test task 2',
            project_id=project1.id,
            assigned_to=user2.id,
            created_by=user1.id,
            status='in_progress',
            priority='medium',
            created_at=base_time + timedelta(days=1)
        )
        
        task3 = Task(
            title='Task 3',
            description='Test task 3',
            project_id=project2.id,
            assigned_to=user1.id,
            created_by=user1.id,
            status='pending',
            priority='low',
            created_at=base_time + timedelta(days=2)
        )
        
        task4 = Task(
            title='Task 4',
            description='Test task 4',
            project_id=project1.id,
            assigned_to=user1.id,
            created_by=user1.id,
            status='completed',
            priority='high',
            created_at=base_time + timedelta(days=3),
            updated_at=base_time + timedelta(days=5)
        )
        
        db.session.add(task1)
        db.session.add(task2)
        db.session.add(task3)
        db.session.add(task4)
        db.session.commit()
        
        comment1 = Comment(
            task_id=task1.id,
            user_id=user1.id,
            content='Comment 1'
        )
        comment2 = Comment(
            task_id=task1.id,
            user_id=user2.id,
            content='Comment 2'
        )
        
        db.session.add(comment1)
        db.session.add(comment2)
        
        message1 = Message(
            sender_id=user1.id,
            receiver_id=user2.id,
            subject='Test message 1',
            content='Message content 1',
            created_at=base_time
        )
        message2 = Message(
            sender_id=user2.id,
            receiver_id=user1.id,
            subject='Test message 2',
            content='Message content 2',
            created_at=base_time + timedelta(days=1)
        )
        message3 = Message(
            sender_id=user1.id,
            receiver_id=user2.id,
            subject='Test message 3',
            content='Message content 3',
            created_at=base_time + timedelta(days=2)
        )
        
        db.session.add(message1)
        db.session.add(message2)
        db.session.add(message3)
        db.session.commit()
        
        return {
            'users': [user1, user2],
            'projects': [project1, project2],
            'tasks': [task1, task2, task3, task4],
            'messages': [message1, message2, message3]
        }

