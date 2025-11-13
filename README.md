# ProjectHub - Security Testing Demo Application

**⚠️ WARNING: This application is intentionally designed with security vulnerabilities for educational and security testing purposes only. DO NOT use in production environments.**

ProjectHub is a project management web application that demonstrates common security vulnerabilities found in real-world applications, including all OWASP Top 10 vulnerabilities and additional security flaws.

## Overview

ProjectHub is designed to help security professionals, developers, and students understand and test for common security vulnerabilities. The application includes:

- User authentication and authorization
- Project and task management
- Document upload and sharing
- Messaging system
- User management (admin)
- RESTful API endpoints
- Docker containerization
- AWS infrastructure as code (Terraform)
- CI/CD pipeline (GitHub Actions)

## Technology Stack

- **Backend**: Flask 1.0.0 (intentionally outdated)
- **Frontend**: React 16.8.6
- **Database**: PostgreSQL
- **Containerization**: Docker
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
- **Admin**: admin@projecthub.com / Admin (password is same as username, capitalized)
- **Alice**: alice@projecthub.com / Alice (project_manager)
- **Bob**: bob@projecthub.com / Bob (team_member)
- **Charlie**: charlie@projecthub.com / Charlie (team_member)
- **Diana**: diana@projecthub.com / Diana (team_member)
- **Eve**: eve@projecthub.com / Eve (project_manager)

**Note**: Login is case-insensitive (you can use `admin`, `Admin`, or `ADMIN`), but passwords match the capitalized username.

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
│   ├── docker-entrypoint.sh  # Container startup script
│   ├── routes/         # Route handlers
│   │   ├── api.py      # General API routes (includes user management)
│   │   ├── auth.py      # Authentication routes
│   │   ├── projects.py # Project management routes
│   │   ├── tasks.py    # Task management routes
│   │   ├── documents.py # Document management routes
│   │   └── messages.py  # Messaging routes
│   └── utils/          # Utility modules
│       ├── logger.py   # Logging configuration
│       └── file_handler.py # File handling utilities
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
│   │   └── index.js     # Entry point
│   ├── Dockerfile      # Frontend Dockerfile
│   └── package.json
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
└── .github/
    └── workflows/
        └── ci.yml      # GitHub Actions CI/CD
```

## Security Vulnerabilities

This application intentionally contains numerous security vulnerabilities. See [SECURITY.md](SECURITY.md) for a complete list.

### OWASP Top 10

1. **A1: Injection** - SQL injection in search/filter endpoints
2. **A2: Broken Authentication** - Weak JWT, no MFA, session fixation
3. **A3: Sensitive Data Exposure** - API responses expose passwords/tokens
4. **A4: XXE** - XML External Entity vulnerabilities in file uploads
5. **A5: Broken Access Control** - IDOR, misconfigured RBAC
6. **A6: Security Misconfiguration** - Outdated dependencies, Docker images
7. **A7: XSS** - Stored, reflected, and DOM-based XSS
8. **A8: Insecure Deserialization** - Pickle, JSON, YAML deserialization
9. **A9: Known Vulnerabilities** - Outdated Flask, React, Docker images
10. **A10: Insufficient Logging** - Log injection, sensitive data in logs

### Additional Vulnerabilities

- Hardcoded secrets in configuration files
- Insecure file uploads (no validation, dangerous file types: php, exe, sh, etc.)
- Path traversal vulnerabilities
- Misconfigured cloud resources (S3 public access, excessive IAM permissions)
- Hardcoded credentials in CI/CD pipelines
- No Content Security Policy
- Insecure token storage (localStorage - XSS risk)
- No CSRF protection
- Case-insensitive authentication (allows enumeration)
- Weak password hashing (MD5)
- Log injection vulnerabilities
- Sensitive data in logs (passwords, API keys, JWT secrets)
- Broken access control in user management (any user can create/update/delete users)
- No input validation or sanitization

## Testing the Vulnerabilities

### SQL Injection

Try searching for projects with:
```
' OR '1'='1
```

### XSS

Try adding a comment with:
```html
<script>alert('XSS')</script>
```

### IDOR

Access other users' resources by modifying URL parameters:
```
/api/tasks/1  (try different IDs)
```

### Broken Authentication

JWT tokens never expire and use a weak secret. Try decoding tokens at jwt.io.

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

