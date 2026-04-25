# 🤖 Telegram Instagram Growth Bot

AI-powered Telegram bot for Instagram content generation and growth automation using LangChain + Python.

## Features

✅ **Content Generation**: Generate 110+ AI-optimized prompts for photography, designs, captions, reels  
✅ **Multi-Agent System**: 9 specialized agents for different tasks  
✅ **Instagram Integration**: Auto-posting and engagement automation  
✅ **Revenue Streams**: Track affiliate links, sponsored posts, digital products  
✅ **Analytics Dashboard**: Real-time growth and performance metrics  
✅ **Local Development**: Complete Docker setup for PostgreSQL + Redis  
✅ **Free Hosting**: Ready to deploy on Railway.app  

## Quick Start

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Git

### Installation

```bash
# Clone or create project
cd telegram-insta-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Start Docker services
docker-compose up -d

# Run bot
python src/main.py
```

### Health Check
```bash
curl http://localhost:8000/health
```

### API Documentation
Open browser: **http://localhost:8000/docs**

## 🤖 9 AI Agents

| Agent | Purpose | Commands |
|-------|---------|----------|
| **ContentGenerator** | Generate viral content with 110+ prompts | `/generate`, `/create` |
| **InstagramIntegration** | Auto-post, schedule, cross-post | `/post`, `/schedule`, `/cross_post` |
| **Engagement** | Safe follower growth (anti-bot) | `/engage`, `/follow`, `/comment`, `/dm` |
| **Monetization** | Track 6 revenue streams | `/revenue`, `/affiliate`, `/sponsored` |
| **Analytics** | Daily/weekly/monthly reports | `/analytics`, `/report`, `/stats` |
| **Trends** | Detect trending topics & forecast virality | `/trends`, `/viral`, `/hashtags` |
| **Privacy** | Data encryption & compliance (GDPR) | `/security`, `/privacy`, `/backup` |
| **TelegramHandler** | Parse & route Telegram commands | (automatic) |
| **Orchestrator** | Master router to all agents | `/help` |

**See [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for detailed agent documentation.**

## Project Structure

```
telegram-insta-bot/
├── src/
│   ├── main.py                      # Entry point
│   ├── config.py                    # Configuration (Groq API)
│   ├── logger.py                    # Logging setup
│   ├── core/
│   │   ├── bot_app.py              # FastAPI app
│   │   └── langchain_setup.py      # LangChain + Groq init
│   ├── agents/
│   │   ├── base_agent.py           # Base abstract class
│   │   ├── telegram_handler.py     # Parse Telegram commands
│   │   ├── orchestrator.py         # Master router
│   │   ├── content_generator.py    # Generate content ⭐ NEW
│   │   ├── instagram_agent.py      # Auto-posting ⭐ NEW
│   │   ├── engagement_agent.py     # Safe growth ⭐ NEW
│   │   ├── monetization_agent.py   # Revenue tracking ⭐ NEW
│   │   ├── analytics_agent.py      # Reports ⭐ NEW
│   │   ├── trends_agent.py         # Trending topics ⭐ NEW
│   │   └── privacy_agent.py        # Security & GDPR ⭐ NEW
│   ├── models/
│   │   └── database.py             # DB models (4 tables)
│   ├── database/
│   │   └── connection.py           # Async connection pool
│   ├── prompts/
│   │   └── templates.py            # 110+ prompt templates
│   └── (other modules)
├── tests/
│   └── test_agents_integration.py   # Agent test suite
├── migrations/                      # DB migrations
├── docker-compose.yml               # PostgreSQL setup
├── requirements.txt                 # 45+ dependencies
├── .env.example                     # Config template
├── IMPLEMENTATION_GUIDE.md          # Detailed guide ⭐ NEW
├── QUICKSTART.md                    # Quick setup
└── README.md
```

## Deployment

### Railway.app (Recommended)
1. Push to GitHub
2. Connect Repository on Railway.app
3. Set environment variables
4. Deploy (auto-deploys on git push)

## Documentation

See QUICKSTART.md for detailed setup guide.

## Tech Stack

- **Framework**: FastAPI + python-telegram-bot
- **AI/LLM**: LangChain + Groq (FREE API)
- **Database**: PostgreSQL (async)
- **Cache**: Redis
- **Queue**: Celery
- **Hosting**: Railway.app

## License

MIT License
