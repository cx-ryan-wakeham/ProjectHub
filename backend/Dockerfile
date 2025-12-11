FROM python:3.11-slim

# Set environment variables
ENV DATABASE_URL="postgresql://projecthub:password123@db:5432/projecthub"
ENV JWT_SECRET="secret_key_12345"
ENV AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
ENV AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

EXPOSE 5000 8000 9000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    netcat-openbsd \
    dos2unix \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Fix line endings and permissions
RUN dos2unix /app/*.sh 2>/dev/null || true && \
    dos2unix /app/docker-entrypoint.sh && \
    chmod +x /app/docker-entrypoint.sh && \
    mkdir -p /app/uploads /app/logs && \
    chmod 777 /app/uploads && \
    chmod 777 /app/logs

# Use bash explicitly to handle volume mount permission issues
CMD ["/bin/bash", "/app/docker-entrypoint.sh"]

