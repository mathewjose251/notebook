# Google OAuth Setup Guide for Sanchari Mentors Platform

## Overview
This guide explains how to properly configure Google OAuth for both development and production environments.

## Problem
You're seeing these errors in Google Cloud Console:
- "Invalid Redirect: must end with a public top-level domain (such as .com or .org)"
- "Invalid Redirect: must use a domain that is a valid top private domain"

This happens because Google OAuth requires proper domain names for redirect URIs, not IP addresses.

## Solutions

### Option 1: Use a Custom Domain (Recommended for Production)

1. **Register a Domain Name**
   - Register a domain like `sanchari-mentors.com` or `your-app.com`
   - Point it to your GCP VM's IP address (35.231.94.15)

2. **Update Google Cloud Console**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Navigate to "APIs & Services" > "Credentials"
   - Edit your OAuth 2.0 Client ID
   - Add these Authorized redirect URIs:
     ```
     https://your-domain.com/login/google/authorized
     https://www.your-domain.com/login/google/authorized
     ```

3. **Update Environment Variables**
   ```bash
   export GOOGLE_OAUTH_REDIRECT_URL=https://your-domain.com
   ```

### Option 2: Use a Free Domain Service (Quick Solution)

1. **Use a Free Domain Service**
   - [No-IP](https://www.noip.com/) - Free dynamic DNS
   - [DuckDNS](https://www.duckdns.org/) - Free subdomain
   - [Freenom](https://www.freenom.com/) - Free domain names

2. **Example with DuckDNS**
   - Go to [DuckDNS](https://www.duckdns.org/)
   - Create a free subdomain like `sanchari-mentors.duckdns.org`
   - Point it to your IP: 35.231.94.15

3. **Update Google Cloud Console**
   - Add these redirect URIs:
     ```
     https://sanchari-mentors.duckdns.org/login/google/authorized
     ```

### Option 3: Disable OAuth for Now (Temporary Solution)

If you want to deploy without OAuth for now:

1. **Update main.py**
   ```python
   # Comment out or remove the Google OAuth setup
   # google_bp = make_google_blueprint(...)
   # app.register_blueprint(google_bp, url_prefix="/login")
   ```

2. **Use Regular Login**
   - Users can still register and login with email/password
   - OAuth can be added later when you have a proper domain

## Step-by-Step Setup for Production

### 1. Get a Domain Name
```bash
# Example: Register sanchari-mentors.com
# Point DNS A record to: 35.231.94.15
```

### 2. Update Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Go to "APIs & Services" > "Credentials"
4. Click on your OAuth 2.0 Client ID
5. Under "Authorized redirect URIs", add:
   ```
   https://sanchari-mentors.com/login/google/authorized
   https://www.sanchari-mentors.com/login/google/authorized
   ```
6. Click "Save"

### 3. Update Your VM Environment
```bash
# SSH into your VM
ssh your-username@35.231.94.15

# Update environment variables
sudo nano /etc/environment
# Add:
GOOGLE_OAUTH_REDIRECT_URL=https://sanchari-mentors.com

# Or update your .env file
sudo nano /path/to/your/app/.env
# Add:
GOOGLE_OAUTH_REDIRECT_URL=https://sanchari-mentors.com

# Restart your application
sudo systemctl restart your-app-service
```

### 4. Test the Setup
1. Visit your domain: `https://sanchari-mentors.com`
2. Try the Google login button
3. Check that you're redirected back properly

## Development Setup

For local development, you can use:
```
http://localhost:8000/login/google/authorized
```

## Troubleshooting

### Common Issues:

1. **"Invalid Redirect URI" Error**
   - Make sure the redirect URI in your code matches exactly what's in Google Cloud Console
   - Check for trailing slashes, http vs https, etc.

2. **"Redirect URI Mismatch" Error**
   - The redirect URI in your request doesn't match any authorized redirect URIs
   - Double-check both the code and Google Cloud Console settings

3. **"Access Blocked" Error**
   - Your app might not be verified by Google
   - For testing, add your email as a test user in Google Cloud Console

### Debug Steps:

1. **Check Current Redirect URI**
   ```python
   # In your main.py, add this debug line:
   print(f"OAuth Redirect URL: {GOOGLE_OAUTH_REDIRECT_URL}/login/google/authorized")
   ```

2. **Verify Google Cloud Console Settings**
   - Go to Google Cloud Console
   - Check that your redirect URI is listed exactly
   - Make sure there are no extra spaces or characters

3. **Test with curl**
   ```bash
   # Test your OAuth endpoint
   curl -I https://your-domain.com/login/google/authorized
   ```

## Security Notes

1. **Never commit OAuth secrets to Git**
   - Use environment variables
   - Keep .env files out of version control

2. **Use HTTPS in Production**
   - Google OAuth requires HTTPS for production
   - Set up SSL certificates for your domain

3. **Regular Security Updates**
   - Keep your OAuth libraries updated
   - Monitor Google Cloud Console for any security alerts

## Quick Fix for Immediate Deployment

If you need to deploy right now without OAuth:

1. **Comment out OAuth in main.py**
   ```python
   # Temporarily disable Google OAuth
   # if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
   #     google_bp = make_google_blueprint(...)
   #     app.register_blueprint(google_bp, url_prefix="/login")
   ```

2. **Deploy without OAuth**
   - Users can still register/login with email/password
   - Add OAuth later when you have a proper domain

3. **Update your login template**
   - Hide or remove the Google login button temporarily

This way you can deploy your application immediately and add OAuth later when you have a proper domain name set up. 