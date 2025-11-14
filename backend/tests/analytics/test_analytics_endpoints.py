import pytest
import json


class TestAnalyticsEndpoints:
    
    def test_tasks_by_status(self, client, auth_headers, sample_data):
        """Test GET /analytics/tasks/by-status endpoint"""
        response = client.get('/analytics/tasks/by-status', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'data' in data
        
        status_data = data['data']
        assert len(status_data) > 0
        
        statuses = {item['status']: item['count'] for item in status_data}
        assert 'completed' in statuses
        assert 'in_progress' in statuses
        assert 'pending' in statuses
        
        assert statuses['completed'] == 2
        assert statuses['in_progress'] == 1
        assert statuses['pending'] == 1
    
    def test_average_completion_time(self, client, auth_headers, sample_data):
        """Test GET /analytics/tasks/average-completion-time endpoint"""
        response = client.get('/analytics/tasks/average-completion-time', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'data' in data
        
        result = data['data']
        assert 'average_days' in result
        assert 'completed_count' in result
        
        assert result['completed_count'] == 2
        assert result['average_days'] > 0
    
    def test_projects_summary(self, client, auth_headers, sample_data):
        """Test GET /analytics/projects/summary endpoint"""
        response = client.get('/analytics/projects/summary', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'data' in data
        
        projects = data['data']
        assert len(projects) == 2
        
        for project in projects:
            assert 'project_id' in project
            assert 'project_name' in project
            assert 'task_count' in project
            assert 'task_percentage' in project
        
        project_names = [p['project_name'] for p in projects]
        assert 'Project A' in project_names
        assert 'Project B' in project_names
        
        project_a = next(p for p in projects if p['project_name'] == 'Project A')
        assert project_a['task_count'] == 3
        
        project_b = next(p for p in projects if p['project_name'] == 'Project B')
        assert project_b['task_count'] == 1
    
    def test_user_productivity(self, client, auth_headers, sample_data):
        """Test GET /analytics/users/<id>/productivity endpoint"""
        users = sample_data['users']
        user1_id = users[0].id
        
        response = client.get(f'/analytics/users/{user1_id}/productivity', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'data' in data
        
        result = data['data']
        assert result['user_id'] == user1_id
        assert 'username' in result
        assert 'total_tasks' in result
        assert 'completed_tasks' in result
        assert 'completion_rate' in result
        assert 'tasks_by_status' in result
        
        assert result['total_tasks'] == 3
        assert result['completed_tasks'] == 2
        assert result['completion_rate'] > 0
    
    def test_user_productivity_not_found(self, client, auth_headers, sample_data):
        """Test user productivity for non-existent user"""
        response = client.get('/analytics/users/9999/productivity', headers=auth_headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        
        assert data['success'] is False
        assert 'error' in data
    
    def test_tasks_by_priority(self, client, auth_headers, sample_data):
        """Test GET /analytics/tasks/by-priority endpoint"""
        response = client.get('/analytics/tasks/by-priority', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'data' in data
        
        priorities = data['data']
        assert len(priorities) > 0
        
        for item in priorities:
            assert 'priority' in item
            assert 'count' in item
            assert 'avg_completion_days' in item
        
        priority_map = {item['priority']: item['count'] for item in priorities}
        assert 'high' in priority_map
        assert 'medium' in priority_map
        assert 'low' in priority_map
    
    def test_project_timeline(self, client, auth_headers, sample_data):
        """Test GET /analytics/projects/<id>/timeline endpoint"""
        projects = sample_data['projects']
        project1_id = projects[0].id
        
        response = client.get(f'/analytics/projects/{project1_id}/timeline', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'data' in data
        
        result = data['data']
        assert result['project_id'] == project1_id
        assert 'project_name' in result
        assert 'total_tasks' in result
        assert 'tasks' in result
        
        assert result['total_tasks'] == 3
        assert len(result['tasks']) == 3
        
        for task in result['tasks']:
            assert 'task_id' in task
            assert 'title' in task
            assert 'status' in task
            assert 'priority' in task
    
    def test_project_timeline_not_found(self, client, auth_headers, sample_data):
        """Test project timeline for non-existent project"""
        response = client.get('/analytics/projects/9999/timeline', headers=auth_headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        
        assert data['success'] is False
        assert 'error' in data
    
    def test_messaging_activity(self, client, auth_headers, sample_data):
        """Test GET /analytics/messaging/activity endpoint"""
        response = client.get('/analytics/messaging/activity', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'data' in data
        
        activity = data['data']
        assert len(activity) > 0
        
        for item in activity:
            assert 'date' in item
            assert 'message_count' in item
    
    def test_analytics_requires_auth(self, client, sample_data):
        """Test that analytics endpoints require authentication"""
        endpoints = [
            '/analytics/tasks/by-status',
            '/analytics/tasks/average-completion-time',
            '/analytics/projects/summary',
            '/analytics/users/1/productivity',
            '/analytics/tasks/by-priority',
            '/analytics/projects/1/timeline',
            '/analytics/messaging/activity'
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 401

