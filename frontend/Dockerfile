# Frontend Dockerfile with intentional security vulnerabilities
FROM node:10  # VULNERABLE: Outdated Node.js version

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# VULNERABLE: Running as root
CMD ["npm", "start"]

