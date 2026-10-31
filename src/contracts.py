"""Typed response contracts for gateway commands (agentic report C2).

Each model describes the JSON a prompt asks for and the keys its consumer (Telegram handler or
agent) reads. The gateway validates every successful response against its contract and logs
violations; it does not reject responses, because handlers already tolerate missing optional
fields. tests/test_contracts.py checks that the prompts and these models agree.
"""

import logging
from typing import Dict, List, Optional, Type

from pydantic import BaseModel, ConfigDict, Field, ValidationError, conint

logger = logging.getLogger(__name__)


class _Contract(BaseModel):
    model_config = ConfigDict(extra="allow")  # extra keys are fine; missing required keys are not


# ── image / text generation (P01 / P02) ──────────────────────────────────────
class ImageVariation(_Contract):
    title: str
    style: str
    prompt: str = Field(min_length=20)
    negative_prompt: str
    aspect_ratio: str
    keywords: List[str] = []


class TextVariation(_Contract):
    title: str
    type: str
    content: str = Field(min_length=1)
    hook: str = ""
    cta: str = ""
    tone: str = ""
    keywords: List[str] = []


class VariationsResponse(_Contract):
    variations: List[dict] = Field(min_length=1)


# ── command responses read by Telegram handlers ──────────────────────────────
class Caption(_Contract):
    caption: str = Field(min_length=1)
    virality_score: conint(ge=0, le=100)


class ContentResponse(_Contract):                    # P06 -> /content
    captions: List[Caption] = Field(min_length=1)
    hashtags: List[str] = []


class TrendingTopic(_Contract):
    topic: str
    viral_potential: conint(ge=0, le=100)


class TrendsResponse(_Contract):                     # P07 -> /trends
    trending_topics: List[TrendingTopic] = Field(min_length=1)


class EngagementTargets(_Contract):
    daily_follows: conint(ge=0)
    daily_likes: conint(ge=0)
    daily_comments: conint(ge=0)


class TimingRecommendations(_Contract):
    peak_hours: List[str] = []
    best_days: List[str] = []


class EngagementResponse(_Contract):                 # P08 -> /engagement
    engagement_targets: EngagementTargets
    comment_templates: List[str] = []
    timing_recommendations: TimingRecommendations


class MonetizationStrategy(_Contract):
    name: str
    description: str
    realistic_revenue_projection: str


class MonetizationResponse(_Contract):               # P09 -> /monetize
    monetization_strategies: List[MonetizationStrategy] = Field(min_length=1)


class AnalyticsResponse(_Contract):                  # P23 -> /analytics (wrapped by AnalyticsAgent)
    note: str
    period: str
    metrics: Dict[str, float]
    insights: List[str] = []


class CaptionGeneratorResponse(_Contract):           # P10 -> /caption
    caption: str = Field(min_length=1)
    cta: str = ""
    hashtags: List[str] = []
    estimated_reach: str = ""


class HashtagPackResponse(_Contract):                # P11 -> hashtag pack
    broad: List[str]
    niche: List[str]
    micro: List[str]
    tip: str = ""


class BioResponse(_Contract):                        # P12 -> /bio
    rewritten_bio: str = Field(min_length=1)
    keywords: List[str] = []


class CalendarPost(_Contract):
    day: str
    format: str
    topic: str


class CalendarResponse(_Contract):                   # P13 -> /ideas
    week_theme: str
    posts: List[CalendarPost] = Field(min_length=7, max_length=7)


class IntentResponse(_Contract):                     # P27 -> orchestrator
    command: str
    confidence: float = Field(ge=0, le=1)
    extracted_params: dict = {}
    fallback_to_chat: bool


class CategoryPickResponse(_Contract):               # P25 -> content generator
    suggested_category: str
    recommended: List[str] = []


CONTRACTS: Dict[str, Type[BaseModel]] = {
    "generate_universal_prompts": VariationsResponse,
    "generate_universal_prompts_retry": VariationsResponse,
    "generate_content": ContentResponse,
    "analyze_trends": TrendsResponse,
    "engagement_strategy": EngagementResponse,
    "monetization_ideas": MonetizationResponse,
    "generate_analytics_report": AnalyticsResponse,
    "caption_generator": CaptionGeneratorResponse,
    "hashtag_pack": HashtagPackResponse,
    "bio_optimizer": BioResponse,
    "content_calendar": CalendarResponse,
    "classify_intent": IntentResponse,
    "suggest_content_category": CategoryPickResponse,
}


def contract_errors(command: str, payload: dict) -> Optional[List[str]]:
    """Return a list of violations for this command's contract, [] if valid, None if no contract."""
    model = CONTRACTS.get(command)
    if model is None:
        return None
    try:
        model.model_validate(payload)
    except ValidationError as e:
        return [f"{'.'.join(str(p) for p in err['loc'])}: {err['msg']}" for err in e.errors()][:10]
    return []


def variation_errors(variations: list, is_text: bool) -> List[str]:
    model = TextVariation if is_text else ImageVariation
    problems = []
    for i, var in enumerate(variations or [], 1):
        try:
            model.model_validate(var)
        except ValidationError as e:
            problems += [f"variations.{i}.{'.'.join(str(p) for p in err['loc'])}: {err['msg']}" for err in e.errors()]
    return problems[:10]
