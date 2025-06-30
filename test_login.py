#!/usr/bin/env python3
"""
Test script for login functionality
This script tests the database functions and login process
"""

import os
import sys
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the database functions from main.py
from main import get_collection_data, set_collection_data

def test_login_functionality():
    """Test the login functionality"""
    print("🧪 Testing Login Functionality")
    print("=" * 50)
    
    # Test 1: Check if users data can be loaded
    print("\n👥 Testing Users Data Loading:")
    try:
        users_data = get_collection_data('users', 'email')
        print(f"   Users data type: {type(users_data)}")
        print(f"   Number of users: {len(users_data) if isinstance(users_data, dict) else len(users_data)}")
        
        # Check if admin user exists
        if isinstance(users_data, dict):
            admin_user = users_data.get('admin@sanchari.org')
            if admin_user:
                print("   ✅ Admin user found")
                print(f"   Admin name: {admin_user.get('name')}")
                print(f"   Admin role: {admin_user.get('role')}")
                print(f"   Admin password: {admin_user.get('password')}")
            else:
                print("   ❌ Admin user not found")
        else:
            # Convert list to dict for testing
            users_dict = {user.get('email'): user for user in users_data if user.get('email')}
            admin_user = users_dict.get('admin@sanchari.org')
            if admin_user:
                print("   ✅ Admin user found (from list)")
                print(f"   Admin name: {admin_user.get('name')}")
                print(f"   Admin role: {admin_user.get('role')}")
                print(f"   Admin password: {admin_user.get('password')}")
            else:
                print("   ❌ Admin user not found")
                
    except Exception as e:
        print(f"   ❌ Error loading users data: {e}")
    
    # Test 2: Test login credentials
    print("\n🔐 Testing Login Credentials:")
    try:
        users_data = get_collection_data('users', 'email')
        
        # Handle case where users_data might be a list or dict
        if isinstance(users_data, list):
            # Convert list to dict keyed by email
            users_data = {user.get('email'): user for user in users_data if user.get('email')}
        
        # Test admin login
        admin_email = 'admin@sanchari.org'
        admin_password = 'Admin@2025'
        
        user = users_data.get(admin_email) if isinstance(users_data, dict) else None
        
        if user:
            if user.get('password') == admin_password:
                print("   ✅ Admin login credentials are correct")
                print(f"   User role: {user.get('role')}")
                print(f"   User name: {user.get('name')}")
            else:
                print("   ❌ Admin password is incorrect")
                print(f"   Expected: {admin_password}")
                print(f"   Found: {user.get('password')}")
        else:
            print("   ❌ Admin user not found")
            
    except Exception as e:
        print(f"   ❌ Error testing login: {e}")
    
    # Test 3: Test other users
    print("\n👤 Testing Other Users:")
    try:
        users_data = get_collection_data('users', 'email')
        
        # Handle case where users_data might be a list or dict
        if isinstance(users_data, list):
            # Convert list to dict keyed by email
            users_data = {user.get('email'): user for user in users_data if user.get('email')}
        
        test_users = [
            ('trainer1@sanchari.org', 'dummy', 'trainer'),
            ('student1@sanchari.org', 'dummy', 'student')
        ]
        
        for email, password, expected_role in test_users:
            user = users_data.get(email) if isinstance(users_data, dict) else None
            if user:
                if user.get('password') == password and user.get('role') == expected_role:
                    print(f"   ✅ {email} - {expected_role} - credentials correct")
                else:
                    print(f"   ❌ {email} - credentials or role incorrect")
            else:
                print(f"   ❌ {email} - user not found")
                
    except Exception as e:
        print(f"   ❌ Error testing other users: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Login functionality test completed!")

if __name__ == "__main__":
    test_login_functionality() 