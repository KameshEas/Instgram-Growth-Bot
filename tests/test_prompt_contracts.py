"""Contract tests: each prompt must ask for the keys its consumer reads."""
import json
import os

import pytest

os.environ.setdefault("GROQ_API_KEY", "test-key")
from src.main import InstagramGrowthBot  # noqa: E402


def _shape(prompt: str) -> dict:
    """Return the last JSON object the prompt shows after 'this shape:' or 'nothing else:'."""
    for marker in ("in exactly this shape:", "nothing else:"):
        idx = prompt.rfind(marker)
        if idx != -1:
            break
    start = prompt.index("{", idx)
    depth, in_str, esc = 0, False, False
    for j in range(start, len(prompt)):
        c = prompt[j]
        if esc:
            esc = False
        elif c == "\\":
            esc = True
        elif c == '"':
            in_str = not in_str
        elif not in_str:
            depth += {"{": 1, "}": -1}.get(c, 0)
            if depth == 0:
                return json.loads(prompt[start:j + 1])
    raise AssertionError("no JSON shape found in prompt")


@pytest.fixture
def bot_and_capture():
    bot = InstagramGrowthBot.__new__(InstagramGrowthBot)  # skip __init__: no client, no DB
    bot.model = "test-model"
    captured = {}

    def fake_call(**kwargs):
        captured.update(kwargs)
        return {}

    bot._call_groq_with_fallback = fake_call
    return bot, captured


CASES = [
    ("generate_content", dict(topic="home workouts", style="motivational"),
     {"captions": ["caption", "virality_score"], "hashtags": [], "virality_score": []}),
    ("analyze_trends", dict(niche="fitness"),
     {"trending_topics": ["topic", "viral_potential"]}),
    ("engagement_strategy", dict(account_size="micro"),
     {"engagement_targets": ["daily_follows", "daily_likes", "daily_comments"],
      "comment_templates": [], "timing_recommendations": ["peak_hours", "best_days"]}),
    ("monetization_ideas", dict(niche="fitness", follower_count=12000),
     {"monetization_strategies": ["name", "description", "realistic_revenue_projection"]}),
    ("generate_analytics_report", dict(report_type="weekly"),
     {"metrics": [], "insights": [], "note": [], "period": []}),
    ("caption_generator", dict(post_description="new gym opening"),
     {"caption": [], "cta": [], "hashtags": [], "estimated_reach": []}),
    ("hashtag_pack", dict(topic="street food"), {"broad": [], "niche": [], "micro": [], "tip": []}),
    ("bio_optimizer", dict(current_bio="baker | Chennai"),
     {"rewritten_bio": [], "hook": [], "value_prop": [], "cta": [], "keywords": []}),
    ("content_calendar", dict(), {"week_theme": [], "posts": ["day", "format", "topic", "caption_angle", "best_time"], "pro_tip": []}),
    ("posting_schedule", dict(), {"best_times": ["time", "day_type", "reason"], "weekly_schedule": [], "frequency": [], "timezone_note": [], "pro_tip": []}),
    ("story_ideas", dict(topic="meal prep"), {"stories": ["type", "title", "prompt", "engagement_tip"], "hook_tip": []}),
    ("profile_audit", dict(), {"score": [], "checklist": ["area", "status", "finding", "action"], "quick_wins": [], "note": []}),
    ("classify_intent", dict(user_message="captions for my yoga class", available_commands=["/content", "/help"]),
     {"command": [], "confidence": [], "extracted_params": [], "fallback_to_chat": []}),
    ("suggest_content_category", dict(user_context="LinkedIn headshot", available_categories=["women_professional"]),
     {"recommended": [], "reasoning": [], "suggested_category": []}),
]


@pytest.mark.parametrize("method,kwargs,required", CASES, ids=[c[0] for c in CASES])
def test_prompt_requests_keys_consumer_reads(bot_and_capture, method, kwargs, required):
    bot, captured = bot_and_capture
    getattr(bot, method)(**kwargs)
    shape = _shape(captured["prompt"])
    for key, subkeys in required.items():
        assert key in shape, f"{method}: prompt does not ask for '{key}'"
        if subkeys:
            item = shape[key][0] if isinstance(shape[key], list) else shape[key]
            for sub in subkeys:
                assert sub in item, f"{method}: prompt does not ask for '{key}.{sub}'"
