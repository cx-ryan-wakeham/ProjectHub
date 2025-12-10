#!/bin/bash
# Wait for database to be ready
echo "Waiting for PostgreSQL..."

# Get DB IP from DNS or environment
DB_HOST="${DB_HOST:-db}"

# Try to resolve and connect to database
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    # Try connecting with netcat or python
    if nc -z $DB_HOST 5432 2>/dev/null || python -c "import socket; socket.create_connection(('$DB_HOST', 5432), timeout=2)" 2>/dev/null; then
        echo "PostgreSQL is ready on $DB_HOST!"
        break
    fi
    attempt=$((attempt + 1))
    echo "Attempt $attempt of $max_attempts - PostgreSQL is unavailable on $DB_HOST, sleeping..."
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "Failed to connect to PostgreSQL after $max_attempts attempts"
    exit 1
fi

# Start the application
exec python app.py

