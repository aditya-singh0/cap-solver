# 🚀 Deployment Guide

This guide covers deploying the Captcha Solver SaaS application to various platforms.

## Prerequisites

- Docker and Docker Compose installed
- Google Cloud Project with Gemini API enabled
- Razorpay account (for payments)
- Domain name (optional)

## Local Development

### 1. Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd cap-solver

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Start the application
docker-compose up -d
```

### 2. Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp env.example .env

# Edit .env with your API keys
nano .env

# Start services
docker-compose up -d
```

### 3. Environment Variables

Create a `.env` file with the following variables:

```env
# Application
APP_NAME=Captcha Solver SaaS
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ENVIRONMENT=production

# Database
DATABASE_URL=postgresql://cap_solver:password@postgres:5432/cap_solver_db

# Redis
REDIS_URL=redis://redis:6379/0

# Google Gemini API
GOOGLE_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-pro-vision

# Razorpay
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-secret

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# File Upload
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,bmp,webp

# CORS
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# Logging
LOG_LEVEL=INFO
```

## Production Deployment

### Option 1: Docker Compose (Recommended)

```bash
# Production environment
export ENVIRONMENT=production
export SECRET_KEY=$(openssl rand -hex 32)

# Start services
docker-compose -f docker-compose.yml up -d

# Check logs
docker-compose logs -f app
```

### Option 2: Kubernetes

Create a `k8s` directory with the following files:

#### `k8s/deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cap-solver-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cap-solver
  template:
    metadata:
      labels:
        app: cap-solver
    spec:
      containers:
      - name: app
        image: your-registry/cap-solver:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: cap-solver-secrets
              key: database-url
        - name: GOOGLE_API_KEY
          valueFrom:
            secretKeyRef:
              name: cap-solver-secrets
              key: google-api-key
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: cap-solver-secrets
              key: secret-key
```

#### `k8s/service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: cap-solver-service
spec:
  selector:
    app: cap-solver
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

#### `k8s/ingress.yaml`
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: cap-solver-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: api.cap-solver.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: cap-solver-service
            port:
              number: 80
```

### Option 3: Cloud Platforms

#### AWS ECS

1. **Create ECR Repository:**
```bash
aws ecr create-repository --repository-name cap-solver
```

2. **Build and Push Image:**
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
docker build -t cap-solver .
docker tag cap-solver:latest your-account.dkr.ecr.us-east-1.amazonaws.com/cap-solver:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/cap-solver:latest
```

3. **Create ECS Task Definition:**
```json
{
  "family": "cap-solver",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::your-account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "cap-solver",
      "image": "your-account.dkr.ecr.us-east-1.amazonaws.com/cap-solver:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "GOOGLE_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:your-account:secret:cap-solver/google-api-key"
        }
      ]
    }
  ]
}
```

#### Google Cloud Run

1. **Build and Deploy:**
```bash
# Build image
docker build -t gcr.io/your-project/cap-solver .

# Push to Container Registry
docker push gcr.io/your-project/cap-solver

# Deploy to Cloud Run
gcloud run deploy cap-solver \
  --image gcr.io/your-project/cap-solver \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=production \
  --set-secrets GOOGLE_API_KEY=google-api-key:latest
```

#### Heroku

1. **Create Heroku App:**
```bash
heroku create your-cap-solver-app
```

2. **Add PostgreSQL:**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

3. **Add Redis:**
```bash
heroku addons:create heroku-redis:hobby-dev
```

4. **Set Environment Variables:**
```bash
heroku config:set GOOGLE_API_KEY=your-api-key
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ENVIRONMENT=production
```

5. **Deploy:**
```bash
git push heroku main
```

## Database Setup

### PostgreSQL Migration

1. **Create Database:**
```sql
CREATE DATABASE cap_solver_db;
CREATE USER cap_solver WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE cap_solver_db TO cap_solver;
```

2. **Run Migrations:**
```bash
# Create migration files
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### Redis Setup

Redis is used for caching and rate limiting. The Docker Compose setup includes Redis automatically.

## SSL/TLS Configuration

### Using Let's Encrypt with Nginx

1. **Install Certbot:**
```bash
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx
```

2. **Obtain Certificate:**
```bash
sudo certbot --nginx -d api.cap-solver.com
```

3. **Auto-renewal:**
```bash
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Using Cloudflare

1. **Add Domain to Cloudflare**
2. **Set DNS Records:**
   - A record: `api.cap-solver.com` → Your server IP
   - CNAME record: `www.api.cap-solver.com` → `api.cap-solver.com`
3. **Enable SSL/TLS:**
   - Set SSL/TLS encryption mode to "Full (strict)"
   - Enable "Always Use HTTPS"

## Monitoring and Logging

### Application Monitoring

1. **Health Check Endpoint:**
```bash
curl https://api.cap-solver.com/health
```

2. **Prometheus Metrics:**
```python
# Add to requirements.txt
prometheus-client==0.17.1

# Add metrics endpoint
from prometheus_client import Counter, Histogram, generate_latest

solves_counter = Counter('captcha_solves_total', 'Total CAPTCHA solves')
solve_duration = Histogram('captcha_solve_duration_seconds', 'CAPTCHA solve duration')

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### Logging

The application uses structured logging with `structlog`. Logs are automatically formatted as JSON for easy parsing.

### Error Tracking

Add Sentry for error tracking:

```python
# Add to requirements.txt
sentry-sdk[fastapi]==1.38.0

# Add to main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
)
```

## Performance Optimization

### Caching

1. **Redis Caching:**
```python
import redis
from functools import wraps

redis_client = redis.Redis.from_url(settings.redis_url)

def cache_result(expiration=3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"captcha:{hash(str(args) + str(kwargs))}"
            cached = redis_client.get(cache_key)
            if cached:
                return cached.decode()
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, str(result))
            return result
        return wrapper
    return decorator
```

### Load Balancing

For high traffic, use multiple application instances behind a load balancer:

```yaml
# docker-compose.yml
services:
  app:
    deploy:
      replicas: 3
    environment:
      - REDIS_URL=redis://redis:6379/0
```

### Database Optimization

1. **Connection Pooling:**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True
)
```

2. **Indexes:**
```sql
-- Add indexes for better performance
CREATE INDEX idx_usage_records_user_id ON usage_records(user_id);
CREATE INDEX idx_usage_records_created_at ON usage_records(created_at);
CREATE INDEX idx_api_keys_key_hash ON api_keys(key_hash);
```

## Security Best Practices

1. **Environment Variables:**
   - Never commit secrets to version control
   - Use secret management services (AWS Secrets Manager, Google Secret Manager)
   - Rotate secrets regularly

2. **API Security:**
   - Rate limiting is enabled by default
   - API keys are hashed before storage
   - JWT tokens have expiration

3. **Network Security:**
   - Use HTTPS in production
   - Configure firewall rules
   - Enable CORS properly

4. **Database Security:**
   - Use strong passwords
   - Enable SSL connections
   - Regular backups

## Backup Strategy

### Database Backups

```bash
# PostgreSQL backup
pg_dump cap_solver_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Automated backup script
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > $BACKUP_DIR/backup_$DATE.sql
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

### File Storage Backups

If using local file storage, backup the uploads directory:

```bash
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz uploads/
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors:**
   - Check DATABASE_URL format
   - Verify PostgreSQL is running
   - Check firewall settings

2. **Redis Connection Errors:**
   - Verify Redis is running
   - Check REDIS_URL format
   - Check memory usage

3. **API Key Issues:**
   - Verify Google API key is valid
   - Check API quotas
   - Verify billing is enabled

4. **Rate Limiting:**
   - Check Redis connection
   - Verify rate limit configuration
   - Monitor usage patterns

### Debug Mode

Enable debug mode for troubleshooting:

```bash
export DEBUG=True
export LOG_LEVEL=DEBUG
```

### Log Analysis

```bash
# View application logs
docker-compose logs app

# Follow logs in real-time
docker-compose logs -f app

# Search for errors
docker-compose logs app | grep ERROR
```

## Scaling

### Horizontal Scaling

1. **Add More Instances:**
```bash
docker-compose up -d --scale app=3
```

2. **Load Balancer Configuration:**
```nginx
upstream cap_solver {
    server app1:8000;
    server app2:8000;
    server app3:8000;
}

server {
    listen 80;
    server_name api.cap-solver.com;
    
    location / {
        proxy_pass http://cap_solver;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Vertical Scaling

1. **Increase Resources:**
```yaml
# docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

2. **Database Scaling:**
   - Use managed PostgreSQL (AWS RDS, Google Cloud SQL)
   - Enable read replicas for read-heavy workloads
   - Implement connection pooling

## Cost Optimization

1. **Resource Monitoring:**
   - Monitor CPU and memory usage
   - Use auto-scaling based on metrics
   - Right-size instances

2. **API Cost Management:**
   - Monitor Gemini API usage
   - Implement caching to reduce API calls
   - Use appropriate rate limits

3. **Storage Optimization:**
   - Use object storage (S3, GCS) for file uploads
   - Implement file cleanup policies
   - Compress images before storage

## Support and Maintenance

### Regular Maintenance

1. **Security Updates:**
   - Keep dependencies updated
   - Monitor for security vulnerabilities
   - Apply patches promptly

2. **Performance Monitoring:**
   - Monitor response times
   - Track error rates
   - Monitor resource usage

3. **Backup Verification:**
   - Test backup restoration
   - Verify backup integrity
   - Document recovery procedures

### Support Channels

- **Documentation:** `/docs` endpoint for API documentation
- **Health Check:** `/health` endpoint for monitoring
- **Logs:** Structured logging for debugging
- **Metrics:** Prometheus metrics for monitoring 