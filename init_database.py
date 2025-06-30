#!/usr/bin/env python3
"""
Database Initialization Script for Sanchari Mentors Platform
This script migrates data from JSON files to MongoDB
"""

import json
import os
from pymongo import MongoClient
from datetime import datetime

def load_json_file(filename):
    """Load data from JSON file"""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def init_database():
    """Initialize MongoDB with data from JSON files"""
    
    # MongoDB connection
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/sanchari_mentors')
    mongo_client = MongoClient(MONGO_URI)
    mongo_db = mongo_client.get_default_database()
    
    print("🔄 Initializing database...")
    
    # Load data from JSON files
    users_data = load_json_file('users.json')
    classes_data = load_json_file('classes.json')
    sessions_data = load_json_file('sessions.json')
    
    # Clear existing collections
    mongo_db.users.delete_many({})
    mongo_db.classes.delete_many({})
    mongo_db.sessions.delete_many({})
    
    # Insert users data
    if users_data:
        if isinstance(users_data, dict):
            # Convert dict to list of documents
            users_list = list(users_data.values())
            if users_list:
                mongo_db.users.insert_many(users_list)
                print(f"✅ Inserted {len(users_list)} users")
        else:
            mongo_db.users.insert_many(users_data)
            print(f"✅ Inserted {len(users_data)} users")
    
    # Insert classes data
    if classes_data:
        if isinstance(classes_data, dict):
            # If it's a dict with 'classes' key, extract the classes
            if 'classes' in classes_data:
                classes_list = classes_data['classes']
                if classes_list:
                    mongo_db.classes.insert_many(classes_list)
                    print(f"✅ Inserted {len(classes_list)} classes")
            else:
                # Insert the whole dict as a single document
                mongo_db.classes.insert_one(classes_data)
                print("✅ Inserted classes data")
        else:
            mongo_db.classes.insert_many(classes_data)
            print(f"✅ Inserted {len(classes_data)} classes")
    
    # Insert sessions data
    if sessions_data:
        if isinstance(sessions_data, dict):
            # If it's a dict with 'sessions' key, extract the sessions
            if 'sessions' in sessions_data:
                sessions_list = sessions_data['sessions']
                if sessions_list:
                    mongo_db.sessions.insert_many(sessions_list)
                    print(f"✅ Inserted {len(sessions_list)} sessions")
            else:
                # Insert the whole dict as a single document
                mongo_db.sessions.insert_one(sessions_data)
                print("✅ Inserted sessions data")
        else:
            mongo_db.sessions.insert_many(sessions_data)
            print(f"✅ Inserted {len(sessions_data)} sessions")
    
    # Verify admin user exists
    admin_user = mongo_db.users.find_one({"email": "admin@sanchari.org"})
    if admin_user:
        print("✅ Admin user found in database")
        print(f"   Email: {admin_user['email']}")
        print(f"   Role: {admin_user['role']}")
        print(f"   Password: {admin_user.get('password', 'No password set')}")
    else:
        print("❌ Admin user not found in database")
    
    # Print summary
    print("\n📊 Database Summary:")
    print(f"   Users: {mongo_db.users.count_documents({})}")
    print(f"   Classes: {mongo_db.classes.count_documents({})}")
    print(f"   Sessions: {mongo_db.sessions.count_documents({})}")
    
    print("\n🎉 Database initialization complete!")
    return True

if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        exit(1) 