#!/usr/bin/env python3
"""
Sanchari Mentors Platform - Main Application Entry Point

This is the main Flask application for the Sanchari Mentors social impact education platform.
The application provides mentoring services for students with a focus on social causes.

Author: Sanchari Mentors Team
Version: 1.0.0
"""

import os
import sys
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the main application from main.py
from main import app, get_collection_data, set_collection_data

# Additional configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sanchari_mentors_secret_key_2025')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
app.config['HOST'] = os.environ.get('FLASK_HOST', '0.0.0.0')
app.config['PORT'] = int(os.environ.get('FLASK_PORT', 8000))

# Additional routes for API endpoints
@app.route('/api/users')
def api_users():
    """API endpoint to get all users (admin only)"""
    if 'user_role' not in session or session['user_role'] != 'admin':
        return jsonify({
            'success': False,
            'error': 'Unauthorized access'
        }), 401
    
    try:
        users_data = get_collection_data('users')
        return jsonify({
            'success': True,
            'users': users_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/mentors')
def api_mentors():
    """API endpoint to get all mentors/trainers"""
    try:
        users_data = get_collection_data('users')
        mentors = [user for user in users_data if user.get('role') == 'trainer']
        return jsonify({
            'success': True,
            'mentors': mentors
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/student/<email>/interests', methods=['GET', 'PUT'])
def api_student_interests(email):
    """API endpoint to get or update student interests"""
    if 'user_role' not in session or session['user_role'] != 'student':
        return jsonify({
            'success': False,
            'error': 'Unauthorized access'
        }), 401
    
    try:
        users_data = get_collection_data('users')
        user = next((u for u in users_data if u.get('email') == email), None)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        if request.method == 'GET':
            return jsonify({
                'success': True,
                'interests': user.get('interests', [])
            })
        elif request.method == 'PUT':
            data = request.get_json()
            if 'interests' in data:
                user['interests'] = data['interests']
                # Update in DB
                db = get_collection_data.__globals__['get_db']()
                db['users'].update_one({'email': email}, {'$set': {'interests': data['interests']}})
                return jsonify({
                    'success': True,
                    'message': 'Interests updated successfully'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Interests field is required'
                }), 400
                
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/stats')
def api_stats():
    """API endpoint to get platform statistics"""
    try:
        users_data = get_collection_data('users')
        classes_data = get_collection_data('classes')
        sessions_data = get_collection_data('sessions')
        
        stats = {
            'total_users': len(users_data),
            'total_students': len([u for u in users_data if u.get('role') == 'student']),
            'total_trainers': len([u for u in users_data if u.get('role') == 'trainer']),
            'total_classes': len(classes_data),
            'total_sessions': len(sessions_data),
        }
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

# Development routes (only in debug mode)
if app.config['DEBUG']:
    @app.route('/dev/reset-data')
    def dev_reset_data():
        """Development endpoint to reset data to initial state"""
        try:
            # Reset users.json to initial state
            initial_users = {
                "student1@gmail.com": {
                    "name": "Priya Sharma",
                    "email": "student1@gmail.com",
                    "role": "student",
                    "interests": ["Artificial Intelligence", "Mathematics"],
                    "google_id": "google_id_1",
                    "profile_pic": "",
                    "created_at": "2025-06-10T10:00:00Z"
                },
                "student2@gmail.com": {
                    "name": "Rahul Kumar",
                    "email": "student2@gmail.com",
                    "role": "student",
                    "interests": ["Communication Skills", "Mathematics"],
                    "google_id": "google_id_2",
                    "profile_pic": "",
                    "created_at": "2025-06-11T14:30:00Z"
                },
                "admin@sanchari.org": {
                    "password": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
                    "role": "admin",
                    "name": "Admin User",
                    "email": "admin@sanchari.org",
                    "profile_pic": "",
                    "interests": []
                }
            }
            
            set_collection_data('users', initial_users)
            
            return jsonify({
                'success': True,
                'message': 'Data reset successfully'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

if __name__ == '__main__':
    print("🚀 Starting Sanchari Mentors Platform...")
    print(f"📍 Server: {app.config['HOST']}:{app.config['PORT']}")
    print(f"🔧 Debug Mode: {app.config['DEBUG']}")
    print("🌐 Access the application at: http://localhost:8000")
    print("📚 Admin Login: admin@sanchari.org / Admin@2025")
    print("=" * 50)
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )