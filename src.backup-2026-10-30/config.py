import os
import sys
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional


class Settings(BaseSettings):
    # Telegram (REQUIRED)
    TELEGRAM_BOT_TOKEN: str

    # LLM (Groq) (REQUIRED)
    GROQ_API_KEY: str
    GROQ_MODEL: str = "mixtral-8x7b-32768"
    GROQ_TEMPERATURE: float = 0.7

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # SQLite user profiles (stdlib — no extra deps)
    SQLITE_DB_PATH: str = "data/users.db"

    # Gift Design Settings
    GIFT_DESIGN_CONCEPTS_PER_REQUEST: int = 3
    GIFT_DESIGN_PROMPTS_PER_CONCEPT: int = 2
    GIFT_DESIGN_CACHE_TTL_HOURS: int = 24
    GIFT_DESIGN_TEMPERATURE: float = 0.85

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @field_validator("TELEGRAM_BOT_TOKEN", "GROQ_API_KEY")
    @classmethod
    def validate_required_tokens(cls, v: str, info) -> str:
        """Ensure required API tokens are set."""
        if not v or v.startswith("your_") or v.startswith("gsk-xxx"):
            field_name = info.field_name
            raise ValueError(
                f"{field_name} must be set to a valid value. "
                f"See .env.example and set your credentials in .env"
            )
        return v

    @field_validator("GROQ_TEMPERATURE")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        """Ensure temperature is within valid range."""
        if not 0.0 <= v <= 2.0:
            raise ValueError("GROQ_TEMPERATURE must be between 0.0 and 2.0")
        return v


# Load settings with proper error handling
try:
    settings = Settings()
except Exception as e:
    print(f"\n❌ Configuration Error: {e}\n")
    print("Please check your .env file and ensure all required variables are set correctly.")
    sys.exit(1)
