import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import api from '../services/api';

function ProjectDetail({ user }) {
  const { id } = useParams();
  const history = useHistory();
  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadProjectData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Load project details
      const projectResponse = await api.get(`/projects/${id}`);
      setProject(projectResponse.data.project);
      
      // Load project tasks
      try {
        const tasksResponse = await api.get('/tasks', {
          params: { project_id: id }
        });
        setTasks(tasksResponse.data.tasks || []);
      } catch (err) {
        console.error('Error loading tasks:', err);
        setTasks([]);
      }
      
      // Load project documents
      try {
        const docsResponse = await api.get('/documents', {
          params: { project_id: id }
        });
        setDocuments(docsResponse.data.documents || []);
      } catch (err) {
        console.error('Error loading documents:', err);
        setDocuments([]);
      }
    } catch (err) {
      console.error('Error loading project:', err);
      setError(err.response?.data?.error || 'Failed to load project');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    loadProjectData();
  }, [loadProjectData]);


  if (loading) {
    return (
      <div className="container">
        <div className="card">
          <p>Loading project...</p>
        </div>
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="container">
        <div className="card">
          <h2>Project Not Found</h2>
          <p>{error || 'The project you are looking for does not exist.'}</p>
          <button className="button" onClick={() => history.push('/dashboard')}>
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2>{project.name}</h2>
          <button className="button" onClick={() => history.push('/dashboard')}>
            Back to Dashboard
          </button>
        </div>
        
        <div style={{ marginBottom: '1rem' }}>
          <p><strong>Description:</strong></p>
          {/* VULNERABLE: XSS - dangerouslySetInnerHTML without sanitization */}
          <div dangerouslySetInnerHTML={{ __html: project.description || 'No description provided.' }} />
        </div>
        
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
          <div>
            <strong>Status:</strong> {project.is_public ? 'Public' : 'Private'}
          </div>
          <div>
            <strong>Owner ID:</strong> {project.owner_id}
          </div>
          {project.created_at && (
            <div>
              <strong>Created:</strong> {new Date(project.created_at).toLocaleDateString()}
            </div>
          )}
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
        <div>
          <div className="card">
            <h3>Tasks ({tasks.length})</h3>
            {tasks.length > 0 ? (
              <div>
                {tasks.map(task => (
                  <div key={task.id} className="card" style={{ marginBottom: '0.5rem', padding: '0.75rem' }}>
                    <h4>{task.title}</h4>
                    <p style={{ fontSize: '0.9rem', color: '#666' }}>{task.description}</p>
                    <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem', fontSize: '0.85rem' }}>
                      <span><strong>Status:</strong> {task.status}</span>
                      <span><strong>Priority:</strong> {task.priority}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p>No tasks found for this project.</p>
            )}
          </div>
        </div>

        <div>
          <div className="card">
            <h3>Documents ({documents.length})</h3>
            {documents.length > 0 ? (
              <div>
                {documents.map(doc => (
                  <div key={doc.id} className="card" style={{ marginBottom: '0.5rem', padding: '0.75rem' }}>
                    <h4>{doc.original_filename || doc.filename}</h4>
                    <div style={{ fontSize: '0.85rem', color: '#666' }}>
                      <div><strong>Type:</strong> {doc.file_type}</div>
                      <div><strong>Size:</strong> {doc.file_size ? `${(doc.file_size / 1024).toFixed(2)} KB` : 'Unknown'}</div>
                      {doc.created_at && (
                        <div><strong>Uploaded:</strong> {new Date(doc.created_at).toLocaleDateString()}</div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p>No documents found for this project.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProjectDetail;

