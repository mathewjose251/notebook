#!/usr/bin/env python3
"""
Google OAuth Setup Helper for Sanchari Mentors
This script helps you set up Google OAuth credentials for the application.
"""

import os
import sys
import webbrowser
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🔐 Google OAuth Setup for Sanchari Mentors")
    print("=" * 60)
    print()

def print_steps():
    print("📋 Step-by-Step Setup Instructions:")
    print()
    print("1. 🌐 Open Google Cloud Console")
    print("   - Go to: https://console.cloud.google.com/")
    print("   - Sign in with your Google account")
    print()
    
    print("2. 🆕 Create a New Project")
    print("   - Click on the project dropdown at the top")
    print("   - Click 'New Project'")
    print("   - Name it 'Sanchari Mentors'")
    print("   - Click 'Create'")
    print()
    
    print("3. 🔧 Enable Google+ API")
    print("   - Go to 'APIs & Services' > 'Library'")
    print("   - Search for 'Google+ API'")
    print("   - Click on it and click 'Enable'")
    print()
    
    print("4. 🔑 Create OAuth 2.0 Credentials")
    print("   - Go to 'APIs & Services' > 'Credentials'")
    print("   - Click 'Create Credentials' > 'OAuth 2.0 Client IDs'")
    print("   - Configure OAuth consent screen if prompted")
    print()
    
    print("5. ⚙️ Configure OAuth Client")
    print("   - Application type: 'Web application'")
    print("   - Name: 'Sanchari Mentors Web Client'")
    print("   - Authorized redirect URIs:")
    print("     * http://localhost:8000/login/google/authorized")
    print("     * http://127.0.0.1:8000/login/google/authorized")
    print("   - Click 'Create'")
    print()
    
    print("6. 📋 Copy Credentials")
    print("   - Copy the Client ID and Client Secret")
    print("   - Keep them secure and don't share them")
    print()

def open_google_console():
    print("🌐 Opening Google Cloud Console...")
    try:
        webbrowser.open("https://console.cloud.google.com/")
        print("✅ Google Cloud Console opened in your browser")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print("Please manually go to: https://console.cloud.google.com/")

def check_credentials():
    print("\n🔍 Checking current credentials...")
    
    client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', '')
    
    if client_id and client_id != 'YOUR_GOOGLE_CLIENT_ID':
        print("✅ GOOGLE_CLIENT_ID is set")
    else:
        print("❌ GOOGLE_CLIENT_ID is not set")
    
    if client_secret and client_secret != 'YOUR_GOOGLE_CLIENT_SECRET':
        print("✅ GOOGLE_CLIENT_SECRET is set")
    else:
        print("❌ GOOGLE_CLIENT_SECRET is not set")
    
    return client_id and client_secret and client_id != 'YOUR_GOOGLE_CLIENT_ID' and client_secret != 'YOUR_GOOGLE_CLIENT_SECRET'

def set_credentials():
    print("\n🔧 Setting up credentials...")
    
    client_id = input("Enter your Google Client ID: ").strip()
    client_secret = input("Enter your Google Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Both Client ID and Client Secret are required")
        return False
    
    # Create a .env file
    env_content = f"""# Google OAuth Credentials for Sanchari Mentors
GOOGLE_CLIENT_ID={client_id}
GOOGLE_CLIENT_SECRET={client_secret}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Credentials saved to .env file")
        
        # Also set environment variables for current session
        os.environ['GOOGLE_CLIENT_ID'] = client_id
        os.environ['GOOGLE_CLIENT_SECRET'] = client_secret
        print("✅ Environment variables set for current session")
        
        return True
    except Exception as e:
        print(f"❌ Error saving credentials: {e}")
        return False

def test_connection():
    print("\n🧪 Testing Google OAuth connection...")
    
    try:
        # Try to import and initialize Flask-Dance
        from flask_dance.contrib.google import make_google_blueprint
        
        client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
        client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', '')
        
        if not client_id or not client_secret:
            print("❌ Credentials not found")
            return False
        
        # Create blueprint (this will test the credentials)
        google_bp = make_google_blueprint(
            client_id=client_id,
            client_secret=client_secret,
            scope=["profile", "email"],
            redirect_url="/login/google/authorized"
        )
        
        print("✅ Google OAuth configuration is valid")
        return True
        
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")
        return False

def main():
    print_header()
    
    # Check if credentials are already set
    if check_credentials():
        print("\n✅ Google OAuth credentials are already configured!")
        response = input("Do you want to reconfigure them? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup complete!")
            return
    
    print_steps()
    
    # Ask if user wants to open Google Console
    response = input("Do you want to open Google Cloud Console now? (Y/n): ").strip().lower()
    if response != 'n':
        open_google_console()
    
    print("\n" + "=" * 60)
    print("After completing the steps above, come back here to configure the credentials.")
    print("=" * 60)
    
    input("\nPress Enter when you have your Client ID and Client Secret...")
    
    if set_credentials():
        if test_connection():
            print("\n🎉 Google OAuth setup completed successfully!")
            print("\nTo run the application:")
            print("1. Load the environment variables: source .env")
            print("2. Start the application: python3 main.py")
            print("3. Visit: http://localhost:8000")
        else:
            print("\n❌ There was an issue with the credentials. Please check them and try again.")
    else:
        print("\n❌ Failed to set up credentials. Please try again.")

if __name__ == "__main__":
    main() 