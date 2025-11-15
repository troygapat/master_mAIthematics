

# AI Math Tutor - Cloud Deployment Guide

Guide for deploying the AI Math Tutor to cloud platforms.

## Overview

This application can be deployed to various cloud platforms:
- **Streamlit Community Cloud** (easiest, free)
- **Heroku** (simple, paid)
- **AWS/GCP/Azure** (full control, scalable)
- **Docker** (containerized deployment)

## Prerequisites

- Git repository with your code
- Anthropic API key
- Cloud platform account

---

## Option 1: Streamlit Community Cloud (Recommended for Start)

**Pros**: Free, easy, built for Streamlit
**Cons**: Limited resources, public by default

### Steps:

1. **Prepare Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Create `requirements.txt`** (already included)

3. **Add `.streamlit/secrets.toml`**
   ```toml
   ANTHROPIC_API_KEY = "your-key-here"
   DATABASE_URL = "postgresql://..."
   SECRET_KEY = "your-secret-key"
   ```

4. **Deploy**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `app.py` as main file
   - Add secrets from above
   - Click Deploy!

### Database Setup for Streamlit Cloud

Use a cloud PostgreSQL database:
- **ElephantSQL** (free tier available)
- **Heroku Postgres**
- **AWS RDS**

Update `.streamlit/secrets.toml`:
```toml
DATABASE_URL = "postgresql://user:pass@host:5432/dbname"
```

---

## Option 2: Heroku Deployment

**Pros**: Easy deployment, good scaling options
**Cons**: Paid (no free tier anymore)

### Steps:

1. **Create `Procfile`**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create `setup.sh`**
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   ```

3. **Update `requirements.txt`**
   (already set up correctly)

4. **Deploy**
   ```bash
   heroku login
   heroku create your-math-tutor
   heroku addons:create heroku-postgresql:mini
   heroku config:set ANTHROPIC_API_KEY=your-key
   heroku config:set SECRET_KEY=your-secret-key
   git push heroku main
   ```

---

## Option 3: Docker Deployment

**Pros**: Portable, consistent environments
**Cons**: Requires Docker knowledge

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create data directory
RUN mkdir -p data

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - DATABASE_URL=postgresql://postgres:password@db:5432/mathtutor
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    volumes:
      - ./data:/app/data

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=mathtutor
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Deploy with Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Option 4: AWS Deployment

**Pros**: Full control, highly scalable
**Cons**: More complex, requires AWS knowledge

### Using AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB**
   ```bash
   eb init -p python-3.11 math-tutor
   ```

3. **Create environment**
   ```bash
   eb create math-tutor-env
   ```

4. **Set environment variables**
   ```bash
   eb setenv ANTHROPIC_API_KEY=your-key
   eb setenv SECRET_KEY=your-secret-key
   eb setenv DATABASE_URL=your-postgres-url
   ```

5. **Deploy**
   ```bash
   eb deploy
   ```

### Using AWS EC2 + RDS

1. **Set up RDS PostgreSQL**
   - Create PostgreSQL instance
   - Note connection details

2. **Launch EC2 instance**
   - Choose Ubuntu/Amazon Linux
   - Configure security groups (allow 8501, 22)

3. **Install on EC2**
   ```bash
   # SSH into instance
   ssh -i your-key.pem ec2-user@your-instance

   # Install dependencies
   sudo yum install python3 git
   pip3 install virtualenv

   # Clone repository
   git clone your-repo
   cd math_tutor

   # Set up
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # Configure environment
   nano .env
   # Add your API keys and DATABASE_URL

   # Run with screen/tmux
   screen
   streamlit run app.py
   ```

4. **Set up Nginx (optional)**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
       }
   }
   ```

---

## Production Configuration

### Environment Variables

Set these in your deployment platform:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-xxx
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=generate-a-random-secret-key

# Optional
APP_ENV=production
AI_MODEL=claude-3-5-sonnet-20241022
AI_MAX_TOKENS=4096
SESSION_TIMEOUT_MINUTES=60
ENABLE_AUTHENTICATION=True
DEBUG=False
```

### Generate Secret Key

```python
import secrets
print(secrets.token_urlsafe(32))
```

### Database Migration

For PostgreSQL, update connection in production:

```python
# In .env
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

Run migrations:
```bash
python src/database/init_db.py --url $DATABASE_URL
```

---

## Security Considerations

### Enable Authentication

1. **Set environment variable**
   ```bash
   ENABLE_AUTHENTICATION=True
   ```

2. **Users must register/login**
   - Authentication will be required on all pages
   - JWT tokens for session management
   - Password hashing with bcrypt

### SSL/HTTPS

**For production, always use HTTPS:**

- **Streamlit Cloud**: Automatic HTTPS
- **Heroku**: Automatic HTTPS
- **AWS/EC2**: Use AWS Certificate Manager + Load Balancer
- **Nginx**: Use Let's Encrypt

```bash
# Let's Encrypt with Certbot
sudo certbot --nginx -d your-domain.com
```

### API Key Security

✅ **DO:**
- Store API keys in environment variables
- Use secrets management (AWS Secrets Manager, etc.)
- Rotate keys periodically
- Limit API key permissions

❌ **DON'T:**
- Commit API keys to git
- Share API keys
- Use same key for dev and production
- Log API keys

---

## Monitoring and Logging

### Application Logs

```python
# Add logging to app.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Monitor API Usage

Track Anthropic API usage:
- Set up alerts for high usage
- Monitor token consumption
- Track error rates

### Health Checks

Add health check endpoint:

```python
# health.py
def health_check():
    try:
        # Check database
        db.get_session()
        # Check AI client
        ai_client.chat("test", [{"role": "user", "content": "hi"}])
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

---

## Performance Optimization

### Database Connection Pooling

```python
# For PostgreSQL
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10
)
```

### Caching

Streamlit has built-in caching:

```python
@st.cache_data(ttl=3600)
def expensive_computation():
    # Results cached for 1 hour
    pass

@st.cache_resource
def get_database_connection():
    # Connection reused
    pass
```

### Rate Limiting

Implement rate limiting for API calls:

```python
from functools import wraps
import time

def rate_limit(max_calls=60, period=60):
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if c > now - period]
            
            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## Backup and Recovery

### Database Backups

**PostgreSQL:**
```bash
# Backup
pg_dump $DATABASE_URL > backup.sql

# Restore
psql $DATABASE_URL < backup.sql
```

**Automated backups:**
- Use platform's backup features (RDS snapshots, Heroku backups)
- Schedule daily backups
- Test restore process

### Application Backups

```bash
# Backup data directory
tar -czf data-backup-$(date +%Y%m%d).tar.gz data/

# Store in S3 or similar
aws s3 cp data-backup-*.tar.gz s3://your-backup-bucket/
```

---

## Scaling Considerations

### Vertical Scaling
- Increase instance size
- More RAM for database
- Faster CPU

### Horizontal Scaling
- Multiple Streamlit instances behind load balancer
- Shared PostgreSQL database
- Redis for session management

### Database Scaling
- Read replicas for PostgreSQL
- Connection pooling
- Query optimization

---

## Cost Optimization

### Anthropic API Costs

- **GPT-4 level model**: ~$0.03 per 1K input tokens, $0.06 per 1K output tokens
- **Average conversation**: 50-100 messages
- **Estimated cost per student per month**: $5-20

**Optimization strategies:**
1. Cache common responses
2. Truncate conversation history aggressively
3. Use lower temperature for simpler queries
4. Set max token limits appropriately

### Infrastructure Costs

**Streamlit Cloud**: Free (with limits)
**Heroku**: ~$7-$25/month
**AWS**: ~$20-$100/month (varies widely)

---

## Maintenance Checklist

### Weekly
- [ ] Check error logs
- [ ] Monitor API usage
- [ ] Review user feedback

### Monthly
- [ ] Database backup verification
- [ ] Security updates
- [ ] Performance review
- [ ] Cost analysis

### Quarterly
- [ ] Dependency updates
- [ ] Security audit
- [ ] Feature usage analysis
- [ ] Capacity planning

---

## Troubleshooting

### Common Issues

**"Database connection failed"**
- Check DATABASE_URL format
- Verify database is running
- Check firewall rules

**"API key invalid"**
- Verify ANTHROPIC_API_KEY is set
- Check for extra spaces
- Ensure key is active

**"Out of memory"**
- Increase instance size
- Optimize conversation history
- Add connection pooling

---

## Support

For deployment issues:
1. Check application logs
2. Verify environment variables
3. Test database connection
4. Review platform documentation

---

**Ready to deploy? Start with Streamlit Cloud for the easiest setup!** 🚀

