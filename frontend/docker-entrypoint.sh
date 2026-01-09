#!/bin/bash
set -e

# Build the frontend
echo "Building frontend..."
npm run build

# Copy build files to shared volume if it exists
if [ -d "/build-output" ]; then
    echo "Copying build files to shared volume..."
    # Clear destination and copy all files including hidden ones
    rm -rf /build-output/* /build-output/.[!.]* /build-output/..?* 2>/dev/null || true
    cp -r /app/build/. /build-output/
    echo "Build files copied successfully"
    
    # Create a ready file to signal that build is complete
    touch /build-output/.ready
    echo "Build ready signal created"
else
    echo "Warning: /build-output directory not found, build files not copied to shared volume"
fi

# Start the development server (for hot-reload during development)
# In production, this container could exit after building
exec npm start

