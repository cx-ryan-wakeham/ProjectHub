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

## First Time Setup

1. Build and start:
   ```bash
   docker-compose -f docker/docker-compose.yml up -d --build
   ```

2. Wait for database seeding (automatic on first startup)
   - Creates admin user and test users
   - Seeds projects, tasks, comments, messages (100 messages with 50 templates, spanning 6 months)
   - Creates document records

3. Access the application at http://localhost:3000

4. Login with any of the default credentials (see above)

## Re-seeding Database

To reset and re-seed the database (⚠️ deletes all data):

```bash
docker-compose -f docker/docker-compose.yml down -v
docker-compose -f docker/docker-compose.yml up -d
```

**Note**: Seeding only occurs if the database is empty. To skip seeding, set `SKIP_SEED=true` in the backend service environment.

## Key Features

- **User Management** (Admin only): Create, update, delete users at `/users`
- **Messages**: Send and receive messages with pagination (10 per page)
- **Projects**: Create and manage projects
- **Tasks**: Create tasks, add comments
- **Documents**: Upload and download documents
- **Dashboard**: View statistics and project list

## Troubleshooting

**Login issues?**
- Ensure backend is running: `docker-compose -f docker/docker-compose.yml ps`
- Check backend logs: `docker-compose -f docker/docker-compose.yml logs backend`
- Verify database is accessible

**Frontend not loading?**
- Check frontend logs: `docker-compose -f docker/docker-compose.yml logs frontend`
- Ensure frontend compiled successfully (look for "Compiled successfully!")

**Database connection errors?**
- Ensure database container is running
- Check database logs: `docker-compose -f docker/docker-compose.yml logs db`
- Verify credentials match in `backend/config.py`

