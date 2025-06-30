#!/bin/bash

# Sanchari Mentors Platform - VM Deployment Script
# This script sets up and deploys the Flask application directly on a VM

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to get public IP
get_public_ip() {
    if command -v curl >/dev/null 2>&1; then
        curl -s ifconfig.me
    elif command -v wget >/dev/null 2>&1; then
        wget -qO- ifconfig.me
    else
        echo "localhost"
    fi
}

# Function to check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root. Please run as a regular user."
        exit 1
    fi
}

# Function to install system dependencies
install_system_deps() {
    print_status "Installing system dependencies..."
    
    # Update package list
    sudo apt-get update
    
    # Install required packages
    sudo apt-get install -y \
        python3 \
        python3-venv \
        python3-pip \
        git \
        curl \
        nginx \
        supervisor \
        build-essential \
        python3-dev \
        libffi-dev \
        libssl-dev
    
    print_success "System dependencies installed"
}

# Function to setup application directory
setup_app_directory() {
    print_status "Setting up application directory..."
    
    # Create app directory if it doesn't exist
    if [ ! -d "/home/$USER/sanchari-mentors" ]; then
        mkdir -p /home/$USER/sanchari-mentors
    fi
    
    cd /home/$USER/sanchari-mentors
    
    # If this is a fresh install, copy files from current directory
    if [ ! -f "main.py" ]; then
        print_status "Copying application files..."
        cp -r /tmp/notebook/* .
    fi
    
    print_success "Application directory setup complete"
}

# Function to setup Python virtual environment
setup_python_env() {
    print_status "Setting up Python virtual environment..."
    
    cd /home/$USER/sanchari-mentors
    
    # Create virtual environment
    python3 -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install Python dependencies
    pip install -r requirements.txt
    
    # Install additional production dependencies
    pip install gunicorn
    
    print_success "Python environment setup complete"
}

# Function to create environment file
create_env_file() {
    print_status "Creating environment file..."
    
    cd /home/$USER/sanchari-mentors
    
    if [ ! -f .env ]; then
        cat > .env << EOF
# Sanchari Mentors Platform Environment Variables
SECRET_KEY=$(openssl rand -hex 32)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=8000
EOF
        print_success "Environment file created"
        print_warning "Please update GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env file"
    else
        print_status "Environment file already exists"
    fi
}

# Function to create data directories
create_data_directories() {
    print_status "Creating data directories..."
    
    cd /home/$USER/sanchari-mentors
    
    mkdir -p data
    mkdir -p flask_session
    mkdir -p static/uploads
    
    # Set proper permissions
    chmod 755 data flask_session static/uploads
    
    print_success "Data directories created"
}

# Function to setup Gunicorn service
setup_gunicorn_service() {
    print_status "Setting up Gunicorn service..."
    
    # Create supervisor configuration
    sudo tee /etc/supervisor/conf.d/sanchari-mentors.conf > /dev/null << EOF
[program:sanchari-mentors]
command=/home/$USER/sanchari-mentors/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 main:app
directory=/home/$USER/sanchari-mentors
user=$USER
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/sanchari-mentors.log
environment=HOME="/home/$USER"
EOF
    
    # Reload supervisor
    sudo supervisorctl reread
    sudo supervisorctl update
    
    print_success "Gunicorn service setup complete"
}

# Function to setup Nginx
setup_nginx() {
    print_status "Setting up Nginx..."
    
    # Create Nginx configuration
    sudo tee /etc/nginx/sites-available/sanchari-mentors > /dev/null << EOF
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /static {
        alias /home/$USER/sanchari-mentors/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF
    
    # Enable the site
    sudo ln -sf /etc/nginx/sites-available/sanchari-mentors /etc/nginx/sites-enabled/
    
    # Remove default site if it exists
    sudo rm -f /etc/nginx/sites-enabled/default
    
    # Test Nginx configuration
    sudo nginx -t
    
    # Restart Nginx
    sudo systemctl restart nginx
    sudo systemctl enable nginx
    
    print_success "Nginx setup complete"
}

# Function to setup firewall
setup_firewall() {
    print_status "Setting up firewall..."
    
    # Allow SSH, HTTP, and HTTPS
    sudo ufw allow ssh
    sudo ufw allow 80
    sudo ufw allow 443
    
    # Enable firewall
    echo "y" | sudo ufw enable
    
    print_success "Firewall setup complete"
}

# Function to start the application
start_application() {
    print_status "Starting the application..."
    
    # Start the supervisor service
    sudo supervisorctl start sanchari-mentors
    
    # Wait a moment for the service to start
    sleep 5
    
    # Check if the service is running
    if sudo supervisorctl status sanchari-mentors | grep -q "RUNNING"; then
        print_success "Application started successfully!"
    else
        print_error "Failed to start application. Check logs:"
        sudo supervisorctl status sanchari-mentors
        sudo tail -n 20 /var/log/sanchari-mentors.log
        exit 1
    fi
}

# Function to show deployment info
show_deployment_info() {
    local public_ip=$(get_public_ip)
    
    echo ""
    echo "=========================================="
    echo "  Sanchari Mentors Platform Deployment"
    echo "=========================================="
    echo ""
    echo "Application URLs:"
    echo "  Local:     http://localhost"
    echo "  Public:    http://$public_ip"
    echo ""
    echo "Useful Commands:"
    echo "  View logs:     sudo tail -f /var/log/sanchari-mentors.log"
    echo "  Restart app:   sudo supervisorctl restart sanchari-mentors"
    echo "  Stop app:      sudo supervisorctl stop sanchari-mentors"
    echo "  Status:        sudo supervisorctl status sanchari-mentors"
    echo "  Nginx logs:    sudo tail -f /var/log/nginx/access.log"
    echo ""
    print_warning "Note: Make sure to update GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env file"
    echo ""
}

# Function to update the application
update() {
    print_status "Updating the application..."
    
    cd /home/$USER/sanchari-mentors
    
    # Pull latest changes (if using git)
    if [ -d .git ]; then
        git pull origin main
    fi
    
    # Activate virtual environment and update dependencies
    source venv/bin/activate
    pip install -r requirements.txt
    
    # Restart the application
    sudo supervisorctl restart sanchari-mentors
    
    print_success "Application updated successfully!"
}

# Function to show logs
show_logs() {
    sudo tail -f /var/log/sanchari-mentors.log
}

# Function to stop the application
stop() {
    print_status "Stopping the application..."
    sudo supervisorctl stop sanchari-mentors
    print_success "Application stopped"
}

# Function to show status
status() {
    print_status "Application status:"
    sudo supervisorctl status sanchari-mentors
    echo ""
    print_status "Nginx status:"
    sudo systemctl status nginx --no-pager -l
}

# Main script logic
case "${1:-deploy}" in
    "deploy")
        check_root
        install_system_deps
        setup_app_directory
        setup_python_env
        create_env_file
        create_data_directories
        setup_gunicorn_service
        setup_nginx
        setup_firewall
        start_application
        show_deployment_info
        ;;
    "update")
        update
        show_deployment_info
        ;;
    "logs")
        show_logs
        ;;
    "stop")
        stop
        ;;
    "status")
        status
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  deploy   - Deploy the application (default)"
        echo "  update   - Update and restart the application"
        echo "  logs     - Show application logs"
        echo "  stop     - Stop the application"
        echo "  status   - Show application status"
        echo "  help     - Show this help message"
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac 