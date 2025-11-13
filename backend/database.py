# Database initialization and connection setup
from models import db, User, Project, Task, Document, Message, Comment, Notification
from config import Config
import hashlib
import os
from datetime import datetime, timedelta
import random

def seed_data(app):
    """Populate database with test/dummy data"""
    with app.app_context():
        # Check environment variable to skip seeding
        if os.environ.get('SKIP_SEED', 'false').lower() == 'true':
            print("Skipping seed data (SKIP_SEED=true)")
            return
        
        # Check if data already exists
        if Project.query.count() > 0:
            print("Database already has data, skipping seed...")
            return
        
        print("Seeding database with test data...")
        
        # Get admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Warning: Admin user not found, cannot seed data")
            return
        
        # Create additional test users
        test_users = []
        user_data = [
            {'username': 'alice', 'email': 'alice@projecthub.com', 'role': 'project_manager'},
            {'username': 'bob', 'email': 'bob@projecthub.com', 'role': 'team_member'},
            {'username': 'charlie', 'email': 'charlie@projecthub.com', 'role': 'team_member'},
            {'username': 'diana', 'email': 'diana@projecthub.com', 'role': 'team_member'},
            {'username': 'eve', 'email': 'eve@projecthub.com', 'role': 'project_manager'},
        ]
        
        for user_info in user_data:
            user = User.query.filter_by(username=user_info['username']).first()
            if not user:
                user = User(
                    username=user_info['username'],
                    email=user_info['email'],
                    role=user_info['role']
                )
                user.set_password('password123')
                user.api_key = f"{user_info['username']}_api_key_{hashlib.md5('password123'.encode()).hexdigest()}"
                db.session.add(user)
                test_users.append(user)
        
        db.session.commit()
        all_users = [admin] + test_users
        print(f"Created {len(test_users)} test users")
        
        # Create projects
        projects = []
        project_data = [
            {
                'name': 'Website Redesign',
                'description': 'Complete redesign of the company website with modern UI/UX. Includes responsive design, improved accessibility, and performance optimization.',
                'is_public': True
            },
            {
                'name': 'Mobile App Development',
                'description': 'Development of a new mobile application for iOS and Android platforms. Features include user authentication, real-time notifications, and offline support.',
                'is_public': False
            },
            {
                'name': 'Security Audit',
                'description': 'Comprehensive security audit of all systems and applications. Includes penetration testing, vulnerability assessment, and compliance review.',
                'is_public': False
            },
            {
                'name': 'API Integration',
                'description': 'Integration with third-party APIs for payment processing, email services, and analytics. Includes error handling and retry logic.',
                'is_public': True
            },
            {
                'name': 'Database Migration',
                'description': 'Migration from legacy database system to new PostgreSQL database. Includes data validation, backup procedures, and rollback plans.',
                'is_public': False
            },
            {
                'name': 'Documentation Portal',
                'description': 'Create a centralized documentation portal for all project documentation, API references, and user guides.',
                'is_public': True
            }
        ]
        
        for i, proj_data in enumerate(project_data):
            project = Project(
                name=proj_data['name'],
                description=proj_data['description'],
                owner_id=all_users[i % len(all_users)].id,
                is_public=proj_data['is_public'],
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.session.add(project)
            projects.append(project)
        
        db.session.commit()
        print(f"Created {len(projects)} projects")
        
        # Create tasks
        task_templates = [
            ('Design mockups', 'Create initial design mockups for review by stakeholders', 'pending', 'high'),
            ('Setup development environment', 'Configure local development setup with all required tools and dependencies', 'completed', 'medium'),
            ('Write unit tests', 'Add comprehensive unit test coverage for core functionality', 'in_progress', 'high'),
            ('Code review', 'Review pull request #123 and provide feedback', 'pending', 'medium'),
            ('Deploy to staging', 'Deploy latest changes to staging environment for QA testing', 'in_progress', 'high'),
            ('Update documentation', 'Update API documentation with latest endpoint changes', 'pending', 'low'),
            ('Fix bug #456', 'Resolve issue with login functionality on mobile devices', 'in_progress', 'high'),
            ('Performance optimization', 'Optimize database queries to improve response times', 'pending', 'medium'),
            ('Security review', 'Review code for security vulnerabilities and best practices', 'pending', 'high'),
            ('User acceptance testing', 'Conduct UAT sessions with key stakeholders', 'pending', 'medium'),
            ('Implement authentication', 'Add OAuth2 authentication flow', 'completed', 'high'),
            ('Database schema design', 'Design and implement new database schema', 'completed', 'high'),
        ]
        
        task_count = 0
        for project in projects:
            num_tasks = random.randint(4, 8)
            for j in range(num_tasks):
                template = random.choice(task_templates)
                assigned_user = random.choice(all_users)
                task = Task(
                    title=template[0],
                    description=template[1],
                    project_id=project.id,
                    assigned_to=assigned_user.id,
                    created_by=project.owner_id,
                    status=template[2],
                    priority=template[3],
                    due_date=datetime.utcnow() + timedelta(days=random.randint(1, 21)),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 15))
                )
                db.session.add(task)
                task_count += 1
        
        db.session.commit()
        print(f"Created {task_count} tasks")
        
        # Create comments on tasks
        tasks = Task.query.all()
        comment_templates = [
            "Great progress on this! Looking forward to the next update.",
            "I've reviewed the code and left some feedback. Please address the security concerns.",
            "This looks good to me. Ready for merge after minor fixes.",
            "Can we discuss the approach for this? I have some suggestions.",
            "Blocked on this - waiting for API access from third-party vendor.",
            "Completed the first phase. Moving to next steps.",
            "Found an issue with the implementation. See details in the attached file.",
            "This is working well in testing. No issues found so far.",
        ]
        
        comment_count = 0
        for task in random.sample(tasks, min(15, len(tasks))):
            num_comments = random.randint(1, 3)
            for _ in range(num_comments):
                comment = Comment(
                    task_id=task.id,
                    user_id=random.choice(all_users).id,
                    content=random.choice(comment_templates),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 10))
                )
                db.session.add(comment)
                comment_count += 1
        
        db.session.commit()
        print(f"Created {comment_count} comments")
        
        # Create messages
        message_subjects = [
            "Project Update Required",
            "Meeting Scheduled",
            "Code Review Request",
            "Urgent: Bug Fix Needed",
            "Weekly Status Report",
            "New Feature Proposal",
            "Security Alert",
            "Deployment Notice",
            "Documentation Request",
            "Team Standup Reminder"
        ]
        
        message_count = 0
        for i in range(20):
            sender = random.choice(all_users)
            receiver = random.choice([u for u in all_users if u.id != sender.id])
            message = Message(
                sender_id=sender.id,
                receiver_id=receiver.id,
                subject=random.choice(message_subjects),
                content=f"This is a test message from {sender.username} to {receiver.username}. The message contains some sample content for testing the messaging system.",
                is_read=(i % 3 == 0),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 14))
            )
            db.session.add(message)
            message_count += 1
        
        db.session.commit()
        print(f"Created {message_count} messages")
        
        # Create notifications
        notification_types = ['task_assigned', 'message_received', 'project_updated', 'comment_added', 'task_completed']
        notification_messages = {
            'task_assigned': 'You have been assigned to a new task',
            'message_received': 'You have received a new message',
            'project_updated': 'A project you are following has been updated',
            'comment_added': 'A new comment was added to a task',
            'task_completed': 'A task has been marked as completed'
        }
        
        notification_count = 0
        for user in all_users:
            for i in range(random.randint(3, 7)):
                notif_type = random.choice(notification_types)
                notification = Notification(
                    user_id=user.id,
                    message=notification_messages.get(notif_type, 'You have a new notification'),
                    type=notif_type,
                    is_read=(i % 2 == 0),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 7))
                )
                db.session.add(notification)
                notification_count += 1
        
        db.session.commit()
        print(f"Created {notification_count} notifications")
        
        # Create some document records (without actual files)
        document_count = 0
        document_types = ['pdf', 'docx', 'txt', 'xlsx']
        document_names = [
            'Project Requirements',
            'Technical Specification',
            'User Guide',
            'API Documentation',
            'Test Plan',
            'Deployment Guide',
            'Architecture Diagram',
            'Meeting Notes'
        ]
        
        for project in random.sample(projects, min(4, len(projects))):
            for i in range(random.randint(2, 4)):
                doc_type = random.choice(document_types)
                doc_name = random.choice(document_names)
                document = Document(
                    filename=f"{doc_name.lower().replace(' ', '_')}_{project.id}_{i}.{doc_type}",
                    original_filename=f"{doc_name}.{doc_type}",
                    file_path=f"/app/uploads/{doc_name.lower().replace(' ', '_')}_{project.id}_{i}.{doc_type}",
                    file_size=random.randint(10000, 500000),
                    file_type=doc_type,
                    project_id=project.id,
                    uploaded_by=random.choice(all_users).id,
                    is_public=(i % 2 == 0),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 10))
                )
                db.session.add(document)
                document_count += 1
        
        db.session.commit()
        print(f"Created {document_count} document records")
        
        print(f"\n✓ Database seeding complete!")
        print(f"  - Users: {User.query.count()}")
        print(f"  - Projects: {Project.query.count()}")
        print(f"  - Tasks: {Task.query.count()}")
        print(f"  - Comments: {Comment.query.count()}")
        print(f"  - Messages: {Message.query.count()}")
        print(f"  - Notifications: {Notification.query.count()}")
        print(f"  - Documents: {Document.query.count()}")
        print(f"\nTest user credentials (all use password: password123):")
        for user in test_users:
            print(f"  - {user.username} ({user.email}) - Role: {user.role}")

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
        
        # Seed test data (only if database is empty)
        seed_data(app)

