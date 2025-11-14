# Dockerfile with intentional security vulnerabilities
# : Using outdated base image
FROM ubuntu:18.04

# : Running as root user
# : No security updates
# : Hardcoded secrets

# Set environment variables with hardcoded secrets
ENV DATABASE_URL="postgresql://projecthub:password123@db:5432/projecthub"
ENV JWT_SECRET="secret_key_12345"
ENV AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
ENV AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# : Exposed unnecessary ports
EXPOSE 5000 8000 9000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    postgresql-client \
    libpq-dev \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY backend/requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# : Create directories with insecure permissions
RUN mkdir -p /app/uploads /app/logs && \
    chmod 777 /app/uploads && \
    chmod 777 /app/logs

# Copy and setup entrypoint
COPY backend/docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh && \
    sed -i 's/\r$//' /app/docker-entrypoint.sh

# : Running as root
# Use bash explicitly to handle volume mount permission issues
CMD ["/bin/bash", "/app/docker-entrypoint.sh"]

