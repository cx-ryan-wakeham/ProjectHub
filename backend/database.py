# Database initialization and connection setup
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Project, Task, Document, Message, Comment, Notification
from config import Config
import hashlib

def init_db(app):
    """Initialize database and create tables"""
    with app.app_context():
        db.create_all()
        
        # Create default admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email=Config.ADMIN_EMAIL,
                role='admin'
            )
            admin.set_password(Config.ADMIN_PASSWORD)
            admin.api_key = "admin_api_key_12345"  # VULNERABLE: Hardcoded API key
            db.session.add(admin)
            db.session.commit()
            print(f"Created admin user: {Config.ADMIN_EMAIL} / {Config.ADMIN_PASSWORD}")

