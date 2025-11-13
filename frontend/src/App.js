import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch, Link, Redirect } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import TaskList from './components/TaskList';
import DocumentUpload from './components/DocumentUpload';
import MessageCenter from './components/MessageCenter';
import ProjectDetail from './components/ProjectDetail';
import api from './services/api';
import './index.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // VULNERABLE: Token stored in localStorage (XSS risk)
    const token = localStorage.getItem('token');
    if (token) {
      api.setToken(token);
      // Get user info
      api.get('/auth/me')
        .then(response => {
          setUser(response.data.user);
        })
        .catch(() => {
          localStorage.removeItem('token');
        });
    }
    setLoading(false);
  }, []);

  const handleLogin = (token, userData) => {
    // VULNERABLE: Storing token in localStorage (XSS risk)
    localStorage.setItem('token', token);
    api.setToken(token);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    api.setToken(null);
    setUser(null);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        {user && (
          <header className="header">
            <h1>ProjectHub</h1>
            <nav>
              <Link to="/dashboard">Dashboard</Link>
              <Link to="/tasks">Tasks</Link>
              <Link to="/documents">Documents</Link>
              <Link to="/messages">Messages</Link>
              <span style={{ color: 'white', margin: '0 1rem' }}>Welcome, {user.username}</span>
              <button className="button" onClick={handleLogout}>Logout</button>
            </nav>
          </header>
        )}

        <Switch>
          <Route exact path="/">
            {user ? <Redirect to="/dashboard" /> : <Login onLogin={handleLogin} />}
          </Route>
          <Route path="/dashboard">
            {user ? <Dashboard user={user} /> : <Redirect to="/" />}
          </Route>
          <Route path="/tasks">
            {user ? <TaskList user={user} /> : <Redirect to="/" />}
          </Route>
          <Route path="/documents">
            {user ? <DocumentUpload user={user} /> : <Redirect to="/" />}
          </Route>
          <Route path="/messages">
            {user ? <MessageCenter user={user} /> : <Redirect to="/" />}
          </Route>
          <Route path="/projects/:id">
            {user ? <ProjectDetail user={user} /> : <Redirect to="/" />}
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;

