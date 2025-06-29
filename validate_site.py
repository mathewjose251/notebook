#!/usr/bin/env python3
"""
Site Validation Script for Sanchari Mentors Platform
This script validates that all key functionality is working correctly.
"""

import requests
import json
import os
from urllib.parse import urljoin

BASE_URL = "http://localhost:8000"

def test_homepage():
    """Test the homepage loads correctly"""
    print("🏠 Testing homepage...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ Homepage loads successfully")
            return True
        else:
            print(f"❌ Homepage failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Homepage test failed: {e}")
        return False

def test_login_page():
    """Test the login page loads correctly"""
    print("\n🔐 Testing login page...")
    try:
        response = requests.get(f"{BASE_URL}/login")
        if response.status_code == 200:
            print("✅ Login page loads successfully")
            return True
        else:
            print(f"❌ Login page failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Login page test failed: {e}")
        return False

def test_static_files():
    """Test that key static files are accessible"""
    print("\n📁 Testing static files...")
    static_files = [
        "/static/css/mentor-showcase.css",
        "/static/js/mentor-carousel.js"
    ]
    
    all_good = True
    for file_path in static_files:
        try:
            response = requests.get(f"{BASE_URL}{file_path}")
            if response.status_code == 200:
                print(f"✅ {file_path} accessible")
            else:
                print(f"❌ {file_path} failed with status code: {response.status_code}")
                all_good = False
        except Exception as e:
            print(f"❌ {file_path} test failed: {e}")
            all_good = False
    
    return all_good

def test_templates():
    """Test that key templates exist"""
    print("\n📄 Testing templates...")
    template_files = [
        "templates/index.html",
        "templates/login.html",
        "templates/base.html",
        "templates/student/dashboard.html",
        "templates/trainer/dashboard.html",
        "templates/admin/dashboard.html"
    ]
    
    all_good = True
    for template_file in template_files:
        if os.path.exists(template_file):
            print(f"✅ {template_file} exists")
        else:
            print(f"❌ {template_file} missing")
            all_good = False
    
    return all_good

def test_data_files():
    """Test that data files exist and are valid JSON"""
    print("\n📊 Testing data files...")
    data_files = [
        "users.json",
        "classes.json",
        "sessions.json"
    ]
    
    all_good = True
    for data_file in data_files:
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r') as f:
                    json.load(f)
                print(f"✅ {data_file} exists and is valid JSON")
            except json.JSONDecodeError:
                print(f"❌ {data_file} exists but is not valid JSON")
                all_good = False
        else:
            print(f"❌ {data_file} missing")
            all_good = False
    
    return all_good

def test_google_oauth_setup():
    """Test Google OAuth setup"""
    print("\n🔑 Testing Google OAuth setup...")
    
    # Check if setup files exist
    setup_files = [
        "setup_google_oauth.py",
        "test_google_oauth.py",
        "Google OAuth Integration for Sanchari Mentors - Detailed Guide.md"
    ]
    
    all_good = True
    for setup_file in setup_files:
        if os.path.exists(setup_file):
            print(f"✅ {setup_file} exists")
        else:
            print(f"❌ {setup_file} missing")
            all_good = False
    
    # Check if .env file exists (optional)
    if os.path.exists(".env"):
        print("✅ .env file exists (Google OAuth credentials configured)")
    else:
        print("⚠️  .env file not found (Google OAuth needs setup)")
    
    return all_good

def test_routes():
    """Test that key routes are accessible"""
    print("\n🛣️ Testing routes...")
    routes = [
        "/",
        "/login",
        "/student/dashboard",
        "/trainer/dashboard", 
        "/admin/dashboard"
    ]
    
    all_good = True
    for route in routes:
        try:
            response = requests.get(f"{BASE_URL}{route}")
            # We expect 302 redirects for protected routes when not logged in
            if response.status_code in [200, 302]:
                print(f"✅ {route} accessible (status: {response.status_code})")
            else:
                print(f"❌ {route} failed with status code: {response.status_code}")
                all_good = False
        except Exception as e:
            print(f"❌ {route} test failed: {e}")
            all_good = False
    
    return all_good

def test_dummy_login():
    """Test dummy login functionality"""
    print("\n👤 Testing dummy login...")
    try:
        # Test admin login
        login_data = {
            'email': 'admin@sanchari.org',
            'password': 'Admin@2025'
        }
        response = requests.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
        
        if response.status_code == 302:
            print("✅ Dummy admin login works (redirects as expected)")
            return True
        else:
            print(f"❌ Dummy admin login failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dummy login test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 Sanchari Mentors Platform Validation")
    print("=" * 60)
    
    tests = [
        ("Homepage", test_homepage),
        ("Login Page", test_login_page),
        ("Static Files", test_static_files),
        ("Templates", test_templates),
        ("Data Files", test_data_files),
        ("Google OAuth Setup", test_google_oauth_setup),
        ("Routes", test_routes),
        ("Dummy Login", test_dummy_login)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 60)
    print(f"📊 Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The platform is working correctly.")
        print("\n✅ Platform Status:")
        print("   - Homepage: Working")
        print("   - Login System: Working")
        print("   - Templates: All present")
        print("   - Static Files: Accessible")
        print("   - Data Files: Valid")
        print("   - Google OAuth: Ready for setup")
        print("   - Routes: All accessible")
        print("   - Dummy Login: Working")
        
        print("\n🌐 Access your platform at: http://localhost:8000")
        print("🔐 Test with dummy credentials:")
        print("   - Admin: admin@sanchari.org / Admin@2025")
        print("   - Trainer: trainer1@sanchari.org / dummy")
        print("   - Student: student1@sanchari.org / dummy")
        
    else:
        print("❌ Some tests failed. Please check the issues above.")
        print("\n🔧 To fix issues:")
        print("   1. Make sure the Flask app is running: python3 main.py")
        print("   2. Check that all files are in the correct directories")
        print("   3. Verify that port 8000 is not blocked")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 