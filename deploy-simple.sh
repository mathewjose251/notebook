#!/bin/bash

# Sanchari Mentors Platform - Simple VM Deployment Script
# This script sets up the Flask application for manual running

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
        build-essential \
        python3-dev \
        libffi-dev \
        libssl-dev
    
    print_success "System dependencies installed"
}

# Function to setup Python virtual environment
setup_python_env() {
    print_status "Setting up Python virtual environment..."
    
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
    
    mkdir -p data
    mkdir -p flask_session
    mkdir -p static/uploads
    
    # Set proper permissions
    chmod 755 data flask_session static/uploads
    
    print_success "Data directories created"
}

# Function to start the application
start_application() {
    print_status "Starting the application..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Start with Gunicorn
    gunicorn -w 4 -b 0.0.0.0:8000 main:app
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
    echo "  Local:     http://localhost:8000"
    echo "  Public:    http://$public_ip:8000"
    echo ""
    echo "To start the application:"
    echo "  source venv/bin/activate"
    echo "  gunicorn -w 4 -b 0.0.0.0:8000 main:app"
    echo ""
    echo "Or use the start command:"
    echo "  ./deploy-simple.sh start"
    echo ""
    print_warning "Note: Make sure to update GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env file"
    echo ""
}

# Main script logic
case "${1:-setup}" in
    "setup")
        install_system_deps
        setup_python_env
        create_env_file
        create_data_directories
        show_deployment_info
        ;;
    "start")
        start_application
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  setup    - Setup the application (default)"
        echo "  start    - Start the application"
        echo "  help     - Show this help message"
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac 