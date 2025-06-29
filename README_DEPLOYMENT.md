# Sanchari Mentors Platform - Deployment Guide

This guide will help you deploy the Sanchari Mentors Platform using Docker containers for easy deployment on any server with a public IP.

## Prerequisites

Before deploying, ensure you have the following installed on your server:

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)
- **OpenSSL** (for SSL certificate generation)
- **Git** (for version control)

### Installing Docker on Ubuntu/Debian

```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
```

### Installing Docker on CentOS/RHEL

```bash
# Install prerequisites
sudo yum install -y yum-utils

# Add Docker repository
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
```

## Quick Deployment

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd notebook
```

### 2. Configure Environment Variables

Copy the example environment file and update it with your settings:

```bash
cp production.env.example .env
```

Edit the `.env` file and update the following variables:

```bash
# Generate a secure secret key
SECRET_KEY=$(openssl rand -hex 32)

# Update Google OAuth credentials
GOOGLE_CLIENT_ID=your_actual_google_client_id
GOOGLE_CLIENT_SECRET=your_actual_google_client_secret
```

### 3. Deploy the Application

Make the deployment script executable and run it:

```bash
chmod +x deploy.sh
./deploy.sh
```

The script will:
- Check prerequisites
- Create necessary directories
- Generate SSL certificates
- Build and start the containers
- Display deployment information

### 4. Access Your Application

After successful deployment, you can access your application at:

- **Local**: http://localhost
- **Public**: https://your-server-ip

## Manual Deployment

If you prefer to deploy manually without the script:

### 1. Create SSL Certificates

```bash
mkdir -p ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/key.pem \
    -out ssl/cert.pem \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=your-domain.com"
```

### 2. Create Data Directories

```bash
mkdir -p data flask_session static/uploads
```

### 3. Build and Start Containers

```bash
docker-compose build
docker-compose up -d
```

## Configuration

### Environment Variables

Key environment variables you should configure:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | Auto-generated |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | Required |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret | Required |
| `FLASK_ENV` | Flask environment | production |
| `FLASK_DEBUG` | Enable debug mode | False |

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Go to Credentials → Create Credentials → OAuth 2.0 Client IDs
5. Set authorized redirect URIs to: `https://your-domain.com/login/google/authorized`
6. Copy Client ID and Client Secret to your `.env` file

### SSL Certificates

For production, replace the self-signed certificates with real ones:

1. **Let's Encrypt** (Free):
   ```bash
   sudo apt-get install certbot
   sudo certbot certonly --standalone -d your-domain.com
   ```

2. **Commercial Certificates**: Place your certificate files in the `ssl/` directory:
   - `ssl/cert.pem` - Your certificate
   - `ssl/key.pem` - Your private key

## Management Commands

### View Application Status

```bash
./deploy.sh status
# or
docker-compose ps
```

### View Logs

```bash
./deploy.sh logs
# or
docker-compose logs -f
```

### Update Application

```bash
./deploy.sh update
```

### Stop Application

```bash
./deploy.sh stop
# or
docker-compose down
```

### Restart Application

```bash
docker-compose restart
```

## Security Considerations

### 1. Firewall Configuration

Ensure your server firewall allows the necessary ports:

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Allow SSH (if needed)
sudo ufw allow 22
```

### 2. Regular Updates

Keep your application and dependencies updated:

```bash
# Update the application
./deploy.sh update

# Update Docker images
docker-compose pull
docker-compose up -d
```

### 3. Backup Strategy

Regularly backup your data:

```bash
# Backup data directory
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# Backup environment file
cp .env backup-env-$(date +%Y%m%d)
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   sudo netstat -tulpn | grep :80
   sudo netstat -tulpn | grep :443
   
   # Stop conflicting services
   sudo systemctl stop apache2  # if Apache is running
   sudo systemctl stop nginx    # if Nginx is running
   ```

2. **Permission Issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   chmod +x deploy.sh
   ```

3. **Container Won't Start**
   ```bash
   # Check container logs
   docker-compose logs web
   
   # Check if ports are available
   docker-compose ps
   ```

4. **SSL Certificate Issues**
   ```bash
   # Regenerate certificates
   rm -rf ssl/
   ./deploy.sh
   ```

### Health Check

Monitor your application health:

```bash
# Check health endpoint
curl -k https://localhost/health

# Check container health
docker-compose ps
```

## Performance Optimization

### 1. Resource Limits

Add resource limits to your containers in `docker-compose.yml`:

```yaml
services:
  web:
    # ... existing configuration ...
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### 2. Database Optimization

Consider using an external database for production:

```yaml
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: sanchari_mentors
      POSTGRES_USER: sanchari
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### 3. Caching

Add Redis for session caching:

```yaml
services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

## Monitoring and Logging

### 1. Application Logs

```bash
# View real-time logs
docker-compose logs -f web

# View nginx logs
docker-compose logs -f nginx
```

### 2. System Monitoring

Install monitoring tools:

```bash
# Install htop for system monitoring
sudo apt-get install htop

# Monitor system resources
htop
```

### 3. Log Rotation

Configure log rotation for production:

```bash
# Create logrotate configuration
sudo tee /etc/logrotate.d/sanchari-mentors << EOF
/path/to/your/app/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
}
EOF
```

## Support

If you encounter issues:

1. Check the logs: `./deploy.sh logs`
2. Verify configuration: `./deploy.sh status`
3. Check system resources: `htop`
4. Review this documentation
5. Check Docker and Docker Compose documentation

## License

This deployment guide is part of the Sanchari Mentors Platform project. 