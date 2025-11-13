import React, { useState, useEffect } from 'react';
import api from '../services/api';

function DocumentUpload({ user }) {
  const [documents, setDocuments] = useState([]);
  const [projects, setProjects] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedProject, setSelectedProject] = useState('');

  useEffect(() => {
    loadDocuments();
    loadProjects();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await api.get('/documents');
      setDocuments(response.data.documents);
    } catch (error) {
      console.error('Error loading documents:', error);
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

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);
    if (selectedProject) {
      formData.append('project_id', selectedProject);
    }
    formData.append('is_public', 'false');

    try {
      await api.post('/documents', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setSelectedFile(null);
      setSelectedProject('');
      loadDocuments();
    } catch (error) {
      console.error('Error uploading document:', error);
    }
  };

  const handleDownload = async (documentId, filename) => {
    try {
      const response = await api.get(`/documents/${documentId}/download`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error downloading document:', error);
    }
  };

  return (
    <div className="container">
      <h2>Documents</h2>

      <div className="card" style={{ marginBottom: '2rem' }}>
        <h3>Upload Document</h3>
        <form onSubmit={handleUpload}>
          <div className="form-group">
            <label>Select File:</label>
            <input
              type="file"
              onChange={handleFileChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Project (optional):</label>
            <select
              value={selectedProject}
              onChange={(e) => setSelectedProject(e.target.value)}
            >
              <option value="">No project</option>
              {projects.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
          <button type="submit" className="button">Upload</button>
        </form>
      </div>

      <div>
        <h3>All Documents</h3>
        {documents.map(doc => (
          <div key={doc.id} className="card" style={{ marginBottom: '1rem' }}>
            <h4>{doc.original_filename}</h4>
            <p>Size: {(doc.file_size / 1024).toFixed(2)} KB | Type: {doc.file_type}</p>
            <button
              onClick={() => handleDownload(doc.id, doc.original_filename)}
              className="button"
            >
              Download
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DocumentUpload;

