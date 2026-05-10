#!/usr/bin/env python3
"""Create database tables (one-time)

Usage:
    python scripts/create_tables.py

This will run SQLModel.metadata.create_all using the async engine in
`src.database.connection` so it works with the project's async DB URL.
"""
import asyncio
import sys
from src.database.connection import engine
from src.models.database import SQLModel
from src.logger import setup_logger

logger = setup_logger("create_tables")


async def run():
    logger.info("Starting DB table creation...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("✅ Tables created or already exist.")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except Exception:
        sys.exit(1)
