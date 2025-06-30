#!/bin/bash

# Startup script for Sanchari Mentors Platform
# This script initializes the database and starts the Flask application

set -e

echo "🚀 Starting Sanchari Mentors Platform..."

# Wait for MongoDB to be ready
echo "⏳ Waiting for MongoDB to be ready..."
until python -c "
import pymongo
import os
import time
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/sanchari_mentors')
try:
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print('MongoDB is ready!')
    client.close()
except Exception as e:
    print(f'MongoDB not ready: {e}')
    exit(1)
"
do
    echo "MongoDB not ready, waiting 5 seconds..."
    sleep 5
done

# Initialize database
echo "🔄 Initializing database..."
python init_database.py

# Start the Flask application
echo "🌟 Starting Flask application..."
exec python main.py 