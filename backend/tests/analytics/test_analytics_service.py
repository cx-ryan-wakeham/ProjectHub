import pytest
import pandas as pd
from analytics.service import AnalyticsService


class TestAnalyticsService:
    
    def test_get_tasks_by_status_returns_list(self, app, sample_data):
        """Test that get_tasks_by_status returns a list of dictionaries"""
        with app.app_context():
            result = AnalyticsService.get_tasks_by_status()
            
            assert isinstance(result, list)
            assert len(result) > 0
            
            for item in result:
                assert isinstance(item, dict)
                assert 'status' in item
                assert 'count' in item
    
    def test_get_tasks_by_status_uses_pandas(self, app, sample_data):
        """Test that pandas is used for data processing"""
        with app.app_context():
            result = AnalyticsService.get_tasks_by_status()
            
            df = pd.DataFrame(result)
            assert not df.empty
            assert 'status' in df.columns
            assert 'count' in df.columns
            
            completed_count = df[df['status'] == 'completed']['count'].iloc[0]
            assert completed_count == 2
    
    def test_get_average_completion_time_calculation(self, app, sample_data):
        """Test average completion time calculation with pandas"""
        with app.app_context():
            result = AnalyticsService.get_average_completion_time()
            
            assert isinstance(result, dict)
            assert 'average_days' in result
            assert 'completed_count' in result
            
            assert result['completed_count'] == 2
            assert result['average_days'] == 2.0
    
    def test_get_projects_summary_with_percentages(self, app, sample_data):
        """Test projects summary includes pandas-calculated percentages"""
        with app.app_context():
            result = AnalyticsService.get_projects_summary()
            
            assert isinstance(result, list)
            assert len(result) == 2
            
            total_percentage = sum(item['task_percentage'] for item in result)
            assert abs(total_percentage - 100.0) < 0.1
            
            df = pd.DataFrame(result)
            assert 'task_percentage' in df.columns
    
    def test_get_user_productivity_with_completion_rate(self, app, sample_data):
        """Test user productivity calculation includes pandas metrics"""
        with app.app_context():
            users = sample_data['users']
            user1_id = users[0].id
            
            result = AnalyticsService.get_user_productivity(user1_id)
            
            assert result is not None
            assert result['user_id'] == user1_id
            assert result['total_tasks'] == 3
            assert result['completed_tasks'] == 2
            
            expected_rate = (2 / 3) * 100
            assert abs(result['completion_rate'] - expected_rate) < 0.1
    
    def test_get_user_productivity_returns_none_for_invalid_user(self, app, sample_data):
        """Test that get_user_productivity returns None for non-existent user"""
        with app.app_context():
            result = AnalyticsService.get_user_productivity(9999)
            assert result is None
    
    def test_get_tasks_by_priority_aggregation(self, app, sample_data):
        """Test tasks by priority uses pandas for sorting and aggregation"""
        with app.app_context():
            result = AnalyticsService.get_tasks_by_priority()
            
            assert isinstance(result, list)
            
            df = pd.DataFrame(result)
            assert not df.empty
            
            priorities = df['priority'].tolist()
            assert 'high' in priorities
            assert 'medium' in priorities
            assert 'low' in priorities
    
    def test_get_project_timeline_dataframe_conversion(self, app, sample_data):
        """Test project timeline uses pandas DataFrame conversion"""
        with app.app_context():
            projects = sample_data['projects']
            project1_id = projects[0].id
            
            result = AnalyticsService.get_project_timeline(project1_id)
            
            assert result is not None
            assert 'tasks' in result
            
            if result['total_tasks'] > 0:
                df = pd.DataFrame(result['tasks'])
                assert not df.empty
                assert 'task_id' in df.columns
                assert 'title' in df.columns
                assert 'status' in df.columns
    
    def test_get_project_timeline_returns_none_for_invalid_project(self, app, sample_data):
        """Test that get_project_timeline returns None for non-existent project"""
        with app.app_context():
            result = AnalyticsService.get_project_timeline(9999)
            assert result is None
    
    def test_get_messaging_activity_temporal_aggregation(self, app, sample_data):
        """Test messaging activity uses pandas for temporal data processing"""
        with app.app_context():
            result = AnalyticsService.get_messaging_activity()
            
            assert isinstance(result, list)
            
            if len(result) > 0:
                df = pd.DataFrame(result)
                assert 'date' in df.columns
                assert 'message_count' in df.columns
                
                assert df['message_count'].dtype in [int, 'int64', 'int32']
    
    def test_sqlalchemy_2x_patterns_no_model_query(self, app, sample_data):
        """Verify that analytics service does not use Model.query patterns"""
        import inspect
        from analytics import service
        
        source = inspect.getsource(service)
        
        assert '.query.' not in source
        assert 'Model.query' not in source
        
        assert 'select(' in source
        assert 'db.session.execute' in source or 'db.session.scalars' in source or 'db.session.get' in source
    
    def test_pandas_integration_dataframe_operations(self, app, sample_data):
        """Test that pandas DataFrame operations are used throughout"""
        with app.app_context():
            result = AnalyticsService.get_projects_summary()
            
            df = pd.DataFrame(result)
            
            assert not df.empty
            assert 'project_id' in df.columns
            assert 'task_count' in df.columns
            assert 'task_percentage' in df.columns
            
            assert df['task_count'].sum() == 4

