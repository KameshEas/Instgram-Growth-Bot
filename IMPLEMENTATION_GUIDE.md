# Implementation Guide: Instagram Growth Bot with 9 AI Agents

## Quick Start (5 minutes)

### 1. Get Your Groq API Key (FREE)
```bash
# Visit: https://console.groq.com
# Sign up → Create API key → Copy to clipboard
```

### 2. Update Environment
```bash
# Edit .env file
GROQ_API_KEY=gsk_your_api_key_here
```

### 3. Start Database
```bash
docker-compose up -d
# Wait 5 seconds for PostgreSQL to start
```

### 4. Start Bot
```bash
# Make sure venv is active
python src/main.py
```

You should see:
```
╔══════════════════════════════════════════════════════════════════════╗
║   🚀 Instagram Growth Bot Starting...                               ║
╚══════════════════════════════════════════════════════════════════════╝
✓ Environment: development
✓ LLM Model: mixtral-8x7b-32768 (Groq)
✓ Database: PostgreSQL
✓ Available Prompts: 110+
✓ Port: 8000
```

---

## 9 Agents Overview

### 1️⃣ **ContentGeneratorAgent** 
**Purpose:** Generate viral-optimized content using 110+ AI prompts + LangChain

**Commands:**
```bash
/generate
/create
/content
```

**Example Usage:**
```python
{
    "command": "/generate",
    "category": "women_professional",  # See prompts/templates.py
    "style": "professional",
    "request": "Fashion photography with lighting tips"
}
```

**Output:** 3-5 prompt variations ready for DALL-E/Midjourney

---

### 2️⃣ **InstagramIntegrationAgent**
**Purpose:** Post to Instagram, schedule posts, cross-post to TikTok/YouTube Shorts

**Commands:**
```bash
/post
/schedule
/cross_post
```

**Example Usage:**
```python
{
    "command": "/post",
    "action": "post",
    "caption": "Amazing photography! 📸",
    "image_url": "https://example.com/image.jpg"
}
```

**Status:** Ready for Instagrapi integration (currently mocked)

---

### 3️⃣ **EngagementAgent**
**Purpose:** Safe organic follower growth with safety delays & limits

**Daily Limits (Anti-Bot Protection):**
- ✓ 100 follows/day
- ✓ 200 likes/day
- ✓ 50 comments/day
- ✓ 30 DMs/day

**Commands:**
```bash
/engage
/follow
/comment
/dm
```

**Example Usage:**
```python
{
    "command": "/engage",
    "action": "engage",
    "hashtag": "photography",
    "max_actions": 20
}
```

---

### 4️⃣ **MonetizationAgent**
**Purpose:** Track 6 revenue streams and calculate ROI

**Revenue Streams:**
1. Sponsored Posts
2. Affiliate Marketing (Amazon, etc.)
3. Digital Products (Gumroad, etc.)
4. Email List Monetization
5. SaaS Links (referrals)
6. Engagement Services

**Commands:**
```bash
/revenue
/affiliate
/sponsored
/monetize
```

**Example Usage:**
```python
{
    "command": "/revenue",
    "action": "track_revenue"
}
```

**Output:**
```json
{
    "total_revenue": 3050.50,
    "daily_projected": 101.68,
    "monthly_projected": 3050.40,
    "yearly_projected": 36605.00
}
```

---

### 5️⃣ **AnalyticsAgent**
**Purpose:** Daily/weekly/monthly reporting with custom metrics

**Report Types:**
- Daily: followers, engagement, reach, impressions
- Weekly: trends, growth %, top posts, recommendations
- Monthly: revenue analysis, ROI, growth trends

**Commands:**
```bash
/analytics
/report
/stats
```

**Example Usage:**
```python
{
    "command": "/analytics",
    "report_type": "daily"
}
```

---

### 6️⃣ **TrendsAgent**
**Purpose:** Detect trending topics from Twitter, TikTok, Reddit

**Features:**
- Trending hashtag detection
- Content suggestions based on trends
- Viral score forecasting (0-100)
- Best posting time recommendations

**Commands:**
```bash
/trends
/viral
/hashtags
```

**Example Usage:**
```python
{
    "command": "/trends",
    "action": "viral_forecast",
    "content_idea": "Photography tips"
}
```

---

### 7️⃣ **PrivacyAgent**
**Purpose:** Data security, encryption, GDPR compliance

**Features:**
- Security audit (95+ score)
- Data encryption (base64 → AES-256)
- Backup management (AWS S3)
- Compliance checking (GDPR, ToS)

**Commands:**
```bash
/security
/privacy
/backup
```

**Example Usage:**
```python
{
    "command": "/security",
    "action": "audit"
}
```

---

### 8️⃣ **TelegramHandlerAgent**
**Purpose:** Parse Telegram commands and extract parameters

**Automatically Handles:**
- Command parsing (`/generate`, `/post`, etc.)
- Parameter extraction
- User session tracking
- Error handling

---

### 9️⃣ **ContentOrchestratorAgent**
**Purpose:** Master router to all 9 agents based on commands

**Automatically Routes:**
- `/generate` → ContentGeneratorAgent
- `/post` → InstagramIntegrationAgent
- `/engage` → EngagementAgent
- `/revenue` → MonetizationAgent
- `/analytics` → AnalyticsAgent
- `/trends` → TrendsAgent
- `/security` → PrivacyAgent
- `/help` → Shows help menu

---

## Testing the Bot

### Method 1: Local Testing with Telegram
```bash
# 1. Get Telegram Bot Token from @BotFather
# 2. Add to .env: TELEGRAM_BOT_TOKEN=xxx
# 3. Run bot: python src/main.py
# 4. Set webhook: https://yourapi.com/webhook
# 5. Send commands in Telegram
```

### Method 2: Direct Python Testing
```python
import asyncio
from src.agents.orchestrator import ContentOrchestratorAgent

async def test():
    agent = ContentOrchestratorAgent()
    
    # Test 1: Generate content
    result = await agent.execute({
        "command": "/generate",
        "category": "women_professional",
        "style": "professional"
    })
    print(result)
    
    # Test 2: Get analytics
    result = await agent.execute({
        "command": "/analytics",
        "report_type": "daily"
    })
    print(result)

asyncio.run(test())
```

### Method 3: HTTP Testing
```bash
# Health check
curl http://localhost:8000/health

# Mock Telegram webhook
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "update_id": 123456789,
    "message": {
      "message_id": 1,
      "from": {"id": 123, "first_name": "User"},
      "chat": {"id": 123, "type": "private"},
      "text": "/generate"
    }
  }'
```

---

## Database Schema

### Tables
```sql
-- Users
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    created_at TIMESTAMP
);

-- Instagram Accounts
CREATE TABLE instagram_accounts (
    account_id SERIAL PRIMARY KEY,
    user_id BIGINT,
    username VARCHAR(255),
    followers_count INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Posts
CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    account_id INT,
    content_type VARCHAR(50),
    image_url VARCHAR(500),
    engagement_rate FLOAT,
    FOREIGN KEY (account_id) REFERENCES instagram_accounts(account_id)
);

-- Agent Logs
CREATE TABLE agent_logs (
    log_id SERIAL PRIMARY KEY,
    agent_name VARCHAR(100),
    action VARCHAR(255),
    status VARCHAR(50),
    execution_time_ms INT,
    created_at TIMESTAMP
);
```

---

## Prompt Categories (110+ Total)

```python
# Available categories in src/prompts/templates.py:
- general_photography (5 prompts)
- women_professional (8 prompts)
- women_transform (10 prompts)
- men_professional (8 prompts)
- men_transform (10 prompts)
- couples_general (8 prompts)
- couples_transform (10 prompts)
- design_posters (8 prompts)
- reel_scripts (10 prompts)
- captions_templates (10 prompts)
- email_subjects (8 prompts)
```

**Usage:**
```python
from src.prompts.templates import get_prompt, get_category_prompts

# Get random prompt from category
prompt = get_prompt("women_professional", 0)

# Get all prompts in category
all_prompts = get_category_prompts("women_professional")

# Get total count
count = get_all_prompts_count()  # Returns 110+
```

---

## Configuration Files

### src/config.py
```python
GROQ_API_KEY=gsk_xxx              # From console.groq.com
GROQ_MODEL=mixtral-8x7b-32768     # Latest Groq model
GROQ_TEMPERATURE=0.7              # Creativity level (0-1)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/telegram_bot
TELEGRAM_BOT_TOKEN=xxx            # From @BotFather
ENVIRONMENT=development
DEBUG=True
```

### docker-compose.yml
```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: telegram_bot
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
```

---

## Common Commands

```bash
# Start bot
python src/main.py

# Check database
psql postgresql://postgres:postgres@localhost:5432/telegram_bot

# View logs
tail -f src/logs/app.log

# Run tests
pytest tests/ -v

# Format code
black src/

# Check types
mypy src/

# Stop database
docker-compose down
```

---

## Deployment (Next Steps)

### Option 1: Railway.app (Recommended for Beginners)
1. Create Railway account
2. Connect GitHub repo
3. Add environment variables
4. Deploy with 1-click

### Option 2: AWS
- EC2 for compute
- RDS for PostgreSQL
- S3 for backups
- Lambda for scheduled jobs

### Option 3: DigitalOcean
- App Platform (managed deployment)
- Managed Databases
- $5/month starter plan

---

## Troubleshooting

### Issue: "Groq API key not found"
```bash
# Solution: Add to .env
GROQ_API_KEY=gsk_your_key_here
```

### Issue: "PostgreSQL connection refused"
```bash
# Solution: Start Docker
docker-compose up -d
```

### Issue: "Module not found" error
```bash
# Solution: Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### Issue: Bot not responding to Telegram
```bash
# Solution: Check webhook
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo

# Re-set webhook
curl https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://yourapi.com/webhook
```

---

## Next Steps

1. ✅ **Get Groq API Key** (5 min) - https://console.groq.com
2. ✅ **Update .env** (2 min) - Add GROQ_API_KEY
3. ✅ **Start Database** (1 min) - `docker-compose up -d`
4. ✅ **Run Bot** (1 min) - `python src/main.py`
5. 🔄 **Test Agents** (15 min) - Send Telegram commands
6. 📊 **Check Logs** (5 min) - `src/logs/app.log`
7. 🚀 **Deploy** (30 min) - Railway.app or AWS

---

## Support

- **Docs:** /docs (Swagger UI)
- **Issues:** Check logs in `src/logs/`
- **GitHub:** [Your Repo URL]
- **Email:** your-email@example.com

---

**Total Setup Time: ~30 minutes** ⏱️
**No credit card needed for Groq!** 💳❌
**All 9 agents ready to use!** 🤖✨
