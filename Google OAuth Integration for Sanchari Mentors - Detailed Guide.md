# Google OAuth Integration for Sanchari Mentors - Detailed Guide

## Overview
This guide will help you set up Google OAuth login for the Sanchari Mentors platform. Google OAuth allows users to log in using their Gmail accounts, providing a secure and convenient authentication method.

## Prerequisites
- A Google account
- Access to Google Cloud Console
- The Sanchari Mentors Flask application running locally

## Step-by-Step Setup

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click "New Project"
4. Enter a project name (e.g., "Sanchari Mentors")
5. Click "Create"

### 2. Enable Google+ API

1. In your new project, go to "APIs & Services" > "Library"
2. Search for "Google+ API" or "Google+ API"
3. Click on "Google+ API"
4. Click "Enable"

### 3. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: "Sanchari Mentors"
   - User support email: Your email
   - Developer contact information: Your email
   - Save and continue through the remaining steps

### 4. Configure OAuth 2.0 Client ID

1. Application type: "Web application"
2. Name: "Sanchari Mentors Web Client"
3. **Authorized redirect URIs**: Add the following:
   - `http://localhost:8000/login/google/authorized`
   - `http://127.0.0.1:8000/login/google/authorized`
4. Click "Create"

### 5. Copy Credentials

After creating the OAuth 2.0 Client ID, you'll see:
- **Client ID**: A long string ending with `.apps.googleusercontent.com`
- **Client Secret**: A shorter string

Copy both of these values.

### 6. Configure the Application

You have two options to configure the credentials:

#### Option A: Environment Variables (Recommended)
Set environment variables before running the application:

```bash
export GOOGLE_CLIENT_ID="102669950361-2do2cq17m4fd9dkoj4da7qiuu3b2snrr.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="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"
python3 main.py
```

#### Option B: Direct Configuration
Edit the `main.py` file and replace the placeholder values:

```python
GOOGLE_CLIENT_ID = 'your_actual_client_id_here'
GOOGLE_CLIENT_SECRET = 'your_actual_client_secret_here'
```

### 7. Test the Integration

1. Start the Flask application: `python3 main.py`
2. Open your browser and go to `http://localhost:8000`
3. Click "Login" and then "Login with Google"
4. You should be redirected to Google's OAuth consent screen
5. After authorizing, you should be redirected back to the application

## Troubleshooting

### Common Issues

1. **"Invalid redirect URI" error**
   - Make sure the redirect URI in Google Cloud Console exactly matches: `http://localhost:8000/login/google/authorized`
   - Check for typos or extra spaces

2. **"Client ID not found" error**
   - Verify that the Client ID is correctly copied from Google Cloud Console
   - Ensure there are no extra spaces or characters

3. **"Access blocked" error**
   - Make sure the Google+ API is enabled in your Google Cloud project
   - Check that your OAuth consent screen is properly configured

4. **"Redirect URI mismatch" error**
   - Add both `http://localhost:8000` and `http://127.0.0.1:8000` variants to authorized redirect URIs

### Security Notes

- Never commit your Client Secret to version control
- Use environment variables for production deployments
- The `OAUTHLIB_INSECURE_TRANSPORT` setting should only be used for local development
- For production, use HTTPS and remove the insecure transport setting

## Production Deployment

For production deployment:

1. Remove or comment out this line in `main.py`:
   ```python
   os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
   ```

2. Add your production domain to authorized redirect URIs in Google Cloud Console:
   - `https://yourdomain.com/login/google/authorized`

3. Use environment variables or a secure configuration management system for credentials

## User Management

When users log in via Google OAuth:
- New users are automatically created with "student" role
- Existing users maintain their current role
- User information (name, email, profile picture) is automatically populated from Google

## Admin Access

To give admin access to a Google user:
1. Log in as an existing admin user
2. Go to Admin > Users
3. Find the Google user by email
4. Change their role to "admin"

## Support

If you encounter issues:
1. Check the Flask application logs for error messages
2. Verify Google Cloud Console settings
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
4. Check that the application is running on the correct port (8000)

