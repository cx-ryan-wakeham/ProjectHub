FROM node:10

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Build the production version
RUN npm run build

# Expose port
EXPOSE 3000

CMD ["npm", "start"]

