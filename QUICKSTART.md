# ProjectHub - Quick Start Guide

## Key Commands

### Build

```bash
# Build all containers
docker-compose -f docker/docker-compose.yml build

# Clean build (no cache)
docker-compose -f docker/docker-compose.yml build --no-cache
```

### Start

```bash
# Start all services in detached mode
docker-compose -f docker/docker-compose.yml up -d

# Build and start in one command
docker-compose -f docker/docker-compose.yml up -d --build
```

### Shutdown

```bash
# Stop services (keeps containers)
docker-compose -f docker/docker-compose.yml stop

# Stop and remove containers
docker-compose -f docker/docker-compose.yml down

# Stop and remove containers + volumes (⚠️ deletes database)
docker-compose -f docker/docker-compose.yml down -v
```

### Useful Commands

```bash
# View logs (all services)
docker-compose -f docker/docker-compose.yml logs -f

# View logs (specific service)
docker-compose -f docker/docker-compose.yml logs -f backend
docker-compose -f docker/docker-compose.yml logs -f frontend

# Check service status
docker-compose -f docker/docker-compose.yml ps

# Restart a service
docker-compose -f docker/docker-compose.yml restart backend
docker-compose -f docker/docker-compose.yml restart frontend

# Rebuild and restart a specific service
docker-compose -f docker/docker-compose.yml up -d --build backend
```

## Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Nginx**: http://localhost:80
- **Database**: localhost:5432

## Default Credentials

- **Admin**: admin@projecthub.com / admin123
- **Developer**: dev@projecthub.com / dev123
- **Manager**: manager@projecthub.com / manager123

## First Time Setup

1. Build and start:
   ```bash
   docker-compose -f docker/docker-compose.yml up -d --build
   ```

2. Wait for database seeding (automatic on first startup)

3. Access the application at http://localhost:3000

## Re-seeding Database

To reset and re-seed the database:

```bash
docker-compose -f docker/docker-compose.yml down -v
docker-compose -f docker/docker-compose.yml up -d
```

