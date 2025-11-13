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
  const [currentPage, setCurrentPage] = useState(1);
  const [pagination, setPagination] = useState({ page: 1, per_page: 10, total: 0, pages: 0 });

  const loadMessages = useCallback(async () => {
    try {
      const response = await api.get('/messages', {
        params: { 
          receiver_id: user.id,
          page: currentPage,
          per_page: 10
        }
      });
      setMessages(response.data.messages || []);
      if (response.data.pagination) {
        setPagination(response.data.pagination);
      }
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  }, [user.id, currentPage]);

  const loadNotifications = useCallback(async () => {
    try {
      const response = await api.get('/messages/notifications');
      const notifications = response.data.notifications || [];
      setNotifications(notifications);
      
      // Auto-mark unread notifications as read when viewing
      const unreadNotifications = notifications.filter(n => !n.is_read);
      if (unreadNotifications.length > 0) {
        // Mark all unread notifications as read
        const markReadPromises = unreadNotifications.map(notif =>
          api.post(`/messages/notifications/${notif.id}/read`).catch(err => {
            console.error(`Error marking notification ${notif.id} as read:`, err);
          })
        );
        await Promise.all(markReadPromises);
        // Reload notifications to get updated read status
        const updatedResponse = await api.get('/messages/notifications');
        setNotifications(updatedResponse.data.notifications || []);
      }
    } catch (error) {
      console.error('Error loading notifications:', error);
    }
  }, []);

  const loadUsers = useCallback(async () => {
    try {
      const response = await api.get('/v1/users');
      setUsers(response.data.users || []);
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
      setCurrentPage(1); // Reset to first page on search
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

            {messages.map(msg => {
              const sender = users.find(u => u.id === msg.sender_id);
              return (
                <div key={msg.id} className="card" style={{ marginBottom: '1rem' }}>
                  <h4>{msg.subject || '(No subject)'}</h4>
                  <div style={{ marginBottom: '0.5rem', color: '#666', fontSize: '0.9rem' }}>
                    <strong>From:</strong> {sender ? sender.username : 'Unknown'}
                  </div>
                  {/* VULNERABLE: XSS - dangerouslySetInnerHTML without sanitization */}
                  <div dangerouslySetInnerHTML={{ __html: msg.content }} />
                  <small style={{ display: 'block', marginTop: '0.5rem', color: '#999' }}>
                    {new Date(msg.created_at).toLocaleString()}
                  </small>
                </div>
              );
            })}
            
            {pagination.pages > 1 && (
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem' }}>
                <button 
                  className="button" 
                  onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                >
                  Previous
                </button>
                <span>Page {pagination.page} of {pagination.pages}</span>
                <button 
                  className="button" 
                  onClick={() => setCurrentPage(p => Math.min(pagination.pages, p + 1))}
                  disabled={currentPage === pagination.pages}
                >
                  Next
                </button>
              </div>
            )}
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
                  borderLeft: notif.is_read ? '4px solid transparent' : '4px solid #3498db',
                  cursor: notif.is_read ? 'default' : 'pointer',
                  position: 'relative'
                }}
                onClick={async () => {
                  if (!notif.is_read) {
                    try {
                      await api.post(`/messages/notifications/${notif.id}/read`);
                      // Update the notification in state
                      setNotifications(prev => 
                        prev.map(n => n.id === notif.id ? { ...n, is_read: true } : n)
                      );
                    } catch (error) {
                      console.error('Error marking notification as read:', error);
                    }
                  }
                }}
              >
                {!notif.is_read && (
                  <span style={{
                    position: 'absolute',
                    top: '0.5rem',
                    right: '0.5rem',
                    fontSize: '0.75rem',
                    color: '#3498db',
                    fontWeight: 'bold'
                  }}>
                    Click to mark as read
                  </span>
                )}
                {/* VULNERABLE: XSS - dangerouslySetInnerHTML without sanitization */}
                <div dangerouslySetInnerHTML={{ __html: notif.message }} />
                <small style={{ display: 'block', marginTop: '0.5rem', color: '#999' }}>
                  {new Date(notif.created_at).toLocaleString()}
                </small>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default MessageCenter;

