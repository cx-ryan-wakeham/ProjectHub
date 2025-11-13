# ProjectHub - Security Testing Demo Application

**⚠️ WARNING: This application is intentionally designed with security vulnerabilities for educational and security testing purposes only. DO NOT use in production environments.**

ProjectHub is a project management web application that demonstrates common security vulnerabilities found in real-world applications, including all OWASP Top 10 vulnerabilities and additional security flaws.

## Overview

ProjectHub is designed to help security professionals, developers, and students understand and test for common security vulnerabilities. The application includes:

- User authentication and authorization
- Project and task management
- Document upload and sharing
- Messaging and notifications
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
- Python 3.7+
- Node.js 10+
- PostgreSQL (if running locally)

### Running with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd ProjectHub
```

2. Start all services:
```bash
docker-compose -f docker/docker-compose.yml up --build
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Database: localhost:5432

### Default Credentials

- **Admin User**: admin@projecthub.com / admin123
- **Database**: projecthub / password123

## Project Structure

```
ProjectHub/
├── backend/              # Flask backend application
│   ├── app.py          # Main Flask app
│   ├── models.py       # Database models
│   ├── routes/         # Route handlers
│   ├── auth.py         # Authentication logic
│   └── config.py       # Configuration (with hardcoded secrets)
├── frontend/           # React frontend application
│   ├── src/
│   │   ├── components/  # React components
│   │   └── services/     # API client
│   └── package.json
├── docker/             # Docker configuration
│   ├── Dockerfile      # Backend Dockerfile
│   └── docker-compose.yml
├── infrastructure/     # Terraform IaC
│   ├── main.tf        # AWS resources
│   ├── s3.tf          # S3 bucket configuration
│   └── iam.tf         # IAM roles and policies
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
- Insecure file uploads (no validation, dangerous file types)
- Path traversal vulnerabilities
- Misconfigured cloud resources (S3 public access, excessive IAM permissions)
- Hardcoded credentials in CI/CD pipelines
- No Content Security Policy
- Insecure token storage (localStorage)
- No CSRF protection

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

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

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

