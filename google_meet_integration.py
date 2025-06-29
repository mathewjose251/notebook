# Google Meet Integration for Sanchari Mentors

import os
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleMeetIntegration:
    def __init__(self):
        self.service = None
        self.credentials = None
        
    def authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        
        # Load existing credentials
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # For production, you'll need to set up OAuth properly
                # This is a simplified version for demonstration
                print("Google Calendar authentication required")
                return False
                
        # Save credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
        self.credentials = creds
        self.service = build('calendar', 'v3', credentials=creds)
        return True
    
    def create_training_session_with_meet(self, training_data):
        """
        Create a Google Calendar event with Google Meet link
        
        Args:
            training_data (dict): Training session information
            
        Returns:
            dict: Event details including Meet link
        """
        try:
            # Calculate start and end times
            start_time = datetime.fromisoformat(training_data['start_datetime'])
            end_time = start_time + timedelta(hours=int(training_data.get('duration', 1)))
            
            # Create event with Google Meet
            event = {
                'summary': f"Sanchari Mentors: {training_data['title']}",
                'description': f"""
                    <h3>Training Session Details</h3>
                    <p><strong>Topic:</strong> {training_data['topic']}</p>
                    <p><strong>Trainer:</strong> {training_data['trainer']}</p>
                    <p><strong>Description:</strong> {training_data['description']}</p>
                    <p><strong>Prerequisites:</strong> {training_data.get('prerequisites', 'None')}</p>
                    
                    <hr>
                    <p><em>Organized by Sanchari Mentors - Social Impact Education Platform</em></p>
                    <p>YouTube: @Sancharimentors | Instagram: sanchari.chennai</p>
                """,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Asia/Kolkata',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Asia/Kolkata',
                },
                'attendees': [],  # Will be populated with interested students
                'conferenceData': {
                    'createRequest': {
                        'requestId': f"sanchari-{training_data['id']}-{int(datetime.now().timestamp())}",
                        'conferenceSolutionKey': {
                            'type': 'hangoutsMeet'
                        }
                    }
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 30},       # 30 minutes before
                    ],
                },
                'visibility': 'public',
                'guestsCanModify': False,
                'guestsCanInviteOthers': False,
                'guestsCanSeeOtherGuests': True,
            }
            
            # Create the event
            created_event = self.service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1
            ).execute()
            
            # Extract Google Meet link
            meet_link = None
            if 'conferenceData' in created_event and 'entryPoints' in created_event['conferenceData']:
                for entry_point in created_event['conferenceData']['entryPoints']:
                    if entry_point['entryPointType'] == 'video':
                        meet_link = entry_point['uri']
                        break
            
            return {
                'success': True,
                'event_id': created_event['id'],
                'meet_link': meet_link,
                'calendar_link': created_event.get('htmlLink'),
                'event_details': created_event
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_attendees_to_event(self, event_id, attendee_emails):
        """Add attendees to an existing calendar event"""
        try:
            # Get the existing event
            event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
            
            # Add new attendees
            existing_attendees = event.get('attendees', [])
            existing_emails = {attendee['email'] for attendee in existing_attendees}
            
            for email in attendee_emails:
                if email not in existing_emails:
                    existing_attendees.append({'email': email})
            
            event['attendees'] = existing_attendees
            
            # Update the event
            updated_event = self.service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=event
            ).execute()
            
            return {'success': True, 'updated_event': updated_event}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

def send_training_notification_with_meet(training_data, interested_students, meet_link):
    """
    Send email notifications to interested students with Google Meet link
    
    Args:
        training_data (dict): Training session information
        interested_students (list): List of student email addresses
        meet_link (str): Google Meet link for the session
    """
    
    # Email configuration (you'll need to set these up)
    sender_email = "notifications@sanchari.org"
    sender_password = "your_app_password"  # Use app password for Gmail
    
    # Create email template
    email_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Inter', Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #B91C1C 0%, #F97316 100%); color: white; padding: 30px; text-align: center; border-radius: 12px 12px 0 0; }}
            .content {{ background: white; padding: 30px; border: 1px solid #e5e7eb; }}
            .footer {{ background: #f8f9fa; padding: 20px; text-align: center; border-radius: 0 0 12px 12px; }}
            .btn {{ display: inline-block; background: linear-gradient(135deg, #B91C1C 0%, #F97316 100%); color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; margin: 10px 5px; }}
            .btn:hover {{ transform: translateY(-2px); }}
            .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .social-links {{ margin-top: 15px; }}
            .social-links a {{ color: #B91C1C; text-decoration: none; margin: 0 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎓 New Training Session Available!</h1>
                <p>Sanchari Mentors - Social Impact Education</p>
            </div>
            
            <div class="content">
                <h2>📚 {training_data['title']}</h2>
                <p>Great news! A new training session in <strong>{training_data['topic']}</strong> has been scheduled based on your interests.</p>
                
                <div class="details">
                    <h3>📋 Session Details:</h3>
                    <ul>
                        <li><strong>Topic:</strong> {training_data['topic']}</li>
                        <li><strong>Trainer:</strong> {training_data['trainer']}</li>
                        <li><strong>Date & Time:</strong> {training_data['start_datetime']}</li>
                        <li><strong>Duration:</strong> {training_data.get('duration', 1)} hour(s)</li>
                        <li><strong>Prerequisites:</strong> {training_data.get('prerequisites', 'None')}</li>
                    </ul>
                </div>
                
                <h3>📝 Description:</h3>
                <p>{training_data['description']}</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{meet_link}" class="btn">🎥 Join Google Meet</a>
                    <a href="#" class="btn">📅 Add to Calendar</a>
                </div>
                
                <div style="background: #e0f2fe; padding: 15px; border-radius: 8px; border-left: 4px solid #0ea5e9;">
                    <h4>💡 How to Join:</h4>
                    <ol>
                        <li>Click the "Join Google Meet" button above</li>
                        <li>Allow camera and microphone access</li>
                        <li>Wait for the trainer to admit you to the session</li>
                        <li>Enjoy learning with Sanchari Mentors!</li>
                    </ol>
                </div>
                
                <p><strong>Questions?</strong> Reply to this email or contact our support team.</p>
            </div>
            
            <div class="footer">
                <p><strong>Sanchari Mentors</strong><br>
                Empowering Students Through Social Impact Education</p>
                
                <div class="social-links">
                    <a href="https://youtube.com/@Sancharimentors">📺 YouTube</a>
                    <a href="https://instagram.com/sanchari.chennai">📸 Instagram</a>
                </div>
                
                <p style="font-size: 0.9em; color: #666; margin-top: 15px;">
                    You received this email because you expressed interest in {training_data['topic']} training sessions.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        # Set up SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send emails to all interested students
        for student_email in interested_students:
            msg = MIMEMultipart('alternative')
            msg['From'] = sender_email
            msg['To'] = student_email
            msg['Subject'] = f"🎓 New {training_data['topic']} Training - Join with Google Meet!"
            
            # Attach HTML content
            html_part = MIMEText(email_template, 'html')
            msg.attach(html_part)
            
            # Send email
            server.send_message(msg)
            print(f"Email sent to {student_email}")
        
        server.quit()
        return {'success': True, 'emails_sent': len(interested_students)}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_interested_students(topic):
    """
    Get list of students interested in a specific topic
    
    Args:
        topic (str): Training topic
        
    Returns:
        list: List of student email addresses
    """
    try:
        # Load student interests
        with open('src/data/interests.json', 'r') as f:
            interests_data = json.load(f)
        
        interested_students = []
        for student_email, interests in interests_data.items():
            if topic.lower() in [interest.lower() for interest in interests]:
                interested_students.append(student_email)
        
        return interested_students
        
    except Exception as e:
        print(f"Error getting interested students: {e}")
        return []

# Example usage function
def create_and_notify_training_session(training_data):
    """
    Complete workflow: Create Google Meet session and notify interested students
    
    Args:
        training_data (dict): Training session information
        
    Returns:
        dict: Result of the operation
    """
    
    # Initialize Google Meet integration
    meet_integration = GoogleMeetIntegration()
    
    # Authenticate (in production, this should be handled properly)
    if not meet_integration.authenticate():
        return {
            'success': False,
            'error': 'Google Calendar authentication failed'
        }
    
    # Create Google Calendar event with Meet link
    event_result = meet_integration.create_training_session_with_meet(training_data)
    
    if not event_result['success']:
        return event_result
    
    # Get interested students
    interested_students = get_interested_students(training_data['topic'])
    
    if not interested_students:
        return {
            'success': True,
            'message': 'Training session created but no interested students found',
            'meet_link': event_result['meet_link'],
            'event_id': event_result['event_id']
        }
    
    # Add students as attendees to the calendar event
    meet_integration.add_attendees_to_event(event_result['event_id'], interested_students)
    
    # Send email notifications with Meet link
    email_result = send_training_notification_with_meet(
        training_data, 
        interested_students, 
        event_result['meet_link']
    )
    
    return {
        'success': True,
        'meet_link': event_result['meet_link'],
        'event_id': event_result['event_id'],
        'calendar_link': event_result['calendar_link'],
        'interested_students': len(interested_students),
        'emails_sent': email_result.get('emails_sent', 0),
        'email_success': email_result['success']
    }

