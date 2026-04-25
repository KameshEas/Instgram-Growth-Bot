# 🤖 Telegram Instagram Growth Bot - MVP

Telegram bot for generating high-quality image generation prompts and trending topic detection using free APIs.

## ✅ What's Included (MVP)

- **Content Generation Agent**: 110+ professional photography, design, and content prompts organized by category
- **Trends Agent**: Real-time trending topics from Reddit, GitHub, and News APIs (no API keys needed)
- **Analytics Agent**: Simulated metrics dashboard for growth projection
- **Engagement Agent**: Strategy recommendations and best practices (not automation)
- **Telegram Interface**: Easy-to-use bot commands for all features
- **Zero Dependencies**: Uses only free APIs, no paid integrations

## ❌ Out of Scope (Not Included)

- ❌ Instagram API integration (no actual posting)
- ❌ Image generation (DALL-E, Midjourney, Stable Diffusion not integrated)
- ❌ Automation (no real account management)
- ❌ Database (uses in-memory storage for MVP)
- ❌ Real monetization tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Virtual environment (venv/conda)
- Telegram bot token (from @BotFather on Telegram)
- Groq API key (free tier, from console.groq.com)

### Installation

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env

# 4. Add your tokens to .env
# TELEGRAM_BOT_TOKEN=your_token_here
# GROQ_API_KEY=your_groq_key_here
```

### Run the Bot

**Option 1: Python Script**
```bash
python run_telegram_bot.py
```

**Option 2: PowerShell (Windows)**
```powershell
.\start_telegram_bot.ps1
```

**Option 3: Batch File (Windows)**
```batch
start_telegram_bot.bat
```

### Verify Bot is Running

The bot starts polling for messages. You should see:
```
[INFO] Starting bot...
[INFO] Bot is running and listening for commands...
```

## 📋 Available Commands

### `/start`
Welcome message with bot introduction

**Usage**: `/start`

### `/help`
List all available commands

**Usage**: `/help`

### `/generate <category>`
Generate image generation prompts from library

**Usage**: `/generate women_professional`

**Available Categories**:
- `general_photography` - General Indian photography prompts
- `women_professional` - Professional women photoshoots
- `women_transform` - Style transfer templates for women
- `men_professional` - Professional men photoshoots
- `men_transform` - Style transfer templates for men
- `couples_general` - Couple photography prompts
- `couples_transform` - Couple style transfer templates
- `design_posters` - Social media design and poster prompts
- `reel_scripts` - Instagram Reel script ideas
- `captions_templates` - Caption and hashtag templates
- `email_subjects` - Email subject line ideas

### `/trending`
Get current trending topics from real-time sources (Reddit, GitHub, News)

**Usage**: `/trending`

**Response includes**:
- Hot topics from Reddit
- Trending GitHub repositories
- Top news headlines

### `/engagement <niche>`
Get organic growth strategies and engagement tips

**Usage**: `/engagement photography`

**Response includes**:
- Growth strategies with expected impact
- Daily time investment needed
- Projected monthly follower growth
- Growth tips by priority
- Hashtag strategy
- Optimal posting schedule
- Comment templates

### `/analytics <type>`
View simulated growth analytics and metrics

**Types**: `daily`, `weekly`, `monthly`

**Usage**: `/analytics weekly`

**Response includes**:
- Growth metrics
- Engagement rates
- Revenue projections
- Content performance
- Growth recommendations

### `/monetize`
Get monetization ideas and revenue stream suggestions

**Usage**: `/monetize`

**Response includes**:
- 6 revenue stream ideas
- Implementation strategies
- Expected earnings by follower count
- Timeline to profitability

### `/settings`
Configure bot preferences

**Usage**: `/settings`

## 📊 Sample Workflow

```
1. User: /trending
   Bot: Returns 15 trending topics from real APIs

2. User: /generate women_professional
   Bot: Returns 3 professional photography prompts

3. User: /engagement photography
   Bot: Returns 5 growth strategies with details

4. User: /analytics weekly
   Bot: Shows weekly simulated metrics and recommendations

5. User: /monetize
   Bot: Shows 6 revenue stream ideas
```

## 🔧 Configuration

Edit `.env` file to customize:

```bash
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token

# LLM (Groq)
GROQ_API_KEY=your_groq_key
GROQ_MODEL=mixtral-8x7b-32768  # You can change model
GROQ_TEMPERATURE=0.7

# Environment
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
```

## 📁 Project Structure

```
telegram-insta-bot/
├── src/
│   ├── agents/              # 9 specialized agents
│   │   ├── base_agent.py
│   │   ├── content_generator.py    # Prompt generation
│   │   ├── trends_agent.py         # Real API trending
│   │   ├── engagement_agent.py     # Tips & strategies
│   │   ├── analytics_agent.py      # Simulated metrics
│   │   ├── orchestrator.py         # Command routing
│   │   ├── telegram_handler.py     # Bot interface
│   │   └── ...
│   ├── prompts/
│   │   └── templates.py     # 110+ prompt library
│   ├── main.py              # Entry point
│   ├── telegram_bot.py      # Bot handlers
│   ├── config.py            # Settings
│   └── logger.py            # Logging
├── requirements.txt         # Minimal dependencies
├── .env.example
├── README.md               # This file
└── run_telegram_bot.py    # Runner script
```

## 🔌 Tech Stack

- **Python 3.10+**: Core language
- **python-telegram-bot**: Telegram interface
- **Groq API**: LLM (for potential enhancements)
- **LangChain**: Orchestration framework
- **Requests + BeautifulSoup**: Web scraping for trends
- **Pydantic**: Data validation

## 📈 Project Roadmap

### Phase 1: MVP (Current) ✅
- ✅ Content generation (prompts)
- ✅ Trend detection (real APIs)
- ✅ Engagement tips
- ✅ Analytics simulation
- ✅ Telegram interface

### Phase 2: Web UI (Future)
- [ ] React dashboard for analytics
- [ ] Prompt library browser
- [ ] Trend tracker visualization

### Phase 3: Advanced Features (Future)
- [ ] Instagram API integration
- [ ] Image generation provider
- [ ] Real database storage
- [ ] User preferences tracking

### Phase 4: Monetization (Future)
- [ ] Affiliate link generation
- [ ] Revenue tracking
- [ ] Sponsorship management

## 🎯 Common Use Cases

### 1. Get Content Ideas
```
/trending → /generate [category]
```

### 2. Plan Content Strategy
```
/engagement [niche] → /analytics weekly
```

### 3. Growth Planning
```
/trending → /engagement [niche] → /monetize
```

### 4. Monetization Planning
```
/analytics monthly → /monetize
```

## 📞 Troubleshooting

**Bot not responding:**
```bash
# Check logs
tail -f logs/bot.log

# Verify token
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.telegram.org/botYOUR_TOKEN/getMe
```

**Rate limiting from APIs:**
- Trends are cached for 6 hours to avoid rate limits
- Each API call includes retry logic

**Missing dependencies:**
```bash
pip install -r requirements.txt --upgrade
```

## 📝 Notes

- All data is **simulated** (MVP demonstration)
- Trends fetch real data from Reddit, GitHub, Hacker News
- Prompts are from professional photography libraries
- No actual Instagram posting/automation
- No database - uses in-memory storage

## 🎓 Learning Resources

- [Telegram Bot API](https://core.telegram.org/bots)
- [python-telegram-bot Docs](https://python-telegram-bot.readthedocs.io)
- [LangChain Docs](https://python.langchain.com)
- [Image Generation Prompt Guide](../image_generation_prompts.md)

## 📄 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

To improve the project:

1. Add more prompt categories in `src/prompts/templates.py`
2. Implement additional trend APIs in `trends_agent.py`
3. Add new engagement strategies in `engagement_agent.py`
4. Create better metrics in `analytics_agent.py`

## 🐛 Reporting Issues

If you find bugs:

1. Check the logs: `logs/bot.log`
2. Verify your `.env` configuration
3. Ensure all dependencies are installed
4. Check API rate limits

---

**Last Updated**: April 2026  
**Status**: MVP (Fully Functional)
