from sqlalchemy import select, func
from db_ext import db
from models import Task, Project, User, Comment, Message
from datetime import datetime, timedelta
import pandas as pd


class AnalyticsService:
    
    @staticmethod
    def get_tasks_by_status():
        stmt = select(Task.status, func.count(Task.id).label('count')).group_by(Task.status)
        result = db.session.execute(stmt).fetchall()
        
        df = pd.DataFrame.from_records(
            [(row[0], row[1]) for row in result],
            columns=['status', 'count']
        )
        return df.to_dict(orient='records')
    
    @staticmethod
    def get_average_completion_time():
        stmt = select(
            Task.id,
            Task.created_at,
            Task.updated_at,
            Task.status
        ).where(Task.status == 'completed')
        
        result = db.session.execute(stmt).fetchall()
        
        if not result:
            return {'average_days': 0, 'completed_count': 0}
        
        records = []
        for row in result:
            if row[1] and row[2]:  # created_at and updated_at
                delta = row[2] - row[1]
                records.append({
                    'task_id': row[0],
                    'days_to_complete': delta.total_seconds() / 86400
                })
        
        if not records:
            return {'average_days': 0, 'completed_count': 0}
        
        df = pd.DataFrame(records)
        avg_days = df['days_to_complete'].mean()
        
        return {
            'average_days': round(avg_days, 2),
            'completed_count': len(records)
        }
    
    @staticmethod
    def get_projects_summary():
        stmt = select(
            Project.id,
            Project.name,
            func.count(Task.id).label('task_count')
        ).outerjoin(Task, Task.project_id == Project.id).group_by(Project.id, Project.name)
        
        result = db.session.execute(stmt).fetchall()
        
        records = [
            {
                'project_id': row[0],
                'project_name': row[1],
                'task_count': row[2]
            }
            for row in result
        ]
        
        df = pd.DataFrame(records)
        
        if df.empty:
            return []
        
        df['task_percentage'] = (df['task_count'] / df['task_count'].sum() * 100).round(2)
        
        return df.to_dict(orient='records')
    
    @staticmethod
    def get_user_productivity(user_id):
        user = db.session.get(User, user_id)
        if not user:
            return None
        
        stmt = select(
            Task.status,
            func.count(Task.id).label('count')
        ).where(Task.assigned_to == user_id).group_by(Task.status)
        
        result = db.session.execute(stmt).fetchall()
        
        df = pd.DataFrame.from_records(
            [(row[0], row[1]) for row in result],
            columns=['status', 'count']
        )
        
        total_tasks = df['count'].sum() if not df.empty else 0
        completed_tasks = df[df['status'] == 'completed']['count'].sum() if not df.empty else 0
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            'user_id': user_id,
            'username': user.username,
            'total_tasks': int(total_tasks),
            'completed_tasks': int(completed_tasks),
            'completion_rate': round(completion_rate, 2),
            'tasks_by_status': df.to_dict(orient='records') if not df.empty else []
        }
    
    @staticmethod
    def get_tasks_by_priority():
        stmt = select(
            Task.priority,
            func.count(Task.id).label('count'),
            func.avg(
                func.extract('epoch', Task.updated_at - Task.created_at) / 86400
            ).label('avg_days')
        ).group_by(Task.priority)
        
        result = db.session.execute(stmt).fetchall()
        
        records = [
            {
                'priority': row[0],
                'count': row[1],
                'avg_completion_days': round(row[2], 2) if row[2] else 0
            }
            for row in result
        ]
        
        df = pd.DataFrame(records)
        
        if df.empty:
            return []
        
        df = df.sort_values(by='priority')
        
        return df.to_dict(orient='records')
    
    @staticmethod
    def get_project_timeline(project_id):
        project = db.session.get(Project, project_id)
        if not project:
            return None
        
        stmt = select(Task).where(Task.project_id == project_id)
        tasks = db.session.scalars(stmt).all()
        
        if not tasks:
            return {
                'project_id': project_id,
                'project_name': project.name,
                'tasks': []
            }
        
        records = [
            {
                'task_id': task.id,
                'title': task.title,
                'status': task.status,
                'priority': task.priority,
                'created_at': task.created_at.isoformat() if task.created_at else None,
                'due_date': task.due_date.isoformat() if task.due_date else None
            }
            for task in tasks
        ]
        
        df = pd.DataFrame(records)
        
        return {
            'project_id': project_id,
            'project_name': project.name,
            'total_tasks': len(tasks),
            'tasks': df.to_dict(orient='records')
        }
    
    @staticmethod
    def get_messaging_activity():
        stmt = select(
            func.date_trunc('day', Message.created_at).label('date'),
            func.count(Message.id).label('count')
        ).group_by(func.date_trunc('day', Message.created_at)).order_by(func.date_trunc('day', Message.created_at))
        
        result = db.session.execute(stmt).fetchall()
        
        records = [
            {
                'date': row[0].strftime('%Y-%m-%d') if row[0] else None,
                'message_count': row[1]
            }
            for row in result
        ]
        
        df = pd.DataFrame(records)
        
        if df.empty:
            return []
        
        df['message_count'] = df['message_count'].astype(int)
        
        return df.to_dict(orient='records')

