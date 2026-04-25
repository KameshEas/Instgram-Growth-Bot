# 🌐 Deployment Guide

Complete guide to deploying the Instagram Growth Bot to production environments.

## Table of Contents

1. [Local Deployment](#local-deployment)
2. [Railway.app (Recommended)](#railwayapp-recommended)
3. [Docker Containerization](#docker-containerization)
4. [Environment Setup](#environment-setup)
5. [Monitoring & Logging](#monitoring--logging)
6. [Troubleshooting](#troubleshooting)

---

## Local Deployment

### Prerequisites

- Python 3.14+ installed
- Groq API key
- ~100 MB disk space (without venv)

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd telegram-insta-bot
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements-minimal.txt
```

### Step 4: Configure Environment

Create `.env` file:

```env
# API Configuration
GROQ_API_KEY=gsk_YOUR_API_KEY_HERE
GROQ_MODEL=llama-3.1-8b-instant
GROQ_TEMPERATURE=0.7

# Logging
LOG_LEVEL=INFO

# Optional: Future Database
# DATABASE_URL=postgresql://user:pass@localhost:5432/bot
# REDIS_URL=redis://localhost:6379
```

### Step 5: Run Bot

```bash
# One-time run
python src/main.py

# Or schedule with task scheduler (Windows)
# See "Scheduling" section below
```

### Step 6: Set Up Task Scheduling

#### Windows Task Scheduler

```batch
# Create batch file: run_bot.bat
@echo off
cd E:\AI Development\Insta Growth\telegram-insta-bot
call venv\Scripts\activate.bat
python src/main.py > logs\bot_%date%.log 2>&1
pause
```

Then in Task Scheduler:
1. Create Basic Task
2. Trigger: Daily at 9 AM
3. Action: Start Program: `C:\path\to\run_bot.bat`
4. Add to startup (optional)

#### Linux/Mac Cron

```bash
# Edit crontab
crontab -e

# Add:
0 9 * * * cd /path/to/bot && /usr/bin/python3 src/main.py >> logs/bot.log 2>&1
```

---

## Railway.app (Recommended)

Railway is the easiest way to deploy Python apps. Free tier available.

### Step 1: Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Instagram Growth Bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/insta-growth-bot.git
git push -u origin main
```

**Important:** Add to `.gitignore`:
```
.env
venv/
__pycache__/
*.pyc
.DS_Store
logs/
```

### Step 2: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `insta-growth-bot` repository

### Step 3: Configure Environment Variables

In Railway dashboard:
1. Go to "Variables" tab
2. Add:
   ```
   GROQ_API_KEY=gsk_YOUR_KEY
   GROQ_MODEL=llama-3.1-8b-instant
   GROQ_TEMPERATURE=0.7
   LOG_LEVEL=INFO
   PYTHON_VERSION=3.14
   ```

### Step 4: Set Start Command

In Railway "Settings" tab:
```
python src/main.py
```

### Step 5: Deploy

1. Connect your GitHub account
2. Select repository and branch
3. Railway auto-deploys on push
4. View logs in Railway dashboard

### Step 6: Set Up Scheduled Runs (Optional)

Use Railway Cron plugin:
1. Add "Cron" to project
2. Set interval: `0 9 * * *` (9 AM daily)
3. Webhook will trigger bot run

---

## Docker Containerization

Build Docker image for consistent deployment across environments.

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.14-slim

WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements-minimal.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-minimal.txt

# Copy application code
COPY src/ src/
COPY .env .env

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)"

# Run bot
CMD ["python", "src/main.py"]
```

### Step 2: Create .dockerignore

```
.env
.git
venv
__pycache__
*.pyc
.DS_Store
logs
tests
```

### Step 3: Build & Run Locally

```bash
# Build image
docker build -t insta-growth-bot:1.0 .

# Run container
docker run \
  -e GROQ_API_KEY=gsk_YOUR_KEY \
  -e GROQ_MODEL=llama-3.1-8b-instant \
  insta-growth-bot:1.0
```

### Step 4: Push to Docker Hub

```bash
# Tag image
docker tag insta-growth-bot:1.0 YOUR_USERNAME/insta-growth-bot:1.0

# Push to registry
docker push YOUR_USERNAME/insta-growth-bot:1.0
```

### Step 5: Deploy to Container Services

#### Using Railway (Docker)
```bash
railway link  # Link to project
railway up    # Deploy using Dockerfile
```

#### Using Google Cloud Run
```bash
gcloud run deploy insta-growth-bot \
  --image gcr.io/PROJECT_ID/insta-growth-bot \
  --set-env-vars GROQ_API_KEY=gsk_YOUR_KEY
```

#### Using AWS ECS
```bash
# Create ECS task definition
aws ecs register-task-definition \
  --family insta-growth-bot \
  --container-definitions file://task-definition.json
```

---

## Environment Setup

### Production .env Template

```env
# ============================================
# GROQ API Configuration
# ============================================
GROQ_API_KEY=gsk_YOUR_FREE_API_KEY_HERE
GROQ_MODEL=llama-3.1-8b-instant
GROQ_TEMPERATURE=0.7

# ============================================
# Logging Configuration
# ============================================
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
LOG_MAX_BYTES=10485760  # 10 MB
LOG_BACKUP_COUNT=5

# ============================================
# Scheduling (Optional)
# ============================================
SCHEDULE_ENABLED=true
SCHEDULE_TIME=09:00  # 9 AM UTC
SCHEDULE_TIMEZONE=UTC

# ============================================
# Database (Optional - Future)
# ============================================
# DATABASE_URL=postgresql://user:pass@localhost:5432/bot
# DATABASE_POOL_SIZE=20
# DATABASE_MAX_OVERFLOW=40

# ============================================
# Redis Cache (Optional - Future)
# ============================================
# REDIS_URL=redis://localhost:6379
# REDIS_TTL=3600

# ============================================
# Monitoring & Alerts (Optional)
# ============================================
# SENTRY_DSN=https://YOUR_SENTRY_KEY@sentry.io/PROJECT_ID
# SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR_WEBHOOK

# ============================================
# Performance Tuning
# ============================================
REQUEST_TIMEOUT=30
RETRY_ATTEMPTS=3
RETRY_DELAY=2
```

### Secret Management

**Never commit `.env` files!**

#### Using Environment Variables (Recommended)

```bash
# On Linux/Mac
export GROQ_API_KEY=gsk_YOUR_KEY
export GROQ_MODEL=llama-3.1-8b-instant

# On Windows PowerShell
$env:GROQ_API_KEY = "gsk_YOUR_KEY"
$env:GROQ_MODEL = "llama-3.1-8b-instant"
```

#### Using Secret Management Services

- **Railway:** Built-in Variables tab
- **GitHub Actions:** Secrets tab
- **AWS Secrets Manager:** For production
- **HashiCorp Vault:** Enterprise solution

---

## Monitoring & Logging

### Log Structure

Logs are written to `logs/bot.log`:

```
2026-04-23 12:48:14,254 - __main__ - INFO - ============================================================
2026-04-23 12:48:14,255 - __main__ - INFO - 🤖 Instagram Growth Bot Started
2026-04-23 12:48:15,904 - httpx - INFO - HTTP Request: POST https://api.groq.com/... "HTTP/1.1 200 OK"
2026-04-23 12:48:15,918 - __main__ - INFO - ✅ Generated 3 captions
```

### View Logs in Real-Time

```bash
# Linux/Mac
tail -f logs/bot.log

# Windows PowerShell
Get-Content logs/bot.log -Wait

# Docker
docker logs -f CONTAINER_ID
```

### Log Levels

| Level | Usage | Example |
|-------|-------|---------|
| DEBUG | Detailed information | API request details |
| INFO | General information | Bot started, results |
| WARNING | Warning messages | Slow responses |
| ERROR | Error conditions | Failed API calls |
| CRITICAL | Severe errors | API key missing |

### Set Log Level

```python
# In src/main.py
import logging

# Change to DEBUG for verbose logging
logging.basicConfig(level=logging.DEBUG)
```

### Integration with Monitoring Services

#### Sentry (Error Tracking)

```bash
pip install sentry-sdk
```

```python
import sentry_sdk
sentry_sdk.init("https://YOUR_KEY@sentry.io/PROJECT_ID")
```

#### DataDog (APM)

```bash
pip install datadog
```

#### New Relic (Monitoring)

```bash
pip install newrelic
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'groq'"

**Solution:**
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements-minimal.txt
```

### Issue: "GROQ_API_KEY not found"

**Solution:**
```bash
# Check .env file exists in project root
ls .env

# Set environment variable manually
export GROQ_API_KEY=gsk_YOUR_KEY
```

### Issue: "BadRequestError: Model decommissioned"

**Solution:**
Update `.env`:
```env
GROQ_MODEL=llama-3.1-8b-instant
```

### Issue: Railway Deploy Fails

**Solution:**
1. Check `.gitignore` includes `.env`
2. Verify `requirements-minimal.txt` exists
3. Ensure `src/main.py` exists and runs
4. Check Python version (3.14+)

### Issue: High Memory Usage

**Solution:**
- Bot uses ~50 MB per run
- If sustained high usage, reduce response context
- Add garbage collection: `import gc; gc.collect()`

### Issue: Slow API Responses

**Solution:**
- Groq free tier is shared (2-5 sec typical)
- Consider caching results
- Use `llama-3.1-8b-instant` (fastest)
- Reduce `temperature` for faster, more consistent results

---

## Performance Checklist

- [ ] .env file created with valid Groq API key
- [ ] Virtual environment activated
- [ ] All dependencies installed from `requirements-minimal.txt`
- [ ] Bot runs locally without errors
- [ ] Logs show successful API calls
- [ ] Task scheduler or cron job configured
- [ ] Monitoring/alerting set up (optional)
- [ ] Backup of configuration files
- [ ] Tested with production data

---

## Scaling to Production

### For Small Teams (< 10 accounts)
- Local server with cron job
- Cost: Free (Groq + local hardware)

### For Medium Growth (10-100 accounts)
- Railway.app or similar PaaS
- Add database (PostgreSQL)
- Cost: $5-50/month

### For Enterprise (100+ accounts)
- Kubernetes cluster
- Dedicated database
- Cache layer (Redis)
- Load balancing
- Cost: $100-1000+/month

---

**Questions?** Check README.md or ARCHITECTURE.md for more details.

Last Updated: April 23, 2026
