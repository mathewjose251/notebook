#!/bin/bash

# ===================== GCP VM DEPLOYMENT INSTRUCTIONS =====================
#
# 1. Clean up old containers and volumes (run these on your GCP VM):
#    docker compose down -v
#    docker volume prune -f
#
# 2. Ensure the following directories exist and are writable:
#    sudo mkdir -p data flask_session static/uploads
#    sudo chmod -R 777 data flask_session static/uploads
#
# 3. Build and start the app (with no cache to ensure fresh build):
#    docker compose build --no-cache
#    docker compose up -d
#
# 4. Check logs for errors:
#    docker compose logs -f
#
# 5. Test the app:
#    Visit http://YOUR_VM_EXTERNAL_IP:8000/
#    Or run: curl http://localhost:8000/health
#
# If you see 'ContainerConfig' errors, double-check your docker-compose.yml for volume conflicts.
# If you see permission errors, make sure the directories have 777 permissions.
#
# ===========================================================================

# Sanchari Mentors Platform - Deployment Script
# This script sets up and deploys the containerized application

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get public IP
get_public_ip() {
    if command_exists curl; then
        curl -s ifconfig.me
    elif command_exists wget; then
        wget -qO- ifconfig.me
    else
        echo "localhost"
    fi
}

# Function to generate SSL certificates
generate_ssl_certificates() {
    print_status "Generating SSL certificates..."
    
    mkdir -p ssl
    
    # Generate self-signed certificate
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem \
        -out ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    
    print_success "SSL certificates generated successfully"
}

# Function to create environment file
create_env_file() {
    print_status "Creating environment file..."
    
    if [ ! -f .env ]; then
        cat > .env << EOF
# Sanchari Mentors Platform Environment Variables
SECRET_KEY=$(openssl rand -hex 32)
GOOGLE_CLIENT_ID=$(openssl rand -hex 16)
GOOGLE_CLIENT_SECRET=$(openssl rand -hex 16)
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
    
    # Copy existing JSON files to data directory if they exist
    if [ -f classes.json ]; then
        cp classes.json data/
    fi
    if [ -f users.json ]; then
        cp users.json data/
    fi
    if [ -f sessions.json ]; then
        cp sessions.json data/
    fi
    
    print_success "Data directories created"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi
    
    print_success "All prerequisites are met"
}

# Function to build and deploy
deploy() {
    print_status "Building and deploying the application..."
    
    # Build the Docker image
    docker-compose build
    
    # Start the services
    docker-compose up -d
    
    print_success "Application deployed successfully!"
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
    echo "  Public:    https://$public_ip"
    echo ""
    echo "Health Check:"
    echo "  http://localhost/health"
    echo "  https://$public_ip/health"
    echo ""
    echo "Useful Commands:"
    echo "  View logs:     docker-compose logs -f"
    echo "  Stop app:      docker-compose down"
    echo "  Restart app:   docker-compose restart"
    echo "  Update app:    ./deploy.sh update"
    echo ""
    print_warning "Note: You're using a self-signed SSL certificate."
    print_warning "For production, replace ssl/cert.pem and ssl/key.pem with real certificates."
    echo ""
}

# Function to update the application
update() {
    print_status "Updating the application..."
    
    # Pull latest changes (if using git)
    if [ -d .git ]; then
        git pull origin main
    fi
    
    # Rebuild and restart
    docker-compose down
    docker-compose build --no-cache
    docker-compose up -d
    
    print_success "Application updated successfully!"
}

# Function to show logs
show_logs() {
    docker-compose logs -f
}

# Function to stop the application
stop() {
    print_status "Stopping the application..."
    docker-compose down
    print_success "Application stopped"
}

# Function to show status
status() {
    print_status "Application status:"
    docker-compose ps
}

# Main script logic
case "${1:-deploy}" in
    "deploy")
        check_prerequisites
        create_env_file
        create_data_directories
        generate_ssl_certificates
        deploy
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