// API client with intentional security vulnerabilities
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// VULNERABLE: No CSRF protection
// VULNERABLE: Token stored in localStorage (XSS risk)

api.setToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

// Request interceptor - VULNERABLE: Logs sensitive data
api.interceptors.request.use(
  (config) => {
    // VULNERABLE: Could log sensitive information
    console.log('API Request:', config);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // VULNERABLE: Token in localStorage
      localStorage.removeItem('token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export default api;

