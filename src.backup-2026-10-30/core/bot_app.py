from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from src.config import settings
from src.logger import setup_logger
from src.main import InstagramGrowthBot
from src.agents.orchestrator import ContentOrchestratorAgent
from src.api.mobile import set_orchestrator
from src.database.connection import engine
from src.models.database import SQLModel

logger = setup_logger("bot_app")

# Create FastAPI app
app = FastAPI(
    title="Telegram Instagram Bot",
    description="AI-powered Telegram bot for Instagram growth",
    version="1.0.0"
)

from src.api.mobile import router as mobile_router

# Mount mobile API router
app.include_router(mobile_router, prefix="/mobile", tags=["mobile"])

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
    # Initialize the InstagramGrowthBot and orchestrator for mobile API
    try:
        bot = InstagramGrowthBot()
        orchestrator = ContentOrchestratorAgent(groq_bot=bot)
        set_orchestrator(orchestrator)
        app.state.orchestrator = orchestrator
        logger.info("✅ Mobile orchestrator configured with InstagramGrowthBot")
    except Exception as e:
        logger.error(f"Failed to initialize InstagramGrowthBot for mobile API: {e}")
    # Ensure DB tables exist (create if missing)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("✅ Database tables verified/created")
    except Exception as e:
        logger.error(f"Failed to create/verify database tables: {e}")

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
