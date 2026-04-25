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
