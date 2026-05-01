import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Telegram
    TELEGRAM_BOT_TOKEN: str

    # LLM (Groq)
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    GROQ_TEMPERATURE: float = 0.7

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # SQLite user profiles (stdlib — no extra deps)
    SQLITE_DB_PATH: str = "data/users.db"

    # Gift Design Settings
    GIFT_DESIGN_CONCEPTS_PER_REQUEST: int = 3  # Number of design variations to generate
    GIFT_DESIGN_PROMPTS_PER_CONCEPT: int = 2  # Number of image generation prompts per concept
    GIFT_DESIGN_CACHE_TTL_HOURS: int = 24  # Cache time-to-live for gift designs
    GIFT_DESIGN_TEMPERATURE: float = 0.85  # Groq temperature for design generation (higher = more creative)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

# Load settings
settings = Settings()
