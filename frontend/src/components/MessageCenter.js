import React, { useState, useEffect, useCallback } from 'react';
import api from '../services/api';

function MessageCenter({ user }) {
  const [messages, setMessages] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [users, setUsers] = useState([]);
  const [newMessage, setNewMessage] = useState({
    receiver_id: '',
    subject: '',
    content: ''
  });
  const [searchQuery, setSearchQuery] = useState('');

  const loadMessages = useCallback(async () => {
    try {
      const response = await api.get('/messages', {
        params: { receiver_id: user.id }
      });
      setMessages(response.data.messages);
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  }, [user.id]);

  const loadNotifications = useCallback(async () => {
    try {
      const response = await api.get('/messages/notifications');
      setNotifications(response.data.notifications);
    } catch (error) {
      console.error('Error loading notifications:', error);
    }
  }, []);

  const loadUsers = useCallback(async () => {
    try {
      const response = await api.get('/api/v1/users');
      setUsers(response.data.users);
    } catch (error) {
      console.error('Error loading users:', error);
    }
  }, []);

  useEffect(() => {
    loadMessages();
    loadNotifications();
    loadUsers();
  }, [loadMessages, loadNotifications, loadUsers]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    try {
      await api.post('/messages', newMessage);
      setNewMessage({ receiver_id: '', subject: '', content: '' });
      loadMessages();
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      const response = await api.get('/messages/search', {
        params: { q: searchQuery }
      });
      setMessages(response.data.results || []);
    } catch (error) {
      console.error('Error searching messages:', error);
    }
  };

  // VULNERABLE: DOM-based XSS in notification display
  useEffect(() => {
    // VULNERABLE: Direct DOM manipulation with user input
    notifications.forEach(notif => {
      if (!notif.is_read) {
        // VULNERABLE: No sanitization - allows XSS
        const notificationElement = document.getElementById(`notif-${notif.id}`);
        if (notificationElement) {
          notificationElement.innerHTML = notif.message;
        }
      }
    });
  }, [notifications]);

  return (
    <div className="container">
      <h2>Messages & Notifications</h2>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
        <div>
          <div className="card" style={{ marginBottom: '2rem' }}>
            <h3>Send Message</h3>
            <form onSubmit={handleSendMessage}>
              <div className="form-group">
                <label>To:</label>
                <select
                  value={newMessage.receiver_id}
                  onChange={(e) => setNewMessage({ ...newMessage, receiver_id: e.target.value })}
                  required
                >
                  <option value="">Select user</option>
                  {users.filter(u => u.id !== user.id).map(u => (
                    <option key={u.id} value={u.id}>{u.username}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Subject:</label>
                <input
                  type="text"
                  value={newMessage.subject}
                  onChange={(e) => setNewMessage({ ...newMessage, subject: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label>Message:</label>
                <textarea
                  value={newMessage.content}
                  onChange={(e) => setNewMessage({ ...newMessage, content: e.target.value })}
                  rows="4"
                  required
                />
              </div>
              <button type="submit" className="button">Send</button>
            </form>
          </div>

          <div className="card">
            <h3>Inbox</h3>
            <form onSubmit={handleSearch} style={{ marginBottom: '1rem' }}>
              <input
                type="text"
                placeholder="Search messages..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{ width: '70%', padding: '0.5rem', marginRight: '0.5rem' }}
              />
              <button type="submit" className="button">Search</button>
            </form>

            {messages.map(msg => (
              <div key={msg.id} className="card" style={{ marginBottom: '1rem' }}>
                <h4>{msg.subject || '(No subject)'}</h4>
                {/* VULNERABLE: XSS - dangerouslySetInnerHTML without sanitization */}
                <div dangerouslySetInnerHTML={{ __html: msg.content }} />
                <small>{new Date(msg.created_at).toLocaleString()}</small>
              </div>
            ))}
          </div>
        </div>

        <div>
          <div className="card">
            <h3>Notifications</h3>
            {notifications.map(notif => (
              <div
                key={notif.id}
                id={`notif-${notif.id}`}
                className="card"
                style={{
                  marginBottom: '1rem',
                  borderLeft: notif.is_read ? 'none' : '4px solid #3498db'
                }}
              >
                {/* VULNERABLE: XSS - dangerouslySetInnerHTML without sanitization */}
                <div dangerouslySetInnerHTML={{ __html: notif.message }} />
                <small>{new Date(notif.created_at).toLocaleString()}</small>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default MessageCenter;

