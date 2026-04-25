# 🔧 Developer Guide - Extending the Instagram Growth Bot

This guide shows you how to add new features to the Instagram Growth Bot.

## Table of Contents

1. [Adding New AI Agents](#adding-new-ai-agents)
2. [Integrating New Services](#integrating-new-services)
3. [Custom Metrics](#custom-metrics)
4. [Database Integration](#database-integration)
5. [Testing Guidelines](#testing-guidelines)
6. [Common Patterns](#common-patterns)

---

## Adding New AI Agents

### Example: Email Marketing Agent

#### Step 1: Define the Agent Method

Add to `src/main.py` in the `InstagramGrowthBot` class:

```python
def email_marketing_strategy(self, niche: str, subscriber_count: int) -> dict:
    """Generate email marketing strategy"""
    prompt = f"""Create an email marketing strategy for a {niche} brand with {subscriber_count} subscribers.
    
Include:
- Email sequence templates
- Subject lines for high open rates
- Call-to-action strategies
- Segmentation recommendations
- A/B testing ideas

Format as JSON."""
    
    start_time = time.time()
    try:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        
        duration = time.time() - start_time
        if METRICS_ENABLED:
            metrics.record_api_call(
                model=self.model,
                duration=duration,
                success=True,
                prompt_length=len(prompt)
            )
        
        result = parse_json_response(response.choices[0].message.content)
        if result:
            logger.info(f"✅ Generated email strategy for {niche}")
            if METRICS_ENABLED:
                health_check.record_success()
        return result or {"error": "Failed to generate strategy"}
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Email strategy error: {e}")
        if METRICS_ENABLED:
            metrics.record_api_call(model=self.model, duration=duration, success=False)
            metrics.record_error("EmailStrategyError", str(e), "EmailMarketingAgent")
            health_check.record_error()
        return {"error": "Failed to generate strategy"}
```

#### Step 2: Add to Main Demo

```python
def main():
    # ... existing code ...
    
    print("\n" + "="*60)
    print("📧 DEMO: Email Marketing")
    print("="*60)
    email = bot.email_marketing_strategy(niche="fitness", subscriber_count=10000)
    print(json.dumps(email, indent=2))
```

#### Step 3: Test It

```bash
python src/main.py
# Check output and logs/bot.log for "Email strategy" messages
```

---

## Integrating New Services

### Example: Add Slack Notifications

#### Step 1: Create Notification Module

Create `src/notifications.py`:

```python
import os
import logging
import requests
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SlackNotifier:
    """Send notifications to Slack"""
    
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
        self.enabled = bool(self.webhook_url)
    
    def send_message(self, title: str, message: str, severity: str = "info"):
        """Send Slack message"""
        if not self.enabled:
            return
        
        colors = {
            "success": "#36a64f",
            "warning": "#ff9900",
            "error": "#ff0000",
            "info": "#0099ff"
        }
        
        payload = {
            "attachments": [{
                "color": colors.get(severity, "#0099ff"),
                "title": title,
                "text": message,
                "footer": "Instagram Growth Bot"
            }]
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            logger.debug(f"✅ Slack notification sent: {title}")
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {e}")

# Create global instance
slack = SlackNotifier()
```

#### Step 2: Use in Main Bot

Add to `src/main.py`:

```python
from src.notifications import slack

def main():
    try:
        bot = InstagramGrowthBot()
        slack.send_message("Bot Started", "Instagram Growth Bot started successfully", "success")
        
        # ... rest of code ...
        
        slack.send_message("Bot Completed", "All demos completed successfully", "success")
    except Exception as e:
        slack.send_message("Bot Error", f"Error: {str(e)}", "error")
        raise
```

#### Step 3: Configure

Add to `.env`:
```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

---

## Custom Metrics

### Example: Track Content Quality

Add to `src/metrics.py`:

```python
def record_content_quality(self, virality_score: float, engagement_potential: float):
    """Track content quality metrics"""
    metric = {
        "timestamp": datetime.now().isoformat(),
        "type": "content_quality",
        "virality_score": virality_score,
        "engagement_potential": engagement_potential,
        "quality_grade": "A" if virality_score >= 80 else "B" if virality_score >= 60 else "C"
    }
    
    self.current_session["metrics"].append(metric)
    logger.info(f"📊 Content quality: Virality {virality_score}, Engagement {engagement_potential}")
```

Use it:
```python
# In generate_content method
if METRICS_ENABLED:
    metrics.record_content_quality(
        virality_score=result.get('virality_score', 0),
        engagement_potential=result.get('engagement_score', 0)
    )
```

---

## Database Integration

### Example: PostgreSQL Storage

#### Step 1: Add Database Module

Create `src/database.py`:

```python
import os
import logging
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

logger = logging.getLogger(__name__)

Base = declarative_base()

class GeneratedContent(Base):
    """Store generated content"""
    __tablename__ = "generated_content"
    
    id = Column(Integer, primary_key=True)
    topic = Column(String(255))
    virality_score = Column(Float)
    content = Column(String(5000))
    created_at = Column(DateTime, default=datetime.now)

class BotSession(Base):
    """Store bot execution sessions"""
    __tablename__ = "bot_sessions"
    
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    total_duration = Column(Float)
    api_calls = Column(Integer)
    success_rate = Column(Float)
    created_at = Column(DateTime, default=datetime.now)

class DatabaseManager:
    def __init__(self):
        db_url = os.getenv("DATABASE_URL", "sqlite:///bot.db")
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def save_content(self, topic: str, virality_score: float, content: dict):
        session = self.Session()
        try:
            db_content = GeneratedContent(
                topic=topic,
                virality_score=virality_score,
                content=str(content)
            )
            session.add(db_content)
            session.commit()
            logger.info(f"✅ Content saved to database: {topic}")
        except Exception as e:
            logger.error(f"Database error: {e}")
            session.rollback()
        finally:
            session.close()

db = DatabaseManager()
```

#### Step 2: Use in Bot

```python
from src.database import db

def generate_content(self, topic: str, style: str = "engaging") -> dict:
    # ... existing code ...
    
    result = parse_json_response(response.choices[0].message.content)
    if result and result.get('captions'):
        db.save_content(
            topic=topic,
            virality_score=result.get('virality_score', 0),
            content=result
        )
    return result
```

#### Step 3: Configure

```bash
# Local SQLite (default)
# No configuration needed

# PostgreSQL Production
DATABASE_URL=postgresql://user:password@localhost:5432/insta_bot
```

---

## Testing Guidelines

### Unit Test Template

Create `tests/test_bot.py`:

```python
import unittest
from src.main import InstagramGrowthBot, parse_json_response

class TestInstagramBot(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.bot = InstagramGrowthBot()
    
    def test_json_parsing(self):
        """Test JSON parsing with markdown"""
        markdown_json = '''```json
{
    "test": "value"
}
```'''
        result = parse_json_response(markdown_json)
        self.assertEqual(result["test"], "value")
    
    def test_json_direct(self):
        """Test direct JSON parsing"""
        json_str = '{"test": "value"}'
        result = parse_json_response(json_str)
        self.assertEqual(result["test"], "value")
    
    def test_generate_content(self):
        """Test content generation"""
        result = self.bot.generate_content(topic="test", style="engaging")
        # Should have either content or error
        self.assertTrue("captions" in result or "error" in result)

if __name__ == "__main__":
    unittest.main()
```

Run tests:
```bash
python -m pytest tests/
# or
python -m unittest tests.test_bot
```

---

## Common Patterns

### Pattern 1: Agent with Validation

```python
def new_agent(self, param: str) -> dict:
    """Agent with parameter validation"""
    # Validate input
    if not param or len(param) < 3:
        logger.warning(f"Invalid parameter: {param}")
        return {"error": "Parameter too short"}
    
    # ... API call and processing ...
```

### Pattern 2: Retry Logic

```python
def call_with_retry(self, func, max_attempts=3):
    """Call function with exponential backoff"""
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts:
                raise
            delay = 2 ** (attempt - 1)
            logger.warning(f"Attempt {attempt} failed, retrying in {delay}s...")
            time.sleep(delay)
```

### Pattern 3: Caching Results

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(self, param: str) -> dict:
    """Cache results of expensive operations"""
    # This function result is cached for identical params
    return self.client.chat.completions.create(...)
```

---

## Deployment of Custom Features

### Step 1: Commit and Push

```bash
git add src/
git commit -m "Add new feature: Email marketing agent"
git push origin main
```

### Step 2: Update Environment Variables (if needed)

Add to `.env` or platform-specific config:
```env
NEW_FEATURE_ENABLED=true
NEW_FEATURE_API_KEY=key_value
```

### Step 3: Deploy

**Railway:**
```bash
# Push to main branch, Railway auto-deploys
git push
```

**Docker:**
```bash
docker build -t insta-growth-bot:2.0 .
docker run -e GROQ_API_KEY=... insta-growth-bot:2.0
```

**Local:**
```bash
python src/main.py
```

---

## Resources

- [Groq API Docs](https://console.groq.com/docs)
- [Python JSON Module](https://docs.python.org/3/library/json.html)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Requests Library](https://requests.readthedocs.io/)

---

**Happy coding! 🚀**

Last Updated: April 23, 2026
