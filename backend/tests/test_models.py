"""
Basic tests for database models
"""
import unittest
from datetime import datetime
from models import User, Project, Task, Message


class TestUserModel(unittest.TestCase):
    """Test User model"""
    
    def test_user_password_hashing(self):
        """Test password hashing and checking"""
        user = User()
        user.username = "testuser"
        user.email = "test@example.com"
        user.set_password("password123")
        
        # Password should be hashed
        self.assertNotEqual(user.password_hash, "password123")
        
        # Check password should work
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.check_password("wrongpassword"))
    
    def test_user_to_dict(self):
        """Test user serialization"""
        user = User()
        user.id = 1
        user.username = "testuser"
        user.email = "test@example.com"
        user.role = "team_member"
        user.created_at = datetime.now()
        
        user_dict = user.to_dict()
        
        self.assertEqual(user_dict['id'], 1)
        self.assertEqual(user_dict['username'], "testuser")
        self.assertEqual(user_dict['email'], "test@example.com")
        self.assertEqual(user_dict['role'], "team_member")
        self.assertIn('created_at', user_dict)


class TestProjectModel(unittest.TestCase):
    """Test Project model"""
    
    def test_project_to_dict(self):
        """Test project serialization"""
        project = Project()
        project.id = 1
        project.name = "Test Project"
        project.description = "A test project"
        project.owner_id = 1
        project.is_public = False
        project.created_at = datetime.now()
        project.updated_at = datetime.now()
        
        project_dict = project.to_dict()
        
        self.assertEqual(project_dict['id'], 1)
        self.assertEqual(project_dict['name'], "Test Project")
        self.assertEqual(project_dict['description'], "A test project")
        self.assertEqual(project_dict['owner_id'], 1)
        self.assertFalse(project_dict['is_public'])


class TestTaskModel(unittest.TestCase):
    """Test Task model"""
    
    def test_task_to_dict(self):
        """Test task serialization"""
        task = Task()
        task.id = 1
        task.title = "Test Task"
        task.description = "A test task"
        task.project_id = 1
        task.created_by = 1
        task.status = "pending"
        task.priority = "high"
        task.created_at = datetime.now()
        
        task_dict = task.to_dict()
        
        self.assertEqual(task_dict['id'], 1)
        self.assertEqual(task_dict['title'], "Test Task")
        self.assertEqual(task_dict['status'], "pending")
        self.assertEqual(task_dict['priority'], "high")


class TestMessageModel(unittest.TestCase):
    """Test Message model"""
    
    def test_message_to_dict(self):
        """Test message serialization"""
        message = Message()
        message.id = 1
        message.sender_id = 1
        message.receiver_id = 2
        message.subject = "Test Subject"
        message.content = "Test content"
        message.is_read = False
        message.created_at = datetime.now()
        
        message_dict = message.to_dict()
        
        self.assertEqual(message_dict['id'], 1)
        self.assertEqual(message_dict['sender_id'], 1)
        self.assertEqual(message_dict['receiver_id'], 2)
        self.assertEqual(message_dict['subject'], "Test Subject")
        self.assertFalse(message_dict['is_read'])


if __name__ == '__main__':
    unittest.main()

