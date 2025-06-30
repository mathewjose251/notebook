#!/bin/bash

# Sanchari Mentors Platform - GCP VM Docker Deployment Script
# This script deploys the notebook repository using Docker on a GCP VM

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
        print_error "If you need to create a user, run: sudo adduser notebook && sudo usermod -aG sudo notebook"
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
        docker.io \
        docker-compose \
        git \
        curl \
        wget \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release
    
    # Start and enable Docker service
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # Add current user to docker group
    sudo usermod -aG docker $USER
    
    print_success "System dependencies installed"
    print_warning "You may need to log out and back in for Docker group changes to take effect"
}

# Function to setup application directory
setup_app_directory() {
    print_status "Setting up application directory..."
    
    # Create app directory
    mkdir -p ~/notebook
    cd ~/notebook
    
    # If this is a fresh install, clone the repo
    if [ ! -f "main.py" ]; then
        print_status "Cloning notebook repository..."
        git clone https://github.com/YOUR_GITHUB_USERNAME/notebook.git .
    else
        print_status "Updating existing repository..."
        git pull origin main
    fi
    
    print_success "Application directory setup complete"
}

# Function to create environment file
create_env_file() {
    print_status "Creating environment file..."
    
    cd ~/notebook
    
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
    
    cd ~/notebook
    
    mkdir -p data
    mkdir -p flask_session
    mkdir -p static/uploads
    
    # Set proper permissions
    chmod 755 data flask_session static/uploads
    
    print_success "Data directories created"
}

# Function to setup firewall
setup_firewall() {
    print_status "Setting up firewall..."
    
    # Allow SSH, HTTP, and HTTPS
    sudo ufw allow ssh
    sudo ufw allow 80
    sudo ufw allow 443
    sudo ufw allow 8000
    
    # Enable firewall
    echo "y" | sudo ufw enable
    
    print_success "Firewall setup complete"
}

# Function to build and deploy Docker containers
deploy_docker() {
    print_status "Building and deploying Docker containers..."
    
    cd ~/notebook
    
    # Stop any existing containers
    docker-compose -f docker-compose.simple.yml down 2>/dev/null || true
    
    # Build and start containers
    docker-compose -f docker-compose.simple.yml up --build -d
    
    # Wait for containers to start
    sleep 10
    
    # Check if containers are running
    if docker-compose -f docker-compose.simple.yml ps | grep -q "Up"; then
        print_success "Docker containers deployed successfully!"
    else
        print_error "Failed to deploy containers. Check logs:"
        docker-compose -f docker-compose.simple.yml logs
        exit 1
    fi
}

# Function to setup auto-restart service
setup_auto_restart() {
    print_status "Setting up auto-restart service..."
    
    # Create systemd service file
    sudo tee /etc/systemd/system/notebook-docker.service > /dev/null << EOF
[Unit]
Description=Sanchari Mentors Notebook Docker Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/$USER/notebook
ExecStart=/usr/bin/docker-compose -f docker-compose.simple.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.simple.yml down
User=$USER
Group=$USER

[Install]
WantedBy=multi-user.target
EOF
    
    # Enable and start the service
    sudo systemctl daemon-reload
    sudo systemctl enable notebook-docker.service
    sudo systemctl start notebook-docker.service
    
    print_success "Auto-restart service setup complete"
}

# Function to show deployment info
show_deployment_info() {
    local public_ip=$(get_public_ip)
    
    echo ""
    echo "=========================================="
    echo "  Sanchari Mentors Platform - GCP VM"
    echo "=========================================="
    echo ""
    echo "Application URLs:"
    echo "  Local:     http://localhost:8000"
    echo "  Public:    http://$public_ip:8000"
    echo ""
    echo "Useful Commands:"
    echo "  View logs:     docker-compose -f ~/notebook/docker-compose.simple.yml logs -f"
    echo "  Restart app:   docker-compose -f ~/notebook/docker-compose.simple.yml restart"
    echo "  Stop app:      docker-compose -f ~/notebook/docker-compose.simple.yml down"
    echo "  Status:        docker-compose -f ~/notebook/docker-compose.simple.yml ps"
    echo "  Update app:    ./deploy-gcp.sh update"
    echo ""
    print_warning "Note: Make sure to update GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env file"
    echo ""
}

# Function to update the application
update() {
    print_status "Updating the application..."
    
    cd ~/notebook
    
    # Pull latest changes
    git pull origin main
    
    # Rebuild and restart containers
    docker-compose -f docker-compose.simple.yml down
    docker-compose -f docker-compose.simple.yml up --build -d
    
    print_success "Application updated successfully!"
}

# Function to show logs
show_logs() {
    cd ~/notebook
    docker-compose -f docker-compose.simple.yml logs -f
}

# Function to stop the application
stop() {
    print_status "Stopping the application..."
    cd ~/notebook
    docker-compose -f docker-compose.simple.yml down
    print_success "Application stopped"
}

# Function to show status
status() {
    print_status "Application status:"
    cd ~/notebook
    docker-compose -f docker-compose.simple.yml ps
    echo ""
    print_status "Docker service status:"
    sudo systemctl status docker --no-pager -l
}

# Function to cleanup
cleanup() {
    print_status "Cleaning up Docker resources..."
    
    # Stop and remove containers
    cd ~/notebook
    docker-compose -f docker-compose.simple.yml down -v
    
    # Remove unused Docker resources
    docker system prune -f
    
    print_success "Cleanup completed"
}

# Main script logic
case "${1:-deploy}" in
    "deploy")
        check_root
        install_system_deps
        setup_app_directory
        create_env_file
        create_data_directories
        setup_firewall
        deploy_docker
        setup_auto_restart
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
    "cleanup")
        cleanup
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
        echo "  cleanup  - Clean up Docker resources"
        echo "  help     - Show this help message"
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac 