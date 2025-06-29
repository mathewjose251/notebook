# Sanchari Mentors Platform

A comprehensive social impact education platform that connects students with mentors for personalized learning experiences.

## 🚀 Features

### For Students
- **Personalized Learning**: Choose from various subjects and skills
- **Live Sessions**: Attend interactive training sessions
- **Resource Library**: Access study materials and resources
- **Doubt Clearing**: Get help with questions and concepts
- **Career Guidance**: Receive career counseling and advice
- **Skill Development**: Track and improve your skills
- **Achievements**: Earn certificates and badges
- **Community**: Connect with fellow students
- **Interest Management**: Set learning preferences

### For Trainers/Mentors
- **Session Management**: Create and manage training sessions
- **Student Progress Tracking**: Monitor student performance
- **Resource Management**: Upload and organize teaching materials
- **Communication Hub**: Interact with students and parents
- **Training Modules**: Create structured learning programs
- **Feedback System**: Collect and analyze student feedback

### For Administrators
- **User Management**: Manage students, trainers, and staff
- **Class Management**: Oversee all training sessions
- **Content Management**: Organize educational content
- **Reports & Analytics**: Generate insights and reports
- **Communications**: Send announcements and notifications
- **System Monitoring**: Monitor platform health and usage

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Session-based with role management + Google OAuth
- **Data Storage**: JSON files (can be easily migrated to database)
- **Styling**: Custom CSS with CSS Variables and modern design
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Poppins, Lato)

## 📁 Project Structure

```
Sanchari Mentors Platform/
├── main.py                 # Main Flask application
├── app.py                  # Alternative entry point with API endpoints
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── setup_google_oauth.py  # Google OAuth setup helper
├── test_google_oauth.py   # Google OAuth test script
├── .env                   # Environment variables (create this)
├── templates/             # Flask templates
│   ├── base.html          # Base template
│   ├── index.html         # Homepage
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── classes.html       # Classes listing
│   ├── errors/            # Error pages
│   │   ├── 404.html
│   │   ├── 403.html
│   │   └── 500.html
│   ├── admin/             # Admin templates
│   │   ├── dashboard.html
│   │   ├── users.html
│   │   ├── create_user.html
│   │   └── edit_user.html
│   ├── student/           # Student templates
│   │   ├── dashboard.html
│   │   ├── interests.html
│   │   └── ...
│   └── trainer/           # Trainer templates
│       ├── dashboard.html
│       └── ...
├── static/                # Static files
│   ├── css/
│   │   ├── styles.css     # Main stylesheet
│   │   ├── new-theme.css  # Alternative theme
│   │   ├── vibrant-theme.css
│   │   └── mentor-showcase.css
│   ├── js/
│   │   ├── mentor-carousel.js
│   │   └── chat-widget.js
│   └── images/            # Image assets
├── data/                  # JSON data files
│   ├── users.json         # User data
│   ├── classes.json       # Class information
│   └── sessions.json      # Session data
└── docs/                  # Documentation
    ├── Google OAuth Integration for Sanchari Mentors - Detailed Guide.md
    ├── Sanchari Mentors Platform - Data Storage and Hosting Guide.md
    └── Usability Validation Report for Sanchari Mentors Platform.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Google account (for OAuth setup)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Edutech App for Social Cause Mentoring in React (3)"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google OAuth (Optional but Recommended)**
   ```bash
   # Run the setup helper
   python3 setup_google_oauth.py
   
   # Or test the current configuration
   python3 test_google_oauth.py
   ```

4. **Run the application**
   ```bash
   # Option 1: Using main.py
   python3 main.py
   
   # Option 2: Using app.py (with additional API endpoints)
   python3 app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:8000`
   - Admin login: `admin@sanchari.org` / `Admin@2025`

## 🔐 Authentication & Roles

### User Roles
- **Student**: Can access classes, resources, and learning features
- **Trainer**: Can create sessions, manage students, and upload content
- **Admin**: Full system access and user management

### Authentication Methods
- **Google OAuth**: Primary login method for students and trainers
- **Email/Password**: Fallback method for admin and testing

### Default Credentials (For Testing Only)
- **Admin**: `admin@sanchari.org` / `Admin@2025`
- **Dummy Trainer**: `trainer1@sanchari.org` / `dummy`
- **Dummy Student**: `student1@sanchari.org` / `dummy`

## 🔑 Google OAuth Setup

The platform supports Google OAuth for secure login using Gmail accounts.

### Quick Setup
1. **Run the setup helper**:
   ```bash
   python3 setup_google_oauth.py
   ```

2. **Follow the interactive guide** to:
   - Create a Google Cloud project
   - Enable Google+ API
   - Create OAuth 2.0 credentials
   - Configure redirect URIs

3. **Test the configuration**:
   ```bash
   python3 test_google_oauth.py
   ```

### Manual Setup
For detailed manual setup instructions, see:
- [Google OAuth Integration Guide](Google%20OAuth%20Integration%20for%20Sanchari%20Mentors%20-%20Detailed%20Guide.md)

### Environment Variables
Create a `.env` file in the project root:
```env
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
```

### Features
- **Auto User Creation**: New Google users are automatically created as students
- **Profile Sync**: Name, email, and profile picture are synced from Google
- **Role Management**: Admins can change user roles through the admin panel
- **Secure**: Uses OAuth 2.0 with proper scopes and security measures

## 📊 API Endpoints

The application includes RESTful API endpoints for integration:

- `GET /api/classes` - Get all classes
- `GET /api/users` - Get all users (admin only)
- `GET /api/sessions` - Get all sessions
- `GET /api/mentors` - Get all mentors/trainers
- `GET /api/stats` - Get platform statistics
- `GET /health` - Health check endpoint

## 🎨 Design Features

### Modern UI/UX
- **Responsive Design**: Works on all devices
- **Glass Morphism**: Modern glass-like effects
- **Gradient Backgrounds**: Beautiful color transitions
- **Smooth Animations**: CSS transitions and animations
- **Interactive Elements**: Hover effects and micro-interactions

### Color Scheme
- **Primary**: #4A90E2 (Blue)
- **Secondary**: #F5A623 (Orange)
- **Accent**: #7ED321 (Green)
- **Gradients**: Purple-blue and orange-pink combinations

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key
- `FLASK_DEBUG`: Enable/disable debug mode
- `FLASK_HOST`: Server host (default: 0.0.0.0)
- `FLASK_PORT`: Server port (default: 8000)
- `GOOGLE_CLIENT_ID`: Google OAuth Client ID
- `GOOGLE_CLIENT_SECRET`: Google OAuth Client Secret

### Customization
- Modify CSS variables in `static/css/styles.css`
- Update color schemes and themes
- Customize templates in the `templates/` directory

## 📈 Data Management

### JSON Data Structure
The application uses JSON files for data storage:

- **users.json**: User profiles and authentication
- **classes.json**: Training session information
- **sessions.json**: Attendance and participation data

### Data Migration
To migrate to a database:
1. Replace JSON file operations in `main.py`
2. Update data loading functions
3. Implement database models and connections

## 🚀 Deployment

### Local Development
```bash
python3 main.py
```

### Production Deployment
1. Set environment variables
2. Remove `OAUTHLIB_INSECURE_TRANSPORT` setting
3. Use HTTPS for Google OAuth
4. Configure production database
5. Set up proper logging and monitoring

## 🐛 Troubleshooting

### Common Issues

1. **Port 5000 in use (macOS)**
   - The app now runs on port 8000 by default
   - If you need to change it, modify the port in `main.py`

2. **Google OAuth not working**
   - Run `python3 test_google_oauth.py` to diagnose issues
   - Check that redirect URIs match exactly
   - Verify Google+ API is enabled

3. **Missing dependencies**
   - Run `pip install -r requirements.txt`
   - Make sure you're using Python 3.8+

4. **Template not found errors**
   - Ensure all HTML files are in the `templates/` directory
   - Check file permissions

## 📚 Documentation

- [Google OAuth Integration Guide](Google%20OAuth%20Integration%20for%20Sanchari%20Mentors%20-%20Detailed%20Guide.md)
- [Data Storage and Hosting Guide](Sanchari%20Mentors%20Platform%20-%20Data%20Storage%20and%20Hosting%20Guide.md)
- [Usability Validation Report](Usability%20Validation%20Report%20for%20Sanchari%20Mentors%20Platform.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the troubleshooting section above
- Review the documentation files
- Run the test scripts to diagnose issues

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ Basic platform structure
- ✅ User authentication
- ✅ Class management
- ✅ Student dashboard

### Phase 2 (Planned)
- 🔄 Database integration
- 🔄 Real-time chat
- 🔄 Video conferencing
- 🔄 Payment integration

### Phase 3 (Future)
- 📋 Mobile app
- 📋 AI-powered recommendations
- 📋 Advanced analytics
- 📋 Multi-language support

---

**Made with ❤️ by Sanchari Mentors Team** 