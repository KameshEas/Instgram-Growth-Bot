# 🚀 Quick Reference: 9 AI Agents

## Agent Commands Cheat Sheet

```
┌──────────────────────────────────────────────────────────────┐
│         TELEGRAM BOT COMMAND REFERENCE                       │
└──────────────────────────────────────────────────────────────┘

/help                      Show all commands & agents

CONTENT GENERATION (ContentGeneratorAgent)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/generate                  Generate content with prompts
  ├─ category: women_professional, women_transform, etc.
  ├─ style: professional, creative, casual
  └─ request: custom description
  
/create                    Alias for /generate
/content                   Alias for /generate

INSTAGRAM (InstagramIntegrationAgent)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/post                      Post to Instagram
  ├─ action: "post"
  ├─ caption: post text
  └─ image_url: image link
  
/schedule                  Schedule post for later
  ├─ action: "schedule"
  ├─ caption: post text
  └─ scheduled_time: 2024-01-15T14:00:00Z
  
/cross_post                Post to TikTok & YouTube Shorts
  └─ content: your content

ENGAGEMENT (EngagementAgent)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/engage                    Smart engagement (follows, likes, comments)
  ├─ action: "engage"
  ├─ hashtag: target hashtag
  └─ max_actions: max 20
  
/follow                    Follow accounts in niche
  ├─ action: "follow_niche"
  ├─ niche: photography
  └─ count: 5-10 max
  
/comment                   Post intelligent comments
  └─ action: "comment_strategy"
  
/dm                        Send DMs to new followers
  ├─ action: "dm_sequence"
  ├─ follower_ids: [...users...]
  └─ message: custom message

MONETIZATION (MonetizationAgent)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/revenue                   Track all revenue
  └─ action: "track_revenue"
  
/affiliate                 Add affiliate link
  ├─ platform: amazon, flipkart, etc.
  ├─ product: product name
  └─ commission_rate: 0.05
  
/sponsored                 Track sponsored deal
  ├─ brand: brand name
  ├─ deal_amount: price
  └─ post_count: number of posts
  
/monetize                  Full monetization dashboard
  └─ action: "dashboard"

ANALYTICS (AnalyticsAgent)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/analytics                 Daily report
  └─ report_type: daily
  
/report                    Weekly or monthly report
  └─ report_type: weekly | monthly
  
/stats                     Get statistics
  └─ Alias for /analytics

TRENDS (TrendsAgent)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/trends                    Detect trending topics
  ├─ action: "detect"
  └─ platforms: twitter, tiktok, reddit
  
/viral                     Get viral forecast for content
  ├─ action: "viral_forecast"
  └─ content_idea: your idea
  
/hashtags                  Get trending hashtags
  ├─ niche: photography
  └─ count: 30

PRIVACY & SECURITY (PrivacyAgent)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/security                  Security audit
  └─ action: "audit"
  
/privacy                   Compliance check
  └─ action: "compliance_check"
  
/backup                    Backup data
  └─ action: "backup"

SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/health                    Server health check (HTTP)
curl http://localhost:8000/health

/docs                      API documentation (Swagger)
http://localhost:8000/docs
```

---

## Agent Details Table

| Agent | File | Type | Status | Commands |
|-------|------|------|--------|----------|
| ContentGenerator | content_generator.py | 📝 Content | ✅ Ready | /generate, /create |
| Instagram | instagram_agent.py | 📸 Social | ⏳ Beta | /post, /schedule |
| Engagement | engagement_agent.py | 🚀 Growth | ✅ Ready | /engage, /follow |
| Monetization | monetization_agent.py | 💰 Revenue | ✅ Ready | /revenue, /affiliate |
| Analytics | analytics_agent.py | 📊 Reports | ✅ Ready | /analytics, /report |
| Trends | trends_agent.py | 📈 Trends | ✅ Ready | /trends, /viral |
| Privacy | privacy_agent.py | 🔐 Security | ✅ Ready | /security, /privacy |
| TelegramHandler | telegram_handler.py | 📱 Parser | ✅ Ready | (auto) |
| Orchestrator | orchestrator.py | 🎯 Router | ✅ Ready | /help |

---

## Common Tasks

### Task 1: Generate Content for Tomorrow
```
/generate category=women_professional style=professional request=fashion
```

### Task 2: Check Today's Growth
```
/analytics report_type=daily
```

### Task 3: Find What's Trending
```
/trends action=detect platforms=twitter,tiktok,reddit
```

### Task 4: Track Revenue
```
/revenue action=track_revenue
```

### Task 5: Smart Engagement
```
/engage action=engage hashtag=photography max_actions=20
```

### Task 6: Schedule Post
```
/schedule action=schedule caption="Beautiful sunset! 🌅" scheduled_time=2024-01-15T14:00:00Z
```

### Task 7: Cross-Post to TikTok
```
/cross_post action=cross_post
```

### Task 8: Security Audit
```
/security action=audit
```

### Task 9: Get Viral Forecast
```
/viral action=viral_forecast content_idea="Photography tips"
```

---

## Sample Python Usage

```python
import asyncio
from src.agents.orchestrator import ContentOrchestratorAgent

async def demo():
    agent = ContentOrchestratorAgent()
    
    # Test 1: Generate content
    result = await agent.execute({
        "command": "/generate",
        "category": "women_professional",
        "style": "professional"
    })
    print("Generated:", result)
    
    # Test 2: Get analytics
    result = await agent.execute({
        "command": "/analytics",
        "report_type": "daily"
    })
    print("Analytics:", result)
    
    # Test 3: Monetization dashboard
    result = await agent.execute({
        "command": "/revenue",
        "action": "dashboard"
    })
    print("Revenue:", result)

asyncio.run(demo())
```

---

## Setup Steps (First Time)

```bash
# 1. Get Groq API Key
# Visit: https://console.groq.com
# Create API key (FREE, no credit card)

# 2. Update .env
echo "GROQ_API_KEY=gsk_your_key_here" >> .env

# 3. Start database
docker-compose up -d

# 4. Activate venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Mac/Linux

# 5. Run bot
python src/main.py

# 6. In another terminal, test
curl http://localhost:8000/health

# 7. Send Telegram commands
# (requires TELEGRAM_BOT_TOKEN in .env)
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Groq API key not found" | Add GROQ_API_KEY to .env |
| "PostgreSQL connection refused" | Run `docker-compose up -d` |
| "Module not found" | Activate venv first |
| "Bot not responding" | Check webhook setup |
| "Port 8000 in use" | Change in src/main.py |

---

## File Structure Quick Look

```
src/agents/
├── base_agent.py              ← All agents inherit from this
├── orchestrator.py            ← Master router
├── telegram_handler.py        ← Parse Telegram commands
├── content_generator.py       ← Generate content
├── instagram_agent.py         ← Post to Instagram
├── engagement_agent.py        ← Grow followers safely
├── monetization_agent.py      ← Track revenue (6 streams)
├── analytics_agent.py         ← Generate reports
├── privacy_agent.py           ← Security & compliance
└── trends_agent.py            ← Detect trends

src/core/
├── bot_app.py                 ← FastAPI app
└── langchain_setup.py         ← LangChain + Groq

src/prompts/
└── templates.py               ← 110+ prompt templates
```

---

## Performance Tips

✅ **Speed Up Generation**: Increase batch size in config
✅ **Reduce Database Load**: Enable Redis caching (commented out)
✅ **Better Engagement**: Use trending hashtags from /trends
✅ **More Revenue**: Track ALL 6 streams with /revenue
✅ **Protect Account**: Use safe engagement limits

---

## Support Resources

- 📚 **Docs**: `IMPLEMENTATION_GUIDE.md`
- 🧪 **Tests**: `tests/test_agents_integration.py`
- 📖 **README**: `README.md`
- 🔍 **API Docs**: http://localhost:8000/docs
- 📝 **Summary**: `IMPLEMENTATION_SUMMARY.md`

---

**Ready to grow? Send /help to start!** 🚀
