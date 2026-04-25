# 🚀 Quick Start Guide - Local Development

## Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Git

## Setup (First Time - 10 minutes)

### 1. Navigate to Project
```bash
cd telegram-insta-bot
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
# Copy example to real .env
cp .env.example .env

# Edit .env and add your Groq API key (FREE):
# Visit: https://console.groq.com
# GROQ_API_KEY=gsk-xxx
```

### 5. Start Docker Services
```bash
docker-compose up -d

# Verify services started
docker-compose ps
# Should show: postgres (healthy), redis (healthy)
```

### 6. Run the Bot
```bash
python src/main.py
```

**Expected Output:**
```
======================================================================
🤖 TELEGRAM INSTAGRAM BOT - LOCAL DEVELOPMENT
======================================================================
✅ Environment: development
✅ Debug Mode: True
✅ LLM Model: gpt-4
✅ Database: PostgreSQL (async)
✅ Cache: Redis
✅ Prompts Available: 80+
======================================================================

📝 Starting Telegram Bot on http://localhost:8000
📚 API Docs: http://localhost:8000/docs
🔍 Health Check: http://localhost:8000/health

======================================================================
```

## Testing

### Health Check
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","environment":"development"}
```

### API Documentation
Open browser: **http://localhost:8000/docs**

## Stopping Services

```bash
# Stop Python bot (Ctrl+C in terminal)

# Stop Docker services
docker-compose down
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows
```

### Database Connection Error
```bash
# Check if postgres is running
docker-compose logs postgres

# Restart services
docker-compose restart
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### OPENAI_API_KEY Not Set
```bash
# Verify .env file exists and has OPENAI_API_KEY
cat .env

# The bot will still run but LLM features won't work
# This is OK for testing basic functionality
```

## Project Commands

### Development
```bash
# Run with auto-reload
python src/main.py

# Run tests
pytest tests/

# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

### Database
```bash
# View database
docker exec -it telegram_bot_postgres psql -U postgres -d telegram_bot

# View database logs
docker-compose logs postgres
```

### Redis
```bash
# Connect to Redis CLI
docker exec -it telegram_bot_redis redis-cli

# Check Redis keys
docker exec -it telegram_bot_redis redis-cli KEYS "*"
```

## Next Steps

1. ✅ Verify bot runs locally
2. 🧪 Test Telegram webhook manually
3. 🎯 Implement more agents (content generator, Instagram integration, etc.)
4. 📦 Push to GitHub
5. 🚀 Deploy to Railway.app

## Project Structure

```
telegram-insta-bot/
├── src/
│   ├── main.py                      # Entry point
│   ├── config.py                    # Configuration
│   ├── logger.py                    # Logging
│   ├── core/
│   │   ├── bot_app.py              # FastAPI app (✅ Ready)
│   │   └── langchain_setup.py      # LangChain (✅ Ready)
│   ├── agents/
│   │   ├── base_agent.py           # Base class (✅ Ready)
│   │   ├── telegram_handler.py     # Telegram handler (✅ Ready)
│   │   └── orchestrator.py         # Router (✅ Ready)
│   ├── models/
│   │   └── database.py             # DB models (✅ Ready)
│   ├── database/
│   │   └── connection.py           # DB connection (✅ Ready)
│   ├── prompts/
│   │   └── templates.py            # 80+ prompts (✅ Ready)
│   └── (other modules)
├── tests/                           # Unit tests
├── migrations/                      # DB migrations
├── docker-compose.yml               # Local dev (✅ Ready)
├── requirements.txt                 # Dependencies (✅ Ready)
└── README.md
```

## Files Ready to Use

✅ `.env.example` - Environment template  
✅ `.gitignore` - Git ignore rules  
✅ `docker-compose.yml` - PostgreSQL + Redis setup  
✅ `requirements.txt` - All Python dependencies  
✅ `src/main.py` - Entry point  
✅ `src/config.py` - Settings management  
✅ `src/logger.py` - Logging setup  
✅ `src/core/bot_app.py` - FastAPI application  
✅ `src/core/langchain_setup.py` - LangChain LLM  
✅ `src/agents/base_agent.py` - Agent base class  
✅ `src/agents/telegram_handler.py` - Telegram parsing  
✅ `src/agents/orchestrator.py` - Message routing  
✅ `src/models/database.py` - Database models  
✅ `src/database/connection.py` - DB connection pool  
✅ `src/prompts/templates.py` - 80+ ready-to-use prompts  

## Git Setup

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial project setup - boilerplate with agents + 80+ prompts"

# Create GitHub repo, then:
git remote add origin https://github.com/YOUR_USERNAME/telegram-insta-bot.git
git branch -M main
git push -u origin main
```

## Support

For issues or questions, check:
1. `docker-compose logs postgres` - Database logs
2. `docker-compose logs redis` - Cache logs
3. `.env` file - Configuration
4. `requirements.txt` - Dependencies

---

**Ready to go!** 🚀 Your local development environment is fully set up.
