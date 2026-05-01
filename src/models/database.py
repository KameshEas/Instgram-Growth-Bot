from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# Tables

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    user_id: int = Field(primary_key=True)
    username: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: Optional[datetime] = None

class InstagramAccount(SQLModel, table=True):
    __tablename__ = "instagram_accounts"
    
    account_id: int = Field(primary_key=True)
    user_id: int
    username: str
    followers_count: int = 0
    niche: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    
    post_id: int = Field(primary_key=True)
    user_id: int
    account_id: int
    content_type: str  # 'feed', 'story', 'reel'
    image_url: Optional[str] = None
    caption: Optional[str] = None
    posted_at: Optional[datetime] = None
    engagement_rate: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AgentLog(SQLModel, table=True):
    __tablename__ = "agent_logs"
    
    log_id: int = Field(primary_key=True)
    agent_name: str
    user_id: Optional[int] = None
    action: str
    status: str
    execution_time_ms: int = 0
    error_details: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class GiftDesign(SQLModel, table=True):
    __tablename__ = "gift_designs"
    
    design_id: int = Field(primary_key=True)
    user_id: int
    product_type: str  # 't_shirt', 'mug', 'hoodie', etc.
    concept_idea: str  # Original user concept
    design_concepts: Optional[str] = None  # JSON string with 3 concepts + prompts
    brand_colors: Optional[str] = None  # JSON string with hex codes
    design_tone: Optional[str] = None  # minimalist, playful, elegant, etc.
    occasion: Optional[str] = None  # birthday, anniversary, corporate, etc.
    recipient_type: Optional[str] = None  # friend, family, coworker, etc.
    design_hash: Optional[str] = None  # SHA-256 hash for caching
    cached_result: Optional[str] = None  # Cached JSON response from Groq
    cache_ttl_hours: int = 24  # Cache time-to-live
    cache_created_at: Optional[datetime] = None  # When cache was created
    rating: Optional[int] = None  # User rating (1-5)
    notes: Optional[str] = None  # User notes/feedback
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
