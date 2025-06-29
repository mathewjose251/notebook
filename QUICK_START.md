# Quick Start Guide - Sanchari Mentors Platform

This guide will get your Sanchari Mentors Platform running in minutes using Docker containers.

## Prerequisites

Make sure you have Docker and Docker Compose installed on your system:

- **macOS**: Install Docker Desktop from https://www.docker.com/products/docker-desktop
- **Ubuntu/Debian**: Follow the installation guide in `README_DEPLOYMENT.md`
- **Windows**: Install Docker Desktop from https://www.docker.com/products/docker-desktop

## Quick Deployment (5 minutes)

### 1. Clone or Download the Project

```bash
# If you have git
git clone <your-repository-url>
cd notebook

# Or download and extract the ZIP file
# Then navigate to the project directory
```

### 2. Run the Simple Deployment Script

```bash
# Make the script executable (if not already)
chmod +x deploy-simple.sh

# Deploy the application
./deploy-simple.sh
```

The script will:
- ✅ Check if Docker is installed and running
- ✅ Create environment configuration
- ✅ Set up data directories
- ✅ Build and start the containers
- ✅ Show you the access URLs

### 3. Access Your Application

After successful deployment, you can access your application at:

- **Local**: http://localhost:8000
- **Public**: http://your-server-ip:8000

### 4. Configure Google OAuth (Optional)

For Google login to work, update the `.env` file with your Google OAuth credentials:

```bash
# Edit the .env file
nano .env

# Update these lines:
GOOGLE_CLIENT_ID=your_actual_google_client_id
GOOGLE_CLIENT_SECRET=your_actual_google_client_secret
```

Then restart the application:

```bash
./deploy-simple.sh update
```

## Management Commands

### View Application Status
```bash
./deploy-simple.sh status
```

### View Logs
```bash
./deploy-simple.sh logs
```

### Stop Application
```bash
./deploy-simple.sh stop
```

### Update Application
```bash
./deploy-simple.sh update
```

## Default Login Credentials

The application comes with some default users for testing:

### Admin User
- **Email**: admin@sanchari.com
- **Password**: admin123
- **Role**: Administrator

### Trainer User
- **Email**: trainer@sanchari.com
- **Password**: trainer123
- **Role**: Trainer

### Student User
- **Email**: student@sanchari.com
- **Password**: student123
- **Role**: Student

## Features Available

- ✅ User authentication and authorization
- ✅ Google OAuth integration
- ✅ Student dashboard with classes, resources, and community
- ✅ Trainer dashboard with sessions and student management
- ✅ Admin dashboard with user and content management
- ✅ Real-time health monitoring
- ✅ Mobile-responsive design

## Troubleshooting

### Application Won't Start
```bash
# Check if Docker is running
docker info

# Check container logs
./deploy-simple.sh logs

# Restart the application
./deploy-simple.sh stop
./deploy-simple.sh deploy
```

### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Stop conflicting services or change the port in docker-compose.simple.yml
```

### Permission Issues
```bash
# Fix file permissions
chmod +x deploy-simple.sh
chmod -R 755 .
```

## Next Steps

1. **Customize the Application**: Update the content, styling, and branding
2. **Add Real Data**: Replace the sample data with your actual content
3. **Configure Email**: Set up email notifications (if needed)
4. **Set Up Monitoring**: Add monitoring and alerting
5. **Production Deployment**: Use the full deployment script with HTTPS

## Support

If you encounter any issues:

1. Check the logs: `./deploy-simple.sh logs`
2. Verify Docker is running: `docker info`
3. Check the comprehensive deployment guide: `README_DEPLOYMENT.md`
4. Review the troubleshooting section in the main README

## Production Deployment

For production deployment with HTTPS, SSL certificates, and nginx reverse proxy, use:

```bash
./deploy.sh
```

This will set up a production-ready deployment with:
- HTTPS/SSL encryption
- Nginx reverse proxy
- Rate limiting
- Security headers
- Load balancing capabilities

---

**Happy Deploying! 🚀** 