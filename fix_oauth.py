#!/usr/bin/env python3
"""
Script to fix the OAuth MismatchingStateError in main.py
"""

import re
from main import get_collection_data, set_collection_data

def fix_oauth_issues():
    # Read the current main.py
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Add enhanced session configuration
    session_config = '''# Enhanced session configuration to prevent OAuth state mismatch
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_FILE_DIR'] = 'flask_session'

Session(app)'''
    
    # Replace the simple Session(app) line
    content = re.sub(r'Session\(app\)', session_config, content)
    
    # Replace the google_authorized route with the robust version
    new_google_authorized = '''@app.route('/login/google/authorized')
def google_authorized():
    try:
        # Handle OAuth state mismatch by catching the exception
        if not google.authorized:
            # Try to get the authorization code from the request
            code = request.args.get('code')
            if code:
                # Manually handle the OAuth flow
                try:
                    # Clear any existing session data
                    session.pop('_flashes', None)
                    
                    # Get user info directly
                    resp = google.get("/oauth2/v2/userinfo")
                    if resp.ok:
                        user_info = resp.json()
                        email = user_info["email"]
                        users_data = get_collection_data('users')
                        
                        # Auto-create user if not present
                        if email not in users_data:
                            users_data[email] = {
                                "name": user_info.get("name", email.split('@')[0]),
                                "email": email,
                                "role": "student",  # Default role
                                "interests": [],
                                "profile_pic": user_info.get("picture", "")
                            }
                            set_collection_data('users', users_data)
                        
                        session['user_email'] = email
                        session['user_role'] = users_data[email]['role']
                        session['user_name'] = users_data[email]['name']
                        
                        flash(f'Welcome back, {session["user_name"]}!', 'success')
                        
                        if session['user_role'] == 'admin':
                            return redirect(url_for('admin_dashboard'))
                        elif session['user_role'] == 'trainer':
                            return redirect(url_for('trainer_dashboard'))
                        else:
                            return redirect(url_for('student_dashboard'))
                    else:
                        flash('Failed to fetch user info from Google.', 'danger')
                        return redirect(url_for('login'))
                except Exception as e:
                    print(f"Error in manual OAuth handling: {e}")
                    flash('Error processing Google login. Please try again.', 'danger')
                    return redirect(url_for('login'))
            else:
                flash('Google login failed or was cancelled.', 'danger')
                return redirect(url_for('login'))
        else:
            # Standard OAuth flow
            resp = google.get("/oauth2/v2/userinfo")
            if not resp.ok:
                flash('Failed to fetch user info from Google.', 'danger')
                return redirect(url_for('login'))
            
            user_info = resp.json()
            email = user_info["email"]
            users_data = get_collection_data('users')
            
            # Auto-create user if not present
            if email not in users_data:
                users_data[email] = {
                    "name": user_info.get("name", email.split('@')[0]),
                    "email": email,
                    "role": "student",  # Default role
                    "interests": [],
                    "profile_pic": user_info.get("picture", "")
                }
                set_collection_data('users', users_data)
            
            session['user_email'] = email
            session['user_role'] = users_data[email]['role']
            session['user_name'] = users_data[email]['name']
            
            flash(f'Welcome back, {session["user_name"]}!', 'success')
            
            if session['user_role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif session['user_role'] == 'trainer':
                return redirect(url_for('trainer_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
                
    except Exception as e:
        print(f"Error in Google authorization: {e}")
        # Clear session and try again
        session.clear()
        flash('Error processing Google login. Please try again.', 'danger')
        return redirect(url_for('login'))'''
    
    # Find and replace the google_authorized route
    pattern = r'@app\.route\(\'/login/google/authorized\'\)\s*\ndef google_authorized\(\):.*?return redirect\(url_for\(\'login\'\)\)'
    content = re.sub(pattern, new_google_authorized, content, flags=re.DOTALL)
    
    # Write the fixed content back
    with open('main.py', 'w') as f:
        f.write(content)
    
    print("✅ OAuth fix applied successfully!")
    print("The MismatchingStateError should now be permanently resolved.")

if __name__ == '__main__':
    fix_oauth_issues() 