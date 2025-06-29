# Sanchari Mentors Platform - Data Storage and Hosting Guide

## Current Data Storage Implementation

### 📁 **File-Based Storage System**
The Sanchari Mentors platform currently uses a **file-based data storage system** for simplicity and ease of deployment. Here's how data is organized:

```
/src/data/
├── users.json          # User accounts (students, trainers, admins)
├── classes.json        # Class/training information
├── interests.json      # Student learning interests
├── sessions.json       # Training sessions data
└── notifications.json  # Email notification logs
```

### 🔧 **Data Structure Examples**

**users.json:**
```json
{
  "admin@sanchari.org": {
    "email": "admin@sanchari.org",
    "password_hash": "hashed_password",
    "role": "admin",
    "name": "Admin User",
    "created_at": "2025-06-13T00:00:00Z"
  },
  "student@gmail.com": {
    "email": "student@gmail.com",
    "google_id": "google_oauth_id",
    "role": "student",
    "name": "Student Name",
    "interests": ["AI", "Mathematics"],
    "created_at": "2025-06-13T00:00:00Z"
  }
}
```

**interests.json:**
```json
{
  "student@gmail.com": {
    "selected_interests": ["AI", "Mathematics", "Communication"],
    "updated_at": "2025-06-13T00:00:00Z"
  }
}
```

## 🏠 **Hosting on Your Local VM**

### **Option 1: Direct Flask Deployment**

1. **Clone the project to your VM:**
```bash
git clone <your-repo> /opt/sanchari-mentors
cd /opt/sanchari-mentors
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set environment variables:**
```bash
export GOOGLE_CLIENT_ID="your-google-oauth-client-id"
export GOOGLE_CLIENT_SECRET="your-google-oauth-secret"
export FLASK_ENV="production"
```

4. **Run with Gunicorn (production server):**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 src.main:app
```

### **Option 2: Docker Deployment**

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "src.main:app"]
```

Run with Docker:
```bash
docker build -t sanchari-mentors .
docker run -d -p 5000:5000 \
  -e GOOGLE_CLIENT_ID="your-client-id" \
  -e GOOGLE_CLIENT_SECRET="your-secret" \
  -v /opt/sanchari-data:/app/src/data \
  sanchari-mentors
```

## 💾 **Data Persistence Strategies**

### **1. File-Based Storage (Current)**
- **Pros:** Simple, no database setup required
- **Cons:** Not suitable for high concurrency
- **Best for:** Small to medium deployments (< 1000 users)

### **2. SQLite Database (Recommended Upgrade)**
```python
# Add to requirements.txt
sqlite3

# Database schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE,
    password_hash TEXT,
    role TEXT,
    name TEXT,
    google_id TEXT,
    created_at TIMESTAMP
);

CREATE TABLE interests (
    user_email TEXT,
    interest TEXT,
    PRIMARY KEY (user_email, interest)
);
```

### **3. PostgreSQL/MySQL (Production)**
For larger deployments, consider:
- PostgreSQL with Docker
- MySQL with proper backup strategies
- Cloud databases (AWS RDS, Google Cloud SQL)

## 🔄 **Data Backup and Recovery**

### **Automated Backup Script**
```bash
#!/bin/bash
# backup-data.sh

BACKUP_DIR="/opt/backups/sanchari-$(date +%Y%m%d-%H%M%S)"
DATA_DIR="/opt/sanchari-mentors/src/data"

mkdir -p $BACKUP_DIR
cp -r $DATA_DIR/* $BACKUP_DIR/

# Keep only last 30 days of backups
find /opt/backups -name "sanchari-*" -mtime +30 -exec rm -rf {} \;

echo "Backup completed: $BACKUP_DIR"
```

### **Cron Job for Daily Backups**
```bash
# Add to crontab (crontab -e)
0 2 * * * /opt/scripts/backup-data.sh
```

## 🔐 **Security Considerations**

### **File Permissions**
```bash
# Secure data directory
chmod 700 /opt/sanchari-mentors/src/data
chown app-user:app-user /opt/sanchari-mentors/src/data
```

### **Environment Variables**
```bash
# /etc/environment or .env file
GOOGLE_CLIENT_ID="your-actual-client-id"
GOOGLE_CLIENT_SECRET="your-actual-secret"
SECRET_KEY="your-flask-secret-key"
```

## 📊 **Monitoring and Maintenance**

### **Log Management**
```python
# Add to main.py
import logging
logging.basicConfig(
    filename='/var/log/sanchari-mentors.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
```

### **Health Check Endpoint**
```python
@app.route('/health')
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

## 🚀 **Scaling Recommendations**

### **Small Scale (< 100 users)**
- Current file-based system
- Single VM deployment
- Daily backups

### **Medium Scale (100-1000 users)**
- Migrate to SQLite
- Load balancer with 2-3 app instances
- Hourly backups

### **Large Scale (1000+ users)**
- PostgreSQL database
- Container orchestration (Kubernetes)
- Real-time backup replication
- CDN for static assets

## 📝 **Migration Path**

When ready to upgrade from file-based to database:

1. **Create migration script:**
```python
import json
import sqlite3

def migrate_to_sqlite():
    # Read JSON files
    with open('data/users.json') as f:
        users = json.load(f)
    
    # Create SQLite database
    conn = sqlite3.connect('sanchari.db')
    # Insert data...
```

2. **Test migration on copy of data**
3. **Schedule maintenance window**
4. **Execute migration**
5. **Verify data integrity**

This approach ensures your data remains safe and accessible while providing a clear upgrade path as your platform grows.

