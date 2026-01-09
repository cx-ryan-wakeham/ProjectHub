import React, { useState, useEffect, useCallback } from 'react';
import api from '../services/api';

function UserManagement({ user }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  
  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    password: '',
    role: 'team_member'
  });

  const loadUsers = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get('/v1/users', {
        params: searchQuery ? { search: searchQuery } : {}
      });
      setUsers(response.data.users || []);
    } catch (err) {
      console.error('Error loading users:', err);
      const errorMessage = err.response?.data?.error || 
                           err.response?.statusText || 
                           err.message || 
                           'Failed to load users';
      const statusCode = err.response?.status;
      setError(`Failed to load users${statusCode ? ` (${statusCode})` : ''}: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  }, [searchQuery]);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/v1/users', newUser);
      setUsers([...users, response.data.user]);
      setNewUser({ username: '', email: '', password: '', role: 'team_member' });
      setShowCreateForm(false);
      setError(null);
    } catch (err) {
      console.error('Error creating user:', err);
      setError(err.response?.data?.error || 'Failed to create user');
    }
  };

  const handleUpdateUser = async (e) => {
    e.preventDefault();
    try {
      const updateData = {
        username: editingUser.username,
        email: editingUser.email,
        role: editingUser.role
      };
      
      // Only include password if it's been changed
      if (editingUser.newPassword) {
        updateData.password = editingUser.newPassword;
      }
      
      const response = await api.put(`/v1/users/${editingUser.id}`, updateData);
      setUsers(users.map(u => u.id === editingUser.id ? response.data.user : u));
      setEditingUser(null);
      setError(null);
    } catch (err) {
      console.error('Error updating user:', err);
      setError(err.response?.data?.error || 'Failed to update user');
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
      return;
    }
    
    try {
      await api.delete(`/v1/users/${userId}`);
      setUsers(users.filter(u => u.id !== userId));
      setError(null);
    } catch (err) {
      console.error('Error deleting user:', err);
      setError(err.response?.data?.error || 'Failed to delete user');
    }
  };

  const startEdit = (userToEdit) => {
    setEditingUser({
      ...userToEdit,
      newPassword: ''
    });
    setShowCreateForm(false);
  };

  const cancelEdit = () => {
    setEditingUser(null);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    loadUsers();
  };

  if (loading && users.length === 0) {
    return (
      <div className="container">
        <div className="card">
          <p>Loading users...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2>User Management</h2>
        {!showCreateForm && !editingUser && (
          <button className="button" onClick={() => setShowCreateForm(true)}>
            Create New User
          </button>
        )}
      </div>

      {error && (
        <div className="card" style={{ backgroundColor: '#fee', marginBottom: '1rem', padding: '1rem' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {showCreateForm && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <h3>Create New User</h3>
          <form onSubmit={handleCreateUser}>
            <div className="form-group">
              <label>Username:</label>
              <input
                type="text"
                value={newUser.username}
                onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                required
                style={{ width: '100%', padding: '0.5rem' }}
              />
            </div>
            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                value={newUser.email}
                onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                required
                style={{ width: '100%', padding: '0.5rem' }}
              />
            </div>
            <div className="form-group">
              <label>Password:</label>
              <input
                type="password"
                value={newUser.password}
                onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                required
                style={{ width: '100%', padding: '0.5rem' }}
              />
            </div>
            <div className="form-group">
              <label>Role:</label>
              <select
                value={newUser.role}
                onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                style={{ width: '100%', padding: '0.5rem' }}
              >
                <option value="team_member">Team Member</option>
                <option value="project_manager">Project Manager</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button type="submit" className="button">Create User</button>
              <button type="button" className="button" onClick={() => {
                setShowCreateForm(false);
                setNewUser({ username: '', email: '', password: '', role: 'team_member' });
              }}>
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {editingUser && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <h3>Edit User</h3>
          <form onSubmit={handleUpdateUser}>
            <div className="form-group">
              <label>Username:</label>
              <input
                type="text"
                value={editingUser.username}
                onChange={(e) => setEditingUser({ ...editingUser, username: e.target.value })}
                required
                style={{ width: '100%', padding: '0.5rem' }}
              />
            </div>
            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                value={editingUser.email}
                onChange={(e) => setEditingUser({ ...editingUser, email: e.target.value })}
                required
                style={{ width: '100%', padding: '0.5rem' }}
              />
            </div>
            <div className="form-group">
              <label>New Password (leave blank to keep current):</label>
              <input
                type="password"
                value={editingUser.newPassword || ''}
                onChange={(e) => setEditingUser({ ...editingUser, newPassword: e.target.value })}
                style={{ width: '100%', padding: '0.5rem' }}
              />
            </div>
            <div className="form-group">
              <label>Role:</label>
              <select
                value={editingUser.role}
                onChange={(e) => setEditingUser({ ...editingUser, role: e.target.value })}
                style={{ width: '100%', padding: '0.5rem' }}
              >
                <option value="team_member">Team Member</option>
                <option value="project_manager">Project Manager</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button type="submit" className="button">Update User</button>
              <button type="button" className="button" onClick={cancelEdit}>
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="card">
        <h3>Users ({users.length})</h3>
        
        <form onSubmit={handleSearch} style={{ marginBottom: '1rem' }}>
          <input
            type="text"
            placeholder="Search users..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ width: '70%', padding: '0.5rem', marginRight: '0.5rem' }}
          />
          <button type="submit" className="button">Search</button>
        </form>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #ddd' }}>
                <th style={{ padding: '0.75rem', textAlign: 'left' }}>ID</th>
                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Username</th>
                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Email</th>
                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Role</th>
                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Created</th>
                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map(u => (
                <tr key={u.id} style={{ borderBottom: '1px solid #eee' }}>
                  <td style={{ padding: '0.75rem' }}>{u.id}</td>
                  <td style={{ padding: '0.75rem' }}>{u.username}</td>
                  <td style={{ padding: '0.75rem' }}>{u.email}</td>
                  <td style={{ padding: '0.75rem' }}>
                    <span style={{
                      padding: '0.25rem 0.5rem',
                      borderRadius: '4px',
                      backgroundColor: u.role === 'admin' ? '#e74c3c' : u.role === 'project_manager' ? '#3498db' : '#95a5a6',
                      color: 'white',
                      fontSize: '0.85rem'
                    }}>
                      {u.role}
                    </span>
                  </td>
                  <td style={{ padding: '0.75rem' }}>
                    {u.created_at ? new Date(u.created_at).toLocaleDateString() : 'N/A'}
                  </td>
                  <td style={{ padding: '0.75rem' }}>
                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                      <button
                        className="button"
                        onClick={() => startEdit(u)}
                        style={{ padding: '0.25rem 0.5rem', fontSize: '0.85rem' }}
                      >
                        Edit
                      </button>
                      <button
                        className="button"
                        onClick={() => handleDeleteUser(u.id)}
                        style={{
                          padding: '0.25rem 0.5rem',
                          fontSize: '0.85rem',
                          backgroundColor: '#e74c3c'
                        }}
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {users.length === 0 && (
          <p style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
            No users found.
          </p>
        )}
      </div>
    </div>
  );
}

export default UserManagement;

