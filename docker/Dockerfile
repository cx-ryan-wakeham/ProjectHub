# Dockerfile with intentional security vulnerabilities
# VULNERABLE: Using outdated base image
FROM ubuntu:18.04

# VULNERABLE: Running as root user
# VULNERABLE: No security updates
# VULNERABLE: Hardcoded secrets

# Set environment variables with hardcoded secrets
ENV DATABASE_URL="postgresql://projecthub:password123@db:5432/projecthub"
ENV JWT_SECRET="secret_key_12345"
ENV AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
ENV AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# VULNERABLE: Exposed unnecessary ports
EXPOSE 5000 8000 9000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# VULNERABLE: Create directories with insecure permissions
RUN mkdir -p /app/uploads /app/logs && \
    chmod 777 /app/uploads && \
    chmod 777 /app/logs

# VULNERABLE: Running as root
CMD ["python3", "app.py"]

