# Security Vulnerabilities in ProjectHub

This document lists all intentional security vulnerabilities in ProjectHub for security testing and educational purposes.

## OWASP Top 10 Vulnerabilities

### A1: Injection

**Location**: Multiple endpoints in `backend/routes/`

**Vulnerabilities**:
- SQL Injection in search/filter endpoints (`/api/projects`, `/api/tasks`)
- Raw SQL queries with string interpolation
- Command injection risk in file handling (`backend/utils/file_handler.py`)

**Example**:
```python
# VULNERABLE: SQL Injection
query = f"SELECT * FROM projects WHERE name LIKE '%{search}%'"
```

**Testing**:
- Search for: `' OR '1'='1`
- Search for: `'; DROP TABLE users; --`

### A2: Broken Authentication

**Location**: `backend/routes/auth.py`, `backend/auth.py`

**Vulnerabilities**:
- Weak JWT secret: `"secret_key_12345"`
- JWT tokens never expire (`JWT_EXPIRATION_DELTA = None`)
- No Multi-Factor Authentication (MFA)
- Session fixation (doesn't regenerate session ID)
- Password reset without email verification
- No rate limiting on login attempts
- Weak password hashing (MD5 instead of bcrypt/argon2)
- Passwords logged in plain text

**Testing**:
- Decode JWT tokens at jwt.io
- Try brute force login attempts
- Use expired tokens (they never expire)

### A3: Sensitive Data Exposure

**Location**: All API endpoints, `backend/models.py`

**Vulnerabilities**:
- API responses include password hashes
- API responses include API keys
- No encryption for data in transit (HTTP in dev)
- Environment variables with secrets in code
- Database credentials in configuration files
- Secrets in Terraform outputs

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
- Check API responses for sensitive fields
- Review configuration files for hardcoded secrets

### A4: XML External Entities (XXE)

**Location**: `backend/utils/file_handler.py`, `backend/routes/documents.py`

**Vulnerabilities**:
- XML file processing without XXE protection
- Uses `xml.etree.ElementTree` which doesn't disable external entities
- Can read internal files via XXE

**Example**:
```python
# VULNERABLE: XXE
tree = ET.parse(file_path)  # No protection against external entities
```

**Testing**:
- Upload XML file with: `<!ENTITY xxe SYSTEM "file:///etc/passwd">`

### A5: Broken Access Control

**Location**: All route handlers

**Vulnerabilities**:
- IDOR (Insecure Direct Object References) - users can access other users' resources
- Broken RBAC - non-admins can modify project settings
- No authorization checks on many endpoints
- Misconfigured file permissions (public access to private documents)

**Example**:
```python
# VULNERABLE: IDOR - no access control check
project = Project.query.get(project_id)
# Should check: project.owner_id == user.id or project.is_public
```

**Testing**:
- Access other users' tasks: `/api/tasks/1` (try different IDs)
- Modify projects you don't own
- Download documents you don't have access to

### A6: Security Misconfiguration

**Location**: Multiple files

**Vulnerabilities**:
- Outdated Flask 1.0.0 with known CVEs
- Outdated Docker base images (ubuntu:18.04, alpine:3.8)
- Outdated PostgreSQL (10.0)
- Outdated Node.js (10)
- Outdated Nginx (1.14)
- Missing security headers
- Debug mode enabled in production
- Exposed unnecessary ports
- Running containers as root user

**Files**:
- `backend/requirements.txt`
- `docker/Dockerfile`
- `docker/docker-compose.yml`
- `infrastructure/main.tf`

### A7: Cross-Site Scripting (XSS)

**Location**: Frontend components, backend routes

**Vulnerabilities**:
- Stored XSS in comments, messages, task descriptions
- Reflected XSS in search results
- DOM-based XSS in notification display
- Use of `dangerouslySetInnerHTML` without sanitization
- No Content Security Policy headers

**Example**:
```javascript
// VULNERABLE: XSS
<div dangerouslySetInnerHTML={{ __html: task.description }} />
```

**Testing**:
- Add comment: `<script>alert('XSS')</script>`
- Search for: `<img src=x onerror=alert('XSS')>`

### A8: Insecure Deserialization

**Location**: `backend/utils/file_handler.py`

**Vulnerabilities**:
- Pickle deserialization can execute arbitrary code (RCE)
- YAML deserialization with unsafe loader
- JSON deserialization without validation

**Example**:
```python
# VULNERABLE: RCE via pickle
data = pickle.load(f)  # Can execute malicious code
```

**Testing**:
- Upload malicious pickle file
- Upload malicious YAML file

### A9: Using Components with Known Vulnerabilities

**Location**: `backend/requirements.txt`, `frontend/package.json`, Dockerfiles

**Vulnerabilities**:
- Flask 1.0.0 (multiple CVEs)
- React 16.8.6 (outdated)
- Outdated system packages in Docker images
- No dependency scanning

**Known CVEs**:
- Flask 1.0.0: CVE-2018-1000656, CVE-2019-1010083
- Werkzeug 0.14.1: Multiple vulnerabilities

### A10: Insufficient Logging & Monitoring

**Location**: `backend/utils/logger.py`

**Vulnerabilities**:
- Log injection vulnerabilities (unsanitized user input)
- Sensitive information in logs (passwords, API keys, tokens)
- No log sanitization
- Logs stored insecurely
- No security event monitoring

**Example**:
```python
# VULNERABLE: Log injection, sensitive data
logger.warning(f"Login attempt - Username: {username}, Password: {password}")
```

**Testing**:
- Login with username containing newlines: `user\n[ERROR] Admin login`

## Additional Vulnerabilities

### Hardcoded Secrets

**Location**: Multiple files

- `backend/config.py`: JWT secret, AWS credentials, database passwords
- `docker/Dockerfile`: Environment variables with secrets
- `infrastructure/variables.tf`: AWS credentials, database passwords
- `.github/workflows/ci.yml`: Hardcoded secrets in environment variables

### Insecure File Uploads

**Location**: `backend/routes/documents.py`, `backend/utils/file_handler.py`

**Vulnerabilities**:
- No file type validation (allows php, exe, sh, etc.)
- Path traversal vulnerabilities
- Files stored with world-readable permissions
- No virus scanning
- Executable files can be uploaded

### Path Traversal

**Location**: `backend/routes/documents.py`

**Vulnerabilities**:
- File download doesn't validate file path
- Can access files outside upload directory

**Testing**:
- Download: `/api/documents/1/download?file=../../../etc/passwd`

### Misconfigured Cloud Resources

**Location**: `infrastructure/`

**Vulnerabilities**:
- S3 bucket with public read access
- Excessive IAM permissions (admin access for all roles)
- Security groups open to 0.0.0.0/0
- RDS database publicly accessible
- No encryption at rest for S3
- Terraform state file not encrypted

### CI/CD Vulnerabilities

**Location**: `.github/workflows/ci.yml`

**Vulnerabilities**:
- Hardcoded secrets in workflow files
- Secrets exposed in logs
- No secret scanning
- Insecure artifact storage
- Build args with secrets

### Missing Security Headers

**Location**: `docker/nginx.conf`, Flask app

**Vulnerabilities**:
- No Content Security Policy (CSP)
- No X-Content-Type-Options
- No X-Frame-Options
- No X-XSS-Protection
- No Strict-Transport-Security

### Insecure Token Storage

**Location**: `frontend/src/App.js`, `frontend/src/services/api.js`

**Vulnerabilities**:
- JWT tokens stored in localStorage (XSS risk)
- No token refresh mechanism
- Tokens never expire

### No CSRF Protection

**Location**: All API endpoints

**Vulnerabilities**:
- No CSRF tokens
- CORS allows all origins
- No SameSite cookie attributes

## Testing Checklist

- [ ] SQL Injection in search endpoints
- [ ] XSS in comments, messages, task descriptions
- [ ] IDOR by modifying URL parameters
- [ ] Broken authentication (weak JWT, no expiration)
- [ ] XXE in XML file uploads
- [ ] Path traversal in file downloads
- [ ] Insecure file uploads (executable files)
- [ ] Hardcoded secrets in configuration
- [ ] Sensitive data exposure in API responses
- [ ] Log injection in login attempts
- [ ] Broken access control (modify others' resources)
- [ ] Outdated dependencies with known CVEs

## Remediation Recommendations

For each vulnerability, proper remediation would include:

1. **Injection**: Use parameterized queries, input validation
2. **Authentication**: Strong secrets, token expiration, MFA, rate limiting
3. **Sensitive Data**: Encrypt in transit and at rest, don't expose in responses
4. **XXE**: Use defusedxml, disable external entities
5. **Access Control**: Proper authorization checks, RBAC
6. **Misconfiguration**: Update dependencies, security headers, least privilege
7. **XSS**: Input sanitization, CSP, avoid dangerouslySetInnerHTML
8. **Deserialization**: Avoid pickle, validate YAML/JSON
9. **Dependencies**: Regular updates, dependency scanning
10. **Logging**: Sanitize logs, don't log sensitive data

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

