# Database initialization and connection setup
from models import db, User, Project, Task, Document, Message, Comment
from config import Config
import hashlib
import os
from datetime import datetime, timedelta
import random

def seed_data(app):
    """Populate database with test/dummy data"""
    with app.app_context():
        try:
            # Check environment variable to skip seeding
            if os.environ.get('SKIP_SEED', 'false').lower() == 'true':
                print("Skipping seed data (SKIP_SEED=true)")
                return
            
            # Check if data already exists
            if Project.query.count() > 0:
                print("Database already has data, skipping seed...")
                return
            
            print("Seeding database with test data...")
        except Exception as e:
            print(f"Error checking seed conditions: {e}")
            return
        
        try:
            # Get admin user (check both 'admin' and 'Admin' for backward compatibility)
            admin = User.query.filter_by(username='Admin').first()
            if not admin:
                admin = User.query.filter_by(username='admin').first()
            if not admin:
                print("Warning: Admin user not found, cannot seed data")
                return
            
            # Create additional test users
            test_users = []
            user_data = [
            {'username': 'Alice', 'email': 'alice@projecthub.com', 'role': 'project_manager'},
            {'username': 'Bob', 'email': 'bob@projecthub.com', 'role': 'team_member'},
            {'username': 'Charlie', 'email': 'charlie@projecthub.com', 'role': 'team_member'},
            {'username': 'Diana', 'email': 'diana@projecthub.com', 'role': 'team_member'},
            {'username': 'Eve', 'email': 'eve@projecthub.com', 'role': 'project_manager'},
            ]
            
            for user_info in user_data:
                user = User.query.filter_by(username=user_info['username']).first()
                if not user:
                    # Password is same as username (capitalized)
                    password = user_info['username']
                    user = User(
                        username=user_info['username'],
                        email=user_info['email'],
                        role=user_info['role']
                    )
                    user.set_password(password)
                    user.api_key = f"{user_info['username']}_api_key_{hashlib.md5(password.encode()).hexdigest()}"
                    db.session.add(user)
                    test_users.append(user)
            
            db.session.commit()
            all_users = [admin] + test_users
            print(f"Created {len(test_users)} test users")
            
            # Store user IDs early to avoid lazy loading issues
            all_user_ids = [user.id for user in all_users]
            
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
            
            project_ids = []
            project_owner_ids = []
            for i, proj_data in enumerate(project_data):
                project = Project(
                    name=proj_data['name'],
                    description=proj_data['description'],
                    owner_id=all_user_ids[i % len(all_user_ids)],
                    is_public=proj_data['is_public'],
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                )
                db.session.add(project)
                # Flush each project individually to avoid bulk insert issues
                db.session.flush()
                # Store IDs immediately after flush
                project_ids.append(project.id)
                project_owner_ids.append(project.owner_id)
            
            db.session.commit()
            print(f"Created {len(project_ids)} projects")
            
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
            
            # Use stored user IDs to avoid lazy loading issues
            user_ids = all_user_ids
            
            task_count = 0
            for i, project_id in enumerate(project_ids):
                # Use stored project attributes
                owner_id = project_owner_ids[i]
                num_tasks = random.randint(4, 8)
                for j in range(num_tasks):
                    template = random.choice(task_templates)
                    assigned_user_id = random.choice(user_ids)
                    task = Task(
                        title=template[0],
                        description=template[1],
                        project_id=project_id,
                        assigned_to=assigned_user_id,
                        created_by=owner_id,
                        status=template[2],
                        priority=template[3],
                        due_date=datetime.utcnow() + timedelta(days=random.randint(1, 21)),
                        created_at=datetime.utcnow() - timedelta(days=random.randint(1, 15))
                    )
                    db.session.add(task)
                    task_count += 1
                    # Flush each task individually to avoid SQLAlchemy/psycopg2 bulk insert compatibility issues
                    db.session.flush()
            
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
                        user_id=random.choice(user_ids),
                        content=random.choice(comment_templates),
                        created_at=datetime.utcnow() - timedelta(days=random.randint(1, 10))
                    )
                    db.session.add(comment)
                    comment_count += 1
                    # Flush each comment individually to avoid bulk insert issues
                    db.session.flush()
            
            db.session.commit()
            print(f"Created {comment_count} comments")
            
            # Create messages
            # Realistic message templates with varied content
            message_templates = [
                {
                    'subject': 'Project Update Required',
                    'content': 'Hi, could you please provide an update on the current status of the project? We need to report progress to stakeholders by end of week.'
                },
                {
                    'subject': 'Meeting Scheduled',
                    'content': 'I\'ve scheduled a team meeting for tomorrow at 2 PM to discuss the upcoming sprint. Please confirm your availability.'
                },
                {
                    'subject': 'Code Review Request',
                    'content': 'I\'ve submitted a pull request for the authentication module. Could you take a look when you have a chance? The changes are in the auth branch.'
                },
                {
                    'subject': 'Urgent: Bug Fix Needed',
                    'content': 'We\'ve identified a critical bug in the payment processing flow. The issue occurs when users try to complete checkout. Can you prioritize this?'
                },
                {
                    'subject': 'Weekly Status Report',
                    'content': 'Here\'s this week\'s status report:\n\n- Completed user authentication module\n- Fixed 3 critical bugs\n- Started work on dashboard redesign\n\nLet me know if you need any additional details.'
                },
                {
                    'subject': 'New Feature Proposal',
                    'content': 'I\'ve drafted a proposal for the new notification system. The document outlines the architecture and implementation approach. Would love to get your feedback before we proceed.'
                },
                {
                    'subject': 'Security Alert',
                    'content': 'We detected some unusual activity in the logs. I\'ve temporarily locked the affected accounts. Can we schedule a quick call to review the security measures?'
                },
                {
                    'subject': 'Deployment Notice',
                    'content': 'The latest version has been deployed to staging. All tests passed successfully. Planning to push to production tomorrow morning if everything looks good.'
                },
                {
                    'subject': 'Documentation Request',
                    'content': 'Could you update the API documentation for the new endpoints? We need to include examples for the authentication and user management endpoints.'
                },
                {
                    'subject': 'Team Standup Reminder',
                    'content': 'Just a reminder that our daily standup is at 9 AM. Please come prepared with your updates on what you completed yesterday and what you plan to work on today.'
                },
                {
                    'subject': 'Database Migration',
                    'content': 'I\'ve prepared the migration script for the schema changes. It needs to be run during the maintenance window this weekend. Can you review the script?'
                },
                {
                    'subject': 'Performance Issue',
                    'content': 'Users are reporting slow response times on the dashboard page. I\'ve identified a few potential bottlenecks. Should we schedule a performance optimization session?'
                },
                {
                    'subject': 'Client Feedback',
                    'content': 'The client reviewed the latest prototype and provided some feedback. They\'re happy with the overall direction but requested a few UI tweaks. I\'ve attached their comments.'
                },
                {
                    'subject': 'API Integration',
                    'content': 'The third-party API integration is complete. I\'ve tested all the endpoints and everything is working as expected. The documentation is in the shared drive.'
                },
                {
                    'subject': 'Testing Results',
                    'content': 'All unit tests are passing. However, we have 2 failing integration tests related to the payment flow. I\'m investigating the root cause.'
                },
                {
                    'subject': 'Budget Approval',
                    'content': 'The budget for Q4 has been approved. We can proceed with the infrastructure upgrades we discussed. I\'ll send the purchase orders next week.'
                },
                {
                    'subject': 'Training Session',
                    'content': 'I\'ve scheduled a training session on the new deployment process for next Tuesday. All team members are invited. The session will cover CI/CD best practices.'
                },
                {
                    'subject': 'Dependency Update',
                    'content': 'We need to update several dependencies to address security vulnerabilities. I\'ve created a branch with the updates. Please test thoroughly before we merge.'
                },
                {
                    'subject': 'User Feedback',
                    'content': 'Received positive feedback from beta users about the new search feature. They particularly liked the improved filtering options. Great work on this!'
                },
                {
                    'subject': 'Sprint Planning',
                    'content': 'Sprint planning meeting is scheduled for Friday. Please review the backlog items and come prepared with estimates. We\'re aiming to finalize the sprint goals.'
                },
                {
                    'subject': 'Infrastructure Maintenance',
                    'content': 'Scheduled maintenance window for this Saturday from 2 AM to 4 AM. The database will be unavailable during this time. I\'ll send a reminder closer to the date.'
                },
                {
                    'subject': 'Design Review',
                    'content': 'The design team has completed the mockups for the new user interface. They\'re available for review in Figma. Let me know your thoughts.'
                },
                {
                    'subject': 'Compliance Check',
                    'content': 'We need to complete the compliance audit by end of month. I\'ve prepared a checklist of items we need to verify. Can you help review the security measures?'
                },
                {
                    'subject': 'Release Notes',
                    'content': 'I\'ve drafted the release notes for version 2.1. Please review and let me know if you want to add or modify anything before we publish.'
                },
                {
                    'subject': 'Customer Support',
                    'content': 'A customer reported an issue with the export functionality. They\'re unable to download reports in PDF format. I\'ve created a ticket and started investigating.'
                },
                {
                    'subject': 'Code Review Complete',
                    'content': 'I\'ve completed the code review for the pull request. Overall looks good, but I\'ve left a few comments about potential improvements. Please address them before we merge.'
                },
                {
                    'subject': 'Sprint Retrospective',
                    'content': 'The sprint retrospective is scheduled for this afternoon. Please come prepared to discuss what went well, what could be improved, and any blockers we encountered.'
                },
                {
                    'subject': 'Database Backup',
                    'content': 'The weekly database backup completed successfully. All data has been backed up to the secure storage location. Backup size: 2.3 GB.'
                },
                {
                    'subject': 'New Team Member',
                    'content': 'We have a new team member joining us next week. They\'ll be working on the frontend team. Please make them feel welcome and help them get up to speed.'
                },
                {
                    'subject': 'API Rate Limits',
                    'content': 'We\'re approaching the rate limits for our third-party API. I\'ve implemented caching to reduce the number of calls. We should monitor usage over the next few days.'
                },
                {
                    'subject': 'Security Patch',
                    'content': 'A critical security patch has been released for one of our dependencies. I\'ve tested it in staging and it looks good. Planning to deploy to production tonight.'
                },
                {
                    'subject': 'Performance Metrics',
                    'content': 'The performance metrics for this month look great. Average response time decreased by 15% and we\'ve had zero downtime. Keep up the excellent work!'
                },
                {
                    'subject': 'Client Meeting',
                    'content': 'We have a client meeting scheduled for next Tuesday at 10 AM. They want to discuss the roadmap for Q1. I\'ll send the agenda by end of week.'
                },
                {
                    'subject': 'Documentation Update',
                    'content': 'I\'ve updated the API documentation with the new endpoints. The documentation is now available in the developer portal. Please review and let me know if anything needs clarification.'
                },
                {
                    'subject': 'Bug Triage',
                    'content': 'We have 5 new bugs reported this week. I\'ve prioritized them based on severity. The critical ones need to be addressed by end of week. Check the bug tracker for details.'
                },
                {
                    'subject': 'Infrastructure Scaling',
                    'content': 'Due to increased traffic, we need to scale up our infrastructure. I\'ve provisioned additional servers and they\'re ready to go live. The scaling will happen automatically based on load.'
                },
                {
                    'subject': 'Code Quality Metrics',
                    'content': 'Our code quality metrics have improved significantly this quarter. Test coverage is up to 85% and we\'ve reduced technical debt by 30%. Great progress team!'
                },
                {
                    'subject': 'Holiday Schedule',
                    'content': 'The holiday schedule for December has been posted. Please update your availability in the calendar. We\'ll maintain minimal coverage during the holidays.'
                },
                {
                    'subject': 'Feature Request',
                    'content': 'A customer has requested a new feature for the dashboard. They want the ability to customize widget layouts. I\'ve added it to the backlog for prioritization.'
                },
                {
                    'subject': 'Monitoring Alert',
                    'content': 'We received an alert about high CPU usage on one of our servers. I\'ve investigated and it appears to be a temporary spike. Monitoring continues.'
                },
                {
                    'subject': 'Team Lunch',
                    'content': 'Team lunch is scheduled for Friday at noon. We\'ll be going to the new restaurant downtown. Please RSVP by Wednesday so I can make reservations.'
                },
                {
                    'subject': 'Version Release',
                    'content': 'Version 2.2 has been released to production. All new features are live and the deployment went smoothly. No issues reported so far.'
                },
                {
                    'subject': 'Data Migration',
                    'content': 'The data migration for the legacy system is complete. All historical data has been successfully migrated. I\'ve run validation checks and everything looks good.'
                },
                {
                    'subject': 'Access Request',
                    'content': 'I need access to the production database for troubleshooting. Could you please grant me temporary access? I\'ll only need it for a few hours.'
                },
                {
                    'subject': 'Code Freeze',
                    'content': 'Code freeze is in effect starting Monday. Only critical bug fixes will be allowed. All feature development should be completed and merged by end of day Friday.'
                },
                {
                    'subject': 'Performance Testing',
                    'content': 'I\'ve completed performance testing on the new feature. Results show it can handle 1000 concurrent users without issues. Ready for production deployment.'
                },
                {
                    'subject': 'Third-Party Integration',
                    'content': 'The integration with the new payment provider is complete. I\'ve tested all payment flows and everything is working correctly. We can start accepting payments through the new provider.'
                },
                {
                    'subject': 'Backup Verification',
                    'content': 'I\'ve verified the database backups and confirmed they\'re working correctly. Test restore was successful. All backups are being stored securely.'
                },
                {
                    'subject': 'Team Offsite',
                    'content': 'The team offsite is scheduled for next month. We\'ll be focusing on team building and strategic planning. More details to follow.'
                }
            ]
            
            message_count = 0
            for i in range(100):  # Doubled from 50 to 100 messages
                sender_id = random.choice(user_ids)
                receiver_id = random.choice([uid for uid in user_ids if uid != sender_id])
                template = random.choice(message_templates)
                # Messages go back as far as 6 months (180 days)
                message = Message(
                    sender_id=sender_id,
                    receiver_id=receiver_id,
                    subject=template['subject'],
                    content=template['content'],
                    is_read=(i % 3 == 0),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 180), hours=random.randint(0, 23))
                )
                db.session.add(message)
                message_count += 1
                # Flush each message individually to avoid bulk insert issues
                db.session.flush()
            
            db.session.commit()
            print(f"Created {message_count} messages")
            
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
            
            # Select random project IDs for documents
            selected_project_indices = random.sample(range(len(project_ids)), min(4, len(project_ids)))
            for project_idx in selected_project_indices:
                project_id = project_ids[project_idx]
                for i in range(random.randint(2, 4)):
                    doc_type = random.choice(document_types)
                    doc_name = random.choice(document_names)
                    document = Document(
                        filename=f"{doc_name.lower().replace(' ', '_')}_{project_id}_{i}.{doc_type}",
                        original_filename=f"{doc_name}.{doc_type}",
                        file_path=f"/app/uploads/{doc_name.lower().replace(' ', '_')}_{project_id}_{i}.{doc_type}",
                        file_size=random.randint(10000, 500000),
                        file_type=doc_type,
                        project_id=project_id,
                        uploaded_by=random.choice(user_ids),
                        is_public=(i % 2 == 0),
                        created_at=datetime.utcnow() - timedelta(days=random.randint(1, 10))
                    )
                    db.session.add(document)
                    document_count += 1
                    # Flush each document individually to avoid bulk insert issues
                    db.session.flush()
            
            db.session.commit()
            print(f"Created {document_count} document records")
            
            print(f"\nDatabase seeding complete!")
            print(f"  - Users: {User.query.count()}")
            print(f"  - Projects: {Project.query.count()}")
            print(f"  - Tasks: {Task.query.count()}")
            print(f"  - Comments: {Comment.query.count()}")
            print(f"  - Messages: {Message.query.count()}")
            print(f"  - Documents: {Document.query.count()}")
            print(f"\nTest user credentials (all use password: password123):")
            for user in test_users:
                print(f"  - {user.username} ({user.email}) - Role: {user.role}")
        except Exception as e:
            print(f"\nWARNING: Error during database seeding: {e}")
            print("Server will continue to start, but database may be incomplete.")
            import traceback
            traceback.print_exc()
            db.session.rollback()

def init_db(app):
    """Initialize database and create tables"""
    with app.app_context():
        db.create_all()
        
        # Create default admin user if it doesn't exist
        # Check both 'Admin' and 'admin' for backward compatibility
        admin = User.query.filter_by(username='Admin').first()
        if not admin:
            admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Password is same as username
            admin_password = 'Admin'
            admin = User(
                username='Admin',
                email=Config.ADMIN_EMAIL,
                role='admin'
            )
            admin.set_password(admin_password)
            admin.api_key = "admin_api_key_12345"
            db.session.add(admin)
            db.session.commit()
            print(f"Created admin user: {Config.ADMIN_EMAIL} / {admin_password}")
        
        # Seed test data (only if database is empty)
        seed_data(app)

