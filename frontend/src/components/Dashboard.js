import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Link } from 'react-router-dom';

function Dashboard({ user }) {
  const [projects, setProjects] = useState([]);
  const [stats, setStats] = useState({});
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadProjects();
    loadStats();
  }, []);

  const loadProjects = async () => {
    try {
      const response = await api.get('/projects', {
        params: { search: searchQuery }
      });
      setProjects(response.data.projects);
    } catch (error) {
      console.error('Error loading projects:', error);
    }
  };

  const loadStats = async () => {
    try {
      const response = await api.get('/api/v1/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    loadProjects();
  };

  // VULNERABLE: Reflected XSS in search results
  const highlightSearch = (text) => {
    if (!searchQuery) return text;
    // VULNERABLE: No sanitization - allows XSS
    const regex = new RegExp(`(${searchQuery})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  };

  return (
    <div className="container">
      <h2>Dashboard</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div className="card">
          <h3>Total Users</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.total_users || 0}</p>
        </div>
        <div className="card">
          <h3>Total Projects</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.total_projects || 0}</p>
        </div>
        <div className="card">
          <h3>Total Tasks</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.total_tasks || 0}</p>
        </div>
        <div className="card">
          <h3>Total Documents</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.total_documents || 0}</p>
        </div>
      </div>

      <div className="card">
        <h3>Projects</h3>
        <form onSubmit={handleSearch} style={{ marginBottom: '1rem' }}>
          <input
            type="text"
            placeholder="Search projects..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ width: '70%', padding: '0.5rem', marginRight: '0.5rem' }}
          />
          <button type="submit" className="button">Search</button>
        </form>

        <div>
          {projects.map(project => (
            <div key={project.id} className="card" style={{ marginBottom: '1rem' }}>
              <h4>
                <Link to={`/projects/${project.id}`}>{project.name}</Link>
              </h4>
              {/* VULNERABLE: XSS - dangerouslySetInnerHTML without sanitization */}
              <div dangerouslySetInnerHTML={{ __html: highlightSearch(project.description || '') }} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

