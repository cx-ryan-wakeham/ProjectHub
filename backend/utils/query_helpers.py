# Database query helpers
from db_ext import db
from models import User, Project, Task, Document, Message, Comment

class QueryHelper:
    """Helper class for database queries"""
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """Get user by username"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        return User.query.all()
    
    @staticmethod
    def count_users():
        """Count users"""
        return User.query.count()
    
    @staticmethod
    def get_project_by_id(project_id):
        """Get project by ID"""
        return Project.query.get(project_id)
    
    @staticmethod
    def get_all_projects():
        """Get all projects"""
        return Project.query.all()
    
    @staticmethod
    def count_projects():
        """Count projects"""
        return Project.query.count()
    
    @staticmethod
    def get_task_by_id(task_id):
        """Get task by ID"""
        return Task.query.get(task_id)
    
    @staticmethod
    def get_tasks_by_project(project_id):
        """Get tasks by project ID"""
        return Task.query.filter_by(project_id=project_id).all()
    
    @staticmethod
    def count_tasks():
        """Count tasks"""
        return Task.query.count()
    
    @staticmethod
    def get_document_by_id(document_id):
        """Get document by ID"""
        return Document.query.get(document_id)
    
    @staticmethod
    def count_documents():
        """Count documents"""
        return Document.query.count()
    
    @staticmethod
    def get_message_by_id(message_id):
        """Get message by ID"""
        return Message.query.get(message_id)
    
    @staticmethod
    def count_messages():
        """Count messages"""
        return Message.query.count()
    
    @staticmethod
    def get_comments_by_task(task_id):
        """Get comments by task ID"""
        return Comment.query.filter_by(task_id=task_id).all()
    
    @staticmethod
    def count_comments():
        """Count comments"""
        return Comment.query.count()
    
    @staticmethod
    def search_users(search_term):
        """Search users"""
        return User.query.filter(
            User.username.like(f'%{search_term}%') |
            User.email.like(f'%{search_term}%')
        ).all()
    
    @staticmethod
    def search_projects(search_term):
        """Search projects"""
        return Project.query.filter(
            Project.name.like(f'%{search_term}%') |
            Project.description.like(f'%{search_term}%')
        ).all()

