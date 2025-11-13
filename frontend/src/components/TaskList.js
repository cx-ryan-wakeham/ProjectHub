import React, { useState, useEffect } from 'react';
import api from '../services/api';

function TaskList({ user }) {
  const [tasks, setTasks] = useState([]);
  const [projects, setProjects] = useState([]);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    project_id: '',
    priority: 'medium'
  });
  const [comments, setComments] = useState({});
  const [newComment, setNewComment] = useState({});

  useEffect(() => {
    loadTasks();
    loadProjects();
  }, []);

  const loadTasks = async () => {
    try {
      const response = await api.get('/tasks');
      setTasks(response.data.tasks);
    } catch (error) {
      console.error('Error loading tasks:', error);
    }
  };

  const loadProjects = async () => {
    try {
      const response = await api.get('/projects');
      setProjects(response.data.projects);
    } catch (error) {
      console.error('Error loading projects:', error);
    }
  };

  const loadComments = async (taskId) => {
    try {
      const response = await api.get(`/tasks/${taskId}/comments`);
      setComments({ ...comments, [taskId]: response.data.comments });
    } catch (error) {
      console.error('Error loading comments:', error);
    }
  };

  const handleCreateTask = async (e) => {
    e.preventDefault();
    try {
      await api.post('/tasks', newTask);
      setNewTask({ title: '', description: '', project_id: '', priority: 'medium' });
      loadTasks();
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  const handleAddComment = async (taskId) => {
    try {
      await api.post(`/tasks/${taskId}/comments`, {
        content: newComment[taskId] || ''
      });
      setNewComment({ ...newComment, [taskId]: '' });
      loadComments(taskId);
    } catch (error) {
      console.error('Error adding comment:', error);
    }
  };

  return (
    <div className="container">
      <h2>Tasks</h2>

      <div className="card" style={{ marginBottom: '2rem' }}>
        <h3>Create New Task</h3>
        <form onSubmit={handleCreateTask}>
          <div className="form-group">
            <label>Title:</label>
            <input
              type="text"
              value={newTask.title}
              onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Description:</label>
            <textarea
              value={newTask.description}
              onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
              rows="4"
            />
          </div>
          <div className="form-group">
            <label>Project:</label>
            <select
              value={newTask.project_id}
              onChange={(e) => setNewTask({ ...newTask, project_id: e.target.value })}
              required
            >
              <option value="">Select a project</option>
              {projects.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Priority:</label>
            <select
              value={newTask.priority}
              onChange={(e) => setNewTask({ ...newTask, priority: e.target.value })}
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          <button type="submit" className="button">Create Task</button>
        </form>
      </div>

      <div>
        <h3>All Tasks</h3>
        {tasks.map(task => (
          <div key={task.id} className={`card task-item ${task.status} ${task.priority}-priority`}>
            <h4>{task.title}</h4>
            {/* VULNERABLE: XSS - dangerouslySetInnerHTML without sanitization */}
            <div dangerouslySetInnerHTML={{ __html: task.description || '' }} />
            <p>Status: {task.status} | Priority: {task.priority}</p>
            
            <div style={{ marginTop: '1rem' }}>
              <h5>Comments</h5>
              {!comments[task.id] && (
                <button onClick={() => loadComments(task.id)} className="button">
                  Load Comments
                </button>
              )}
              {comments[task.id] && comments[task.id].map(comment => (
                <div key={comment.id} style={{ marginBottom: '0.5rem', padding: '0.5rem', background: '#f0f0f0', borderRadius: '4px' }}>
                  {/* VULNERABLE: XSS - dangerouslySetInnerHTML without sanitization */}
                  <div dangerouslySetInnerHTML={{ __html: comment.content }} />
                  <small>{new Date(comment.created_at).toLocaleString()}</small>
                </div>
              ))}
              
              <div style={{ marginTop: '0.5rem' }}>
                <textarea
                  placeholder="Add a comment..."
                  value={newComment[task.id] || ''}
                  onChange={(e) => setNewComment({ ...newComment, [task.id]: e.target.value })}
                  rows="2"
                  style={{ width: '100%', marginBottom: '0.5rem' }}
                />
                <button onClick={() => handleAddComment(task.id)} className="button">
                  Add Comment
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TaskList;

