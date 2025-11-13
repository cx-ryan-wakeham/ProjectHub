import React, { useState } from 'react';
import api from '../services/api';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      if (isRegister) {
        // Register
        const response = await api.post('/auth/register', {
          username,
          email,
          password,
        });
        onLogin(response.data.token, response.data.user);
      } else {
        // Login
        const response = await api.post('/auth/login', {
          username,
          password,
        });
        onLogin(response.data.token, response.data.user);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    }
  };

  return (
    <div className="container" style={{ maxWidth: '400px', marginTop: '100px' }}>
      <div className="card">
        <h2>{isRegister ? 'Register' : 'Login'}</h2>
        {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}
        <form onSubmit={handleSubmit}>
          {isRegister && (
            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          )}
          <div className="form-group">
            <label>Username:</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="button" style={{ width: '100%' }}>
            {isRegister ? 'Register' : 'Login'}
          </button>
        </form>
        <button
          type="button"
          onClick={() => setIsRegister(!isRegister)}
          style={{ marginTop: '1rem', background: 'none', border: 'none', color: '#3498db', cursor: 'pointer' }}
        >
          {isRegister ? 'Already have an account? Login' : "Don't have an account? Register"}
        </button>
      </div>
    </div>
  );
}

export default Login;

