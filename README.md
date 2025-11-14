# ProjectHub - Security Testing Demo Application

**⚠️ WARNING: This application is intentionally designed with security vulnerabilities for educational and security testing purposes only. DO NOT use in production environments.**

ProjectHub is a project management web application that demonstrates common security vulnerabilities found in real-world applications, including all OWASP Top 10 vulnerabilities and additional security flaws.

## Features

- **User Management**: Registration, authentication, role-based access control (admin, project_manager, team_member)
- **Project Management**: Create, update, delete projects with descriptions and status tracking
- **Task Management**: Assign tasks to users, track status, add comments
- **Document Management**: Upload documents with metadata extraction (supports XML, YAML, Pickle, images)
- **Messaging**: Send and receive messages between users
- **Analytics**: Application statistics and search functionality
- **Admin Dashboard**: HTML-based admin interface for viewing system data
- **Request Tracking**: Request ID generation and logging for all API calls
- **Error Handling**: Custom error pages with request tracking

## Overview

ProjectHub is designed to help security professionals, developers, and students understand and test for common security vulnerabilities. The application includes:

- User authentication and authorization (JWT-based)
- Project and task management with comments
- Document upload and sharing with metadata extraction
- Messaging system between users
- User management (admin functionality)
- Analytics and reporting endpoints
- Admin dashboard (HTML interface)
- RESTful API endpoints
- Request tracking and logging
- Docker containerization
- AWS infrastructure as code (Terraform)
- CI/CD pipeline (GitHub Actions)

## Technology Stack

- **Backend**: Flask 1.1.4
- **Frontend**: React 16.8.6
- **Database**: PostgreSQL 10
- **ORM**: SQLAlchemy (via Flask-SQLAlchemy 2.3.2)
- **Authentication**: JWT (PyJWT 1.6.4, Flask-JWT-Extended 3.13.1)
- **Templates**: Jinja2 2.11.3
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx 1.14
- **Infrastructure**: Terraform (AWS)
- **CI/CD**: GitHub Actions

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.7+ (for local development)
- Node.js 10+ (for local development)
- PostgreSQL (if running locally without Docker)

### Key Commands

#### Build and Start

**Build all containers:**
```bash
docker-compose -f docker/docker-compose.yml build
```

**Build without cache (clean build):**
```bash
docker-compose -f docker/docker-compose.yml build --no-cache
```

**Start all services:**
```bash
docker-compose -f docker/docker-compose.yml up -d
```

**Build and start in one command:**
```bash
docker-compose -f docker/docker-compose.yml up -d --build
```

#### Shutdown

**Stop all services (keeps containers):**
```bash
docker-compose -f docker/docker-compose.yml stop
```

**Stop and remove containers:**
```bash
docker-compose -f docker/docker-compose.yml down
```

**Stop and remove containers + volumes (⚠️ deletes database data):**
```bash
docker-compose -f docker/docker-compose.yml down -v
```

#### Useful Commands

**View logs:**
```bash
# All services
docker-compose -f docker/docker-compose.yml logs -f

# Specific service
docker-compose -f docker/docker-compose.yml logs -f backend
docker-compose -f docker/docker-compose.yml logs -f frontend
```

**Check service status:**
```bash
docker-compose -f docker/docker-compose.yml ps
```

**Restart a specific service:**
```bash
docker-compose -f docker/docker-compose.yml restart backend
docker-compose -f docker/docker-compose.yml restart frontend
```

### Running with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd ProjectHub
```

2. Build and start all services:
```bash
docker-compose -f docker/docker-compose.yml up -d --build
```

3. Wait for services to initialize (database seeding happens automatically on first startup)

4. Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Admin Dashboard**: http://localhost:5000/admin
- **API Health Check**: http://localhost:5000/api/health
- **Nginx (Production)**: http://localhost:80
- **Database**: localhost:5432

### Database Seeding

The application automatically seeds the database with test data on first startup. This includes:
- Test users (admin and team members)
- Sample projects
- Tasks and comments
- Messages (100 messages with 50 unique templates, spanning 6 months)
- Document records

**Note**: Seeding only occurs if the database is empty. To re-seed, remove the database volume:
```bash
docker-compose -f docker/docker-compose.yml down -v
docker-compose -f docker/docker-compose.yml up -d
```

To skip seeding, set the environment variable `SKIP_SEED=true` in the backend service.

### Default Credentials

**Application Users** (seeded automatically):
- **Admin**: admin@projecthub.com / Admin (admin role) - password: `Admin`
- **Alice**: alice@projecthub.com / Alice (project_manager role) - password: `Alice`
- **Bob**: bob@projecthub.com / Bob (team_member role) - password: `Bob`
- **Charlie**: charlie@projecthub.com / Charlie (team_member role) - password: `Charlie`
- **Diana**: diana@projecthub.com / Diana (team_member role) - password: `Diana`
- **Eve**: eve@projecthub.com / Eve (project_manager role) - password: `Eve`

**Note**: Login accepts either username or email (case-insensitive). Passwords match the capitalized username (e.g., username "Alice" has password "Alice").

**Database**:
- **User**: projecthub
- **Password**: password123
- **Database**: projecthub

## Project Structure

```
ProjectHub/
├── backend/              # Flask backend application
│   ├── app.py          # Main Flask app
│   ├── models.py       # Database models
│   ├── database.py     # Database initialization and seeding
│   ├── auth.py         # Authentication logic
│   ├── config.py       # Configuration (with hardcoded secrets)
│   ├── requirements.txt # Python dependencies
│   ├── docker-entrypoint.sh  # Container startup script
│   ├── routes/         # Route handlers
│   │   ├── __init__.py
│   │   ├── api.py      # General API routes (includes user management)
│   │   ├── auth.py     # Authentication routes
│   │   ├── projects.py # Project management routes
│   │   ├── tasks.py    # Task management routes
│   │   ├── documents.py # Document management routes
│   │   ├── messages.py  # Messaging routes
│   │   └── analytics.py # Analytics and reporting routes
│   ├── utils/          # Utility modules
│   │   ├── __init__.py
│   │   ├── logger.py   # Logging configuration
│   │   ├── file_handler.py # File handling utilities
│   │   ├── request_context.py # Request context management
│   │   ├── query_helpers.py # Database query helpers
│   │   ├── datetime_utils.py # Datetime utilities
│   │   └── jinja_filters.py # Jinja2 template filters
│   ├── templates/      # HTML templates
│   │   ├── error.html  # Error pages
│   │   └── admin.html  # Admin dashboard
│   ├── uploads/        # Uploaded files directory
│   └── logs/           # Application logs directory
├── frontend/           # React frontend application
│   ├── src/
│   │   ├── components/  # React components
│   │   │   ├── Dashboard.js
│   │   │   ├── Login.js
│   │   │   ├── TaskList.js
│   │   │   ├── MessageCenter.js
│   │   │   ├── DocumentUpload.js
│   │   │   ├── ProjectDetail.js
│   │   │   └── UserManagement.js
│   │   ├── services/     # API client
│   │   │   └── api.js
│   │   ├── App.js       # Main React component
│   │   ├── index.js     # Entry point
│   │   └── index.css    # Global styles
│   ├── public/
│   │   └── index.html   # HTML template
│   ├── Dockerfile      # Frontend Dockerfile
│   └── package.json    # Node.js dependencies
├── docker/             # Docker configuration
│   ├── Dockerfile      # Backend Dockerfile
│   ├── docker-compose.yml # Service orchestration
│   └── nginx.conf      # Nginx reverse proxy config
├── infrastructure/     # Terraform IaC
│   ├── main.tf        # AWS resources
│   ├── s3.tf          # S3 bucket configuration
│   ├── iam.tf          # IAM roles and policies
│   ├── variables.tf   # Terraform variables
│   └── outputs.tf     # Terraform outputs
├── .github/
│   └── workflows/
│       └── ci.yml      # GitHub Actions CI/CD
├── README.md          # This file
├── QUICKSTART.md      # Quick start guide
├── LICENSE            # License file
├── openapi.yaml       # OpenAPI specification
└── get-docker.sh      # Docker installation helper script
```

## Security Vulnerabilities

This application intentionally contains numerous security vulnerabilities for educational and security testing purposes. The application demonstrates common security flaws found in real-world applications.

### High-Level Summary

The application includes vulnerabilities across all OWASP Top 10 categories:

- **Injection vulnerabilities** (SQL injection, command injection, XXE)
- **Broken authentication and session management** (weak secrets, no expiration, case-insensitive login)
- **Sensitive data exposure** (passwords, API keys, tokens exposed in API responses and logs)
- **Broken access control** (IDOR, misconfigured RBAC, unauthorized access)
- **Security misconfiguration** (outdated dependencies, insecure defaults, missing security headers)
- **Cross-site scripting (XSS)** (stored, reflected, DOM-based)
- **Insecure deserialization** (pickle, YAML, JSON)
- **Using components with known vulnerabilities** (outdated packages with CVEs)
- **Insufficient logging and monitoring** (log injection, sensitive data in logs)
- **Additional security weaknesses** (hardcoded secrets, insecure file uploads, path traversal, no CSRF protection, weak password hashing)

## Breaking Changes on Dependency Upgrades

This application uses older patterns and APIs that will break when upgrading dependencies. The following table summarizes the breaking changes:

| Pattern | Current Version | Breaking Version | Files Affected | Instances | Migration Complexity |
|---------|----------------|------------------|----------------|-----------|---------------------|
| `Model.query` (SQLAlchemy) | SQLAlchemy 1.4.x (pinned, via Flask-SQLAlchemy 2.3.2) | SQLAlchemy 2.0+ | 10+ files | 100+ | **SIGNIFICANT** - Replace with `db.session.query(Model)` |
| `datetime.utcnow()` (Python) | Python 3.6 (Ubuntu 18.04 default) | Python 3.12+ | 8+ files | 18+ | **HIGH** - Replace with `datetime.now(timezone.utc)` |
| `_request_ctx_stack` (Flask) | Flask 1.1.4 | Flask 2.0+ | 4+ files | 10+ | **MEDIUM** - Replace with `g` object |
| `@contextfilter` (Jinja2) | Jinja2 2.11.3 | Jinja2 3.0+ | 2 files | 7 filters | **MEDIUM** - Replace with `@pass_context` |
| `yaml.load()` without Loader (PyYAML) | PyYAML 3.13 | PyYAML 6.0+ | 1 file | 1 | **LOW** - Add `Loader=yaml.SafeLoader` |

**Version Details:**
- **SQLAlchemy**: SQLAlchemy is pinned to `<2.0,>=1.4.0` in requirements.txt to work with Flask-SQLAlchemy 2.3.2. The `Model.query` pattern works in SQLAlchemy 1.4.x but is **removed** in SQLAlchemy 2.0+. Upgrading to SQLAlchemy 2.0+ will break all `Model.query` usage (100+ instances). This pattern must be migrated to `db.session.query(Model)` or `db.session.get(Model, id)` before upgrading.
- **Python**: Ubuntu 18.04 includes Python 3.6. `datetime.utcnow()` is deprecated in Python 3.12 and will be removed in future versions.
- **Flask**: Version 1.1.4 uses `_request_ctx_stack` which is removed in Flask 2.0+ (replaced with `g` object).
- **Jinja2**: Version 2.11.3 uses `@contextfilter` which is replaced with `@pass_context` in Jinja2 3.0+.
- **PyYAML**: Version 3.13 allows `yaml.load()` without Loader (with security warnings). PyYAML 6.0+ removes this unsafe default.

**Note**: These patterns are intentionally used throughout the codebase to create realistic technical debt scenarios for upgrade testing. The current versions work correctly, but upgrading to the breaking versions will require refactoring.

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/reset-password` - Password reset

### Projects
- `GET /api/projects` - List all projects (with search)
- `GET /api/projects/<id>` - Get project details
- `POST /api/projects` - Create project
- `PUT /api/projects/<id>` - Update project
- `DELETE /api/projects/<id>` - Delete project
- `GET /api/projects/<id>/tasks` - Get project tasks

### Tasks
- `GET /api/tasks` - List all tasks (with filters)
- `GET /api/tasks/<id>` - Get task details
- `POST /api/tasks` - Create task
- `PUT /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task
- `GET /api/tasks/<id>/comments` - Get task comments
- `POST /api/tasks/<id>/comments` - Add comment to task

### Documents
- `GET /api/documents` - List all documents
- `GET /api/documents/<id>` - Get document details
- `POST /api/documents` - Upload document
- `PUT /api/documents/<id>` - Update document
- `DELETE /api/documents/<id>` - Delete document
- `GET /api/documents/<id>/download` - Download document

### Messages
- `GET /api/messages` - List messages (sent/received)
- `GET /api/messages/<id>` - Get message details
- `POST /api/messages` - Send message
- `DELETE /api/messages/<id>` - Delete message
- `GET /api/messages/search` - Search messages

### Analytics
- `GET /api/analytics/stats` - Get application statistics
- `GET /api/analytics/search` - Search across users and projects
- `GET /api/analytics/user/<id>` - Get user analytics

### General API
- `GET /api/v1/users` - List all users (with search)
- `GET /api/v1/users/<id>` - Get user details
- `POST /api/v1/users` - Create user
- `PUT /api/v1/users/<id>` - Update user
- `DELETE /api/v1/users/<id>` - Delete user
- `GET /api/v1/stats` - Get statistics
- `GET /api/v1/search` - Global search

### Other
- `GET /` - API information
- `GET /api/health` - Health check
- `GET /admin` - Admin dashboard (HTML)

## Testing the Vulnerabilities

### SQL Injection

Try searching for projects with:
```
' OR '1'='1
```

Or in the users endpoint:
```
GET /api/v1/users?search=' OR '1'='1
```

### XSS

Try adding a comment with:
```html
<script>alert('XSS')</script>
```

### IDOR

Access other users' resources by modifying URL parameters:
```
GET /api/tasks/1  (try different IDs)
GET /api/documents/1
GET /api/messages/1
```

### Broken Authentication

JWT tokens never expire and use a weak secret. Try decoding tokens at jwt.io. Tokens are stored in localStorage and can be accessed via browser console.

## Development

### Local Development (without Docker)

#### Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Set environment variables (or use .env file)
export DATABASE_URL=postgresql://projecthub:password123@localhost:5432/projecthub
export JWT_SECRET=secret_key_12345

# Initialize database
python -c "from database import init_db; from app import app; init_db(app)"

# Run the application
python app.py
```

The backend will be available at http://localhost:5000

#### Frontend Setup

```bash
cd frontend
npm install

# Set API URL (or edit src/services/api.js)
export REACT_APP_API_URL=http://localhost:5000/api

# Run the development server
npm start
```

The frontend will be available at http://localhost:3000

### Docker Development

For development with hot-reload, the docker-compose.yml includes volume mounts that sync your local code changes into the containers. Simply edit files locally and the changes will be reflected in the running containers (frontend may require a page refresh).

## Infrastructure Deployment

⚠️ **Warning**: The Terraform configuration contains intentional misconfigurations. Do not deploy to production.

```bash
cd infrastructure
terraform init
terraform plan
terraform apply
```

## Contributing

This is a security testing demo application. Contributions should focus on adding more realistic vulnerabilities or improving documentation.

## License

MIT License - See LICENSE file for details

## Disclaimer

This software is provided for educational and security testing purposes only. The authors are not responsible for any misuse of this software. Use at your own risk.

