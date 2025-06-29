#!/usr/bin/env python3
"""
Test script for Google OAuth configuration
This script tests if the Google OAuth setup is working correctly.
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from flask import Flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        from flask_dance.contrib.google import make_google_blueprint
        print("✅ Flask-Dance Google imported successfully")
    except ImportError as e:
        print(f"❌ Flask-Dance Google import failed: {e}")
        return False
    
    return True

def test_credentials():
    """Test if Google OAuth credentials are configured"""
    print("\n🔑 Testing credentials...")
    
    # Load .env file if it exists
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    
    client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', '')
    
    if not client_id or client_id == 'YOUR_GOOGLE_CLIENT_ID':
        print("❌ GOOGLE_CLIENT_ID not configured")
        return False
    
    if not client_secret or client_secret == 'YOUR_GOOGLE_CLIENT_SECRET':
        print("❌ GOOGLE_CLIENT_SECRET not configured")
        return False
    
    print("✅ Google OAuth credentials are configured")
    print(f"   Client ID: {client_id[:20]}...")
    print(f"   Client Secret: {client_secret[:10]}...")
    
    return True

def test_blueprint_creation():
    """Test if Google OAuth blueprint can be created"""
    print("\n🔧 Testing blueprint creation...")
    
    try:
        from flask_dance.contrib.google import make_google_blueprint
        
        client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
        client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', '')
        
        google_bp = make_google_blueprint(
            client_id=client_id,
            client_secret=client_secret,
            scope=["profile", "email"],
            redirect_url="/login/google/authorized"
        )
        
        print("✅ Google OAuth blueprint created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create Google OAuth blueprint: {e}")
        return False

def test_flask_app():
    """Test if Flask app can be created with Google OAuth"""
    print("\n🌐 Testing Flask app creation...")
    
    try:
        from flask import Flask
        from flask_dance.contrib.google import make_google_blueprint
        
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        
        client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
        client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', '')
        
        google_bp = make_google_blueprint(
            client_id=client_id,
            client_secret=client_secret,
            scope=["profile", "email"],
            redirect_url="/login/google/authorized"
        )
        
        app.register_blueprint(google_bp, url_prefix="/login")
        
        print("✅ Flask app with Google OAuth created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create Flask app with Google OAuth: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 Google OAuth Configuration Test")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Credentials Test", test_credentials),
        ("Blueprint Test", test_blueprint_creation),
        ("Flask App Test", test_flask_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Google OAuth is properly configured.")
        print("\nYou can now run the application:")
        print("python3 main.py")
    else:
        print("❌ Some tests failed. Please check the configuration.")
        print("\nTo set up Google OAuth, run:")
        print("python3 setup_google_oauth.py")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 