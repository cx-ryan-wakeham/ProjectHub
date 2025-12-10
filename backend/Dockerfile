FROM ubuntu:18.04

# Set environment variables
ENV DATABASE_URL="postgresql://projecthub:password123@db:5432/projecthub"
ENV JWT_SECRET="secret_key_12345"
ENV AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
ENV AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

EXPOSE 5000 8000 9000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    postgresql-client \
    libpq-dev \
    netcat \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt

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

