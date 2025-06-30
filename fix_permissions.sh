#!/bin/bash

# Fix permissions for Sanchari Mentors Platform
# This script ensures proper permissions for data directories

set -e

echo "Fixing permissions for Sanchari Mentors Platform..."

# Create directories if they don't exist
mkdir -p flask_session
mkdir -p data
mkdir -p static/uploads

# Set proper permissions (777 for maximum compatibility)
chmod -R 777 flask_session
chmod -R 777 data
chmod -R 777 static/uploads

# Set ownership to current user (optional, for better security)
# sudo chown -R $(whoami):$(whoami) flask_session data static/uploads

echo "Permissions fixed successfully!"
echo ""
echo "Directories with 777 permissions:"
echo "  - flask_session/"
echo "  - data/"
echo "  - static/uploads/"
echo ""
echo "You can now run: docker compose up -d" 