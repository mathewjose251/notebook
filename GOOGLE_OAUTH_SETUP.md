# Google OAuth Setup Guide for Sanchari Mentors

## Current Issue
The Google OAuth is failing because the redirect URI is not properly configured in the Google Cloud Console.

## Solution Steps

### 1. Access Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project or create a new one
3. Navigate to "APIs & Services" > "Credentials"

### 2. Configure OAuth 2.0 Client ID
1. Find your existing OAuth 2.0 Client ID or create a new one
2. Click on the client ID to edit it
3. In the "Authorized redirect URIs" section, add:
   ```
   http://localhost:8000/login/google/authorized
   ```
4. **Important**: Make sure to use `localhost` not `127.0.0.1`
5. Click "Save"

### 3. Verify Configuration
Your OAuth 2.0 Client ID should have these settings:
- **Application type**: Web application
- **Name**: Sanchari Mentors (or your preferred name)
- **Authorized JavaScript origins**: 
  ```
  http://localhost:8000
  ```
- **Authorized redirect URIs**:
  ```
  http://localhost:8000/login/google/authorized
  ```

### 4. Update Environment Variables (Optional)
You can set environment variables instead of hardcoding credentials:

```bash
export GOOGLE_CLIENT_ID="your-client-id-here"
export GOOGLE_CLIENT_SECRET="your-client-secret-here"
```

### 5. Test the Setup
1. Restart your Flask application
2. Go to `http://localhost:8000/login`
3. Click "Login with Google"
4. You should be redirected to Google's consent screen
5. After authorization, you should be redirected back to the application

## Troubleshooting

### Common Issues:

1. **"redirect_uri_mismatch" error**
   - Ensure the redirect URI in Google Cloud Console exactly matches: `http://localhost:8000/login/google/authorized`
   - Check for typos or extra spaces

2. **"invalid_client" error**
   - Verify your Client ID and Client Secret are correct
   - Make sure you're using the right OAuth 2.0 Client ID

3. **"access_denied" error**
   - Check if the Google+ API is enabled in your project
   - Verify the scopes are properly configured

### Enable Required APIs:
1. Go to "APIs & Services" > "Library"
2. Search for and enable:
   - Google+ API
   - Google People API

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit credentials to version control**
   - Use environment variables for production
   - Add `.env` files to `.gitignore`

2. **Production Setup**
   - Use HTTPS in production
   - Update redirect URIs to your production domain
   - Remove `OAUTHLIB_INSECURE_TRANSPORT` setting

3. **Client Secret Security**
   - Keep your client secret secure
   - Rotate secrets regularly
   - Use different credentials for development and production

## Current Configuration

The application is currently configured with:
- **Client ID**: `102669950361-2do2cq17m4fd9dkoj4da7qiuu3b2snrr.apps.googleusercontent.com`
- **Redirect URI**: `http://localhost:8000/login/google/authorized`
- **Scopes**: `profile`, `email`

Make sure these match exactly in your Google Cloud Console configuration. 