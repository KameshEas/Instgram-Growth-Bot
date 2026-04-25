from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from src.config import settings
from src.logger import setup_logger

logger = setup_logger("bot_app")

# Create FastAPI app
app = FastAPI(
    title="Telegram Instagram Bot",
    description="AI-powered Telegram bot for Instagram growth",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize app on startup"""
    logger.info("🚀 Bot starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug: {settings.DEBUG}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Bot shutting down...")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }

@app.post("/webhook")
async def telegram_webhook(update: dict):
    """Telegram webhook endpoint"""
    logger.info(f"Received update: {update.get('update_id')}")
    return {"ok": True}
