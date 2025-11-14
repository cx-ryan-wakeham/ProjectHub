# ProjectHub - Security Testing Demo Application

**⚠️ WARNING: This application is intentionally designed with security vulnerabilities for educational and security testing purposes only. DO NOT use in production environments.**

ProjectHub is a project management web application that demonstrates common security vulnerabilities found in real-world applications, including all OWASP Top 10 vulnerabilities and additional security flaws.

## Features

- **User Management**: Registration, authentication, role-based access control (admin, project_manager, team_member)
- **Project Management**: Create, update, delete projects with descriptions and status tracking
- **Task Management**: Assign tasks to users, track status, add comments
- **Document Management**: Upload documents with metadata extraction (supports XML, YAML, Pickle, images)
- **Messaging**: Send and receive messages between users
- **Analytics Subsystem**: Advanced analytics and reporting with pandas-powered data processing (SQLAlchemy 2.x patterns)
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
- **ORM**: SQLAlchemy 1.4.0 (via Flask-SQLAlchemy 2.3.2)
- **Data Processing**: pandas 1.1.5
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
│   ├── db_ext.py       # Custom SQLAlchemy extension
│   ├── models.py       # Database models
│   ├── database.py     # Database initialization and seeding
│   ├── auth.py         # Authentication logic
│   ├── config.py       # Configuration (with hardcoded secrets)
│   ├── requirements.txt # Python dependencies
│   ├── docker-entrypoint.sh  # Container startup script
│   ├── analytics/      # Analytics subsystem (SQLAlchemy 2.x patterns)
│   │   ├── __init__.py # Blueprint registration
│   │   ├── routes.py   # Analytics API endpoints
│   │   └── service.py  # Analytics logic with pandas integration
│   ├── routes/         # Route handlers (legacy patterns)
│   │   ├── __init__.py
│   │   ├── api.py      # General API routes (includes user management)
│   │   ├── auth.py     # Authentication routes
│   │   ├── projects.py # Project management routes
│   │   ├── tasks.py    # Task management routes
│   │   ├── documents.py # Document management routes
│   │   ├── messages.py  # Messaging routes
│   │   └── analytics.py # Legacy analytics routes (uses QueryHelper)
│   ├── utils/          # Utility modules
│   │   ├── __init__.py
│   │   ├── logger.py   # Logging configuration
│   │   ├── file_handler.py # File handling utilities
│   │   ├── request_context.py # Request context management
│   │   ├── query_helpers.py # Database query helpers (legacy patterns)
│   │   ├── datetime_utils.py # Datetime utilities
│   │   └── jinja_filters.py # Jinja2 template filters
│   ├── templates/      # HTML templates
│   │   ├── error.html  # Error pages
│   │   └── admin.html  # Admin dashboard
│   ├── tests/          # Test suite
│   │   ├── conftest.py # Test fixtures and configuration
│   │   └── analytics/  # Analytics tests (SQLAlchemy 2.x patterns)
│   │       ├── test_analytics_endpoints.py
│   │       └── test_analytics_service.py
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

This application uses older patterns and APIs that will break when upgrading dependencies. The codebase is designed to force comprehensive refactoring when students attempt to upgrade dependencies to address security vulnerabilities.

### Legacy Pattern Usage Summary

| Pattern | Current Version | Breaking Version | Files Affected | Instances | Migration Complexity |
|---------|----------------|------------------|----------------|-----------|---------------------|
| `Model.query` (SQLAlchemy) | SQLAlchemy 1.4.0 | SQLAlchemy 2.0+ | 10 files | ~83 | **CRITICAL** - Replace with `db.session.execute(select(Model))` |
| `datetime.utcnow()` (Python) | Python 3.6 (Ubuntu 18.04) | Python 3.12+ | 6 files | 13 | **HIGH** - Replace with `datetime.now(timezone.utc)` |
| `_request_ctx_stack` (Flask) | Flask 1.1.4 | Flask 2.0+ | 3 files | 10 | **MEDIUM** - Replace with `g` object |
| `@contextfilter` (Jinja2) | Jinja2 2.11.3 | Jinja2 3.0+ | 1 file | 7 | **MEDIUM** - Replace with `@pass_context` |
| `yaml.load()` without Loader | PyYAML 3.13 | PyYAML 6.0+ | 1 file | 1 | **LOW** - Add `Loader=yaml.SafeLoader` |

### The Dependency Forcing Mechanism

The application includes a **pandas-based forcing mechanism** that creates an unavoidable upgrade cascade:

#### Current State (Stable)
```
SQLAlchemy 1.4.0 + pandas 1.1.5 + Flask-SQLAlchemy 2.3.2
├─ Legacy code: Uses Model.query.* (83 instances) ✓ Works
├─ Analytics: Uses SQLAlchemy 2.x patterns ✓ Works
└─ All features functional ✓
```

#### The Trap: Upgrading pandas
When students attempt to upgrade pandas to address CVEs or get newer features:

```
pandas 1.1.5 → pandas 2.0+
    ↓
FORCES SQLAlchemy >=2.0.0 (hard dependency requirement)
    ↓
SQLAlchemy 2.0 removes Model.query as a class attribute
    ↓
Legacy code breaks: 83 instances of Model.query.* fail
    ↓
Analytics continues working (already uses 2.x patterns)
    ↓
Students must refactor ALL legacy queries to SQLAlchemy 2.x patterns
```

#### Why This Forcing Works

1. **pandas 1.1.5** (current): Compatible with SQLAlchemy 1.4.0
2. **pandas 2.0+** (future): Requires SQLAlchemy >=2.0.0 (hard dependency)
3. **SQLAlchemy 2.0+**: Removes `Model.query` as a class attribute (breaking change)
4. **Analytics code**: Already uses SQLAlchemy 2.x patterns (`select()`, `db.session.execute()`)
5. **Legacy code**: Uses `Model.query.*` in 83 places across 10 files

### Detailed Version Constraints

**SQLAlchemy 1.4.0** (Transitional Version):
- Supports BOTH legacy patterns (`Model.query`) AND 2.x patterns (`select()`)
- Works with Flask-SQLAlchemy 2.3.2
- Works with pandas 1.1.5
- Allows gradual migration between patterns

**pandas Version Requirements**:
- **pandas 1.1.5**: Requires SQLAlchemy >=1.3.0 (satisfied by 1.4.0)
- **pandas 2.0.0+**: Requires SQLAlchemy >=2.0.0 (FORCES upgrade)

**SQLAlchemy 2.0+ Breaking Changes**:
- `Model.query` removed as a class attribute
- Must use `db.session.execute(select(Model))` instead
- All 83 instances of legacy patterns must be migrated
- Requires Flask-SQLAlchemy 3.0+ (additional breaking changes)

### Legacy Code Distribution

Files using `Model.query` patterns:
- `backend/routes/api.py` - 18 instances
- `backend/utils/query_helpers.py` - 19 instances
- `backend/routes/analytics.py` (old) - Uses QueryHelper (legacy)
- `backend/routes/auth.py` - 5 instances
- `backend/routes/messages.py` - 4 instances
- `backend/routes/tasks.py` - 8 instances
- `backend/routes/projects.py` - 7 instances
- `backend/routes/documents.py` - 5 instances
- `backend/database.py` - 13 instances
- `backend/auth.py` - 1 instance
- `backend/app.py` - 3 instances

**Total**: ~83 instances across 10+ files

### Analytics Subsystem (Forward Compatible)

The `backend/analytics/` subsystem is **intentionally built with SQLAlchemy 2.x patterns**:
- Uses `select()` for query construction
- Uses `db.session.execute()` for execution
- Uses `db.session.scalars()` for scalar results
- Uses `db.session.get()` for primary key lookups
- **Zero usage** of `Model.query` patterns

This subsystem:
1. Works correctly on SQLAlchemy 1.4.0 (current)
2. Will continue working on SQLAlchemy 2.0+ (future)
3. Demonstrates the migration target for legacy code
4. Integrates pandas 1.1.5 for data processing

### Forced Refactoring Scenario

When students upgrade pandas:

```bash
# Student action
pip install pandas>=2.0  # To fix CVEs

# Automatic cascade
pip resolver: pandas 2.x requires SQLAlchemy>=2.0
pip resolver: Installing SQLAlchemy 2.0.0

# Result
✗ 83 instances of Model.query.* break
✓ Analytics endpoints continue working
✗ Dashboard, messages, user management fail
✗ Tests fail (except analytics tests)

# Required fix
Refactor all 83 Model.query instances to:
  User.query.all() → db.session.execute(select(User)).scalars().all()
  User.query.get(id) → db.session.get(User, id)
  User.query.filter_by(...).first() → db.session.execute(select(User).filter_by(...)).scalar_one_or_none()
```

### Migration Effort Estimate

- **Time**: 8-12 hours for complete refactoring
- **Files**: 10+ files to modify
- **Instances**: 83 query patterns to update
- **Testing**: Full regression testing required
- **Complexity**: High - requires understanding SQLAlchemy 2.x Core patterns

### Other Breaking Changes

**Python 3.12+**:
- `datetime.utcnow()` is deprecated (13 instances in 6 files)
- Must replace with `datetime.now(timezone.utc)`

**Flask 2.0+**:
- `_request_ctx_stack` removed (10 instances in 3 files)
- Must replace with `g` object or current_app

**Jinja2 3.0+**:
- `@contextfilter` renamed to `@pass_context` (7 filters in 1 file)

**PyYAML 6.0+**:
- `yaml.load()` requires explicit `Loader` parameter (1 instance)

### Educational Value

This design teaches students:
1. **Dependency Management**: Understanding transitive dependencies
2. **Breaking Changes**: How major version upgrades cascade
3. **Technical Debt**: Cost of delaying migrations
4. **Modern Patterns**: SQLAlchemy 2.x Core patterns
5. **Testing**: Importance of comprehensive test coverage
6. **Planning**: Gradual migration strategies (analytics shows the way)

**Note**: These patterns are intentionally designed to create realistic upgrade scenarios found in production systems. The current configuration is stable and functional, but future upgrades require careful planning and significant refactoring effort.

## Analytics Subsystem

ProjectHub includes **two analytics implementations** to demonstrate the difference between legacy and modern patterns:

### Legacy Analytics (`backend/routes/analytics.py`)
- Uses `QueryHelper` class which wraps `Model.query` patterns
- Compatible with current SQLAlchemy 1.4.0
- **Will break** when upgrading to SQLAlchemy 2.0+
- Endpoints: `/api/analytics/stats`, `/api/analytics/search`, `/api/analytics/user/<id>`

### Modern Analytics (`backend/analytics/`)
- Built exclusively with **SQLAlchemy 2.x patterns** and **pandas** integration
- Forward-compatible with SQLAlchemy 2.0+
- Demonstrates migration target for legacy code
- Endpoints: `/analytics/tasks/*`, `/analytics/projects/*`, `/analytics/users/*`, `/analytics/messaging/*`

### Architecture

The modern analytics subsystem is located in `backend/analytics/` and consists of:

- **`service.py`**: Core analytics logic using SQLAlchemy 2.x patterns (`select()`, `db.session.execute()`, `db.session.scalars()`, `db.session.get()`)
- **`routes.py`**: REST API endpoints for accessing analytics data
- **`__init__.py`**: Blueprint registration and module initialization

### Key Features

- **Modern SQLAlchemy Patterns**: All analytics queries use SQLAlchemy 2.x-style syntax with explicit `select()` statements
- **pandas Integration**: Data processing and aggregation powered by pandas DataFrames
- **Real-time Analytics**: Compute metrics on-demand from current database state
- **Comprehensive Testing**: Full test coverage in `tests/analytics/`

### Analytics Endpoints

#### Modern Analytics (SQLAlchemy 2.x + pandas)
All modern analytics endpoints require authentication via JWT token.

**Task Analytics:**
- `GET /analytics/tasks/by-status` - Task counts grouped by status (pending, in_progress, completed)
- `GET /analytics/tasks/average-completion-time` - Average time to complete tasks (in days)
- `GET /analytics/tasks/by-priority` - Task distribution and metrics by priority level

**Project Analytics:**
- `GET /analytics/projects/summary` - Summary of all projects with task counts and percentages
- `GET /analytics/projects/<id>/timeline` - Timeline view of all tasks in a specific project

**User Analytics:**
- `GET /analytics/users/<id>/productivity` - Productivity metrics for a specific user (completion rate, task distribution)

**Messaging Analytics:**
- `GET /analytics/messaging/activity` - Message activity aggregated by date

#### Legacy Analytics (Model.query patterns)
Legacy endpoints that will break on SQLAlchemy 2.0+ upgrade:

- `GET /api/analytics/stats` - Application statistics (requires auth)
- `GET /api/analytics/search?q=<term>` - Search across users and projects (requires auth)
- `GET /api/analytics/user/<id>` - Get user analytics details (requires auth)

### Usage Examples

#### Modern Analytics (Recommended)
```python
import requests

# Get JWT token
login_response = requests.post('http://localhost:5000/api/auth/login', 
    json={'username': 'Admin', 'password': 'Admin'})
token = login_response.json()['token']

# Call modern analytics endpoint
response = requests.get(
    'http://localhost:5000/analytics/tasks/by-status',
    headers={'Authorization': f'Bearer {token}'}
)

data = response.json()
# Returns: {
#   'success': True, 
#   'data': [
#     {'status': 'completed', 'count': 12}, 
#     {'status': 'pending', 'count': 18}, 
#     {'status': 'in_progress', 'count': 9}
#   ]
# }
```

#### Legacy Analytics (Will break on SQLAlchemy 2.0+)
```python
# Call legacy analytics endpoint
response = requests.get(
    'http://localhost:5000/api/analytics/stats',
    headers={'Authorization': f'Bearer {token}'}
)

stats = response.json()
# Returns: {
#   'user_count': 6, 
#   'project_count': 6, 
#   'task_count': 39,
#   ...
# }
```

### Implementation Notes

The analytics subsystem demonstrates modern Python data engineering practices:

1. **SQLAlchemy 2.x Patterns**: No use of legacy `Model.query` syntax
   ```python
   # Modern style used in analytics
   stmt = select(Task.status, func.count(Task.id)).group_by(Task.status)
   result = db.session.execute(stmt).fetchall()
   ```

2. **pandas Processing**: DataFrames for aggregation and transformation
   ```python
   df = pd.DataFrame.from_records(rows, columns=['status', 'count'])
   df['percentage'] = (df['count'] / df['count'].sum() * 100)
   return df.to_dict(orient='records')
   ```

3. **Session-based Queries**: Direct use of `db.session.get()` for lookups
   ```python
   user = db.session.get(User, user_id)
   ```

### Testing

The analytics subsystem includes comprehensive tests in `backend/tests/analytics/`:

- **`test_analytics_endpoints.py`**: API endpoint integration tests
- **`test_analytics_service.py`**: Service layer unit tests with pandas validation

Run tests with:
```bash
cd backend
pytest tests/analytics/
```

### Future Compatibility

The modern analytics subsystem is designed for forward compatibility with future dependency upgrades. It uses SQLAlchemy 2.x patterns that will continue to work when upgrading from SQLAlchemy 1.4.x to 2.0+, unlike legacy code that relies on `Model.query`.

### Summary: Why Two Analytics Implementations?

The dual analytics approach serves an educational purpose:

1. **Legacy Analytics** (`/api/analytics/*`):
   - Shows typical production code using `Model.query`
   - Works fine on SQLAlchemy 1.4.0
   - Will break when pandas upgrade forces SQLAlchemy 2.0+
   
2. **Modern Analytics** (`/analytics/*`):
   - Demonstrates SQLAlchemy 2.x migration target
   - Already compatible with SQLAlchemy 2.0+
   - Proves that the refactored pattern works
   - Integrates pandas for data processing

When students upgrade pandas and break the legacy code, they can:
- See working examples in the modern analytics module
- Compare legacy vs. modern patterns side-by-side
- Use analytics tests as reference for migration
- Learn best practices for modern SQLAlchemy development

### Quick Reference: Legacy vs Modern Patterns

| Component | Path | Pattern | SQLAlchemy 2.0 Compatible? |
|-----------|------|---------|---------------------------|
| **Modern Analytics** | `backend/analytics/` | SQLAlchemy 2.x + pandas | ✅ Yes |
| Analytics Tests | `backend/tests/analytics/` | SQLAlchemy 2.x | ✅ Yes |
| Legacy Analytics | `backend/routes/analytics.py` | Model.query | ❌ No |
| User Routes | `backend/routes/api.py` | Model.query | ❌ No |
| Auth Routes | `backend/routes/auth.py` | Model.query | ❌ No |
| Project Routes | `backend/routes/projects.py` | Model.query | ❌ No |
| Task Routes | `backend/routes/tasks.py` | Model.query | ❌ No |
| Document Routes | `backend/routes/documents.py` | Model.query | ❌ No |
| Message Routes | `backend/routes/messages.py` | Model.query | ❌ No |
| Query Helpers | `backend/utils/query_helpers.py` | Model.query | ❌ No |
| Database Seeding | `backend/database.py` | Model.query | ❌ No |
| Main App | `backend/app.py` | Model.query | ❌ No |

**Total Legacy Instances**: ~83 across 10 files  
**Migration Target**: See `backend/analytics/service.py` for examples

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

