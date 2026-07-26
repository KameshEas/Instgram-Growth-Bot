#!/usr/bin/env python3
"""Run Telegram bot with proper environment setup and validation."""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

# Load environment variables from .env file
from dotenv import load_dotenv
env_file = PROJECT_ROOT / ".env"
if env_file.exists():
    load_dotenv(dotenv_path=str(env_file), override=True)
else:
    print("[WARN] .env file not found — using environment variables or defaults")

# Validate required environment variables
REQUIRED_VARS = ["TELEGRAM_BOT_TOKEN", "GROQ_API_KEY"]
missing_vars = [var for var in REQUIRED_VARS if not os.getenv(var)]

if missing_vars:
    print(f"[ERROR] Missing required environment variables: {', '.join(missing_vars)}")
    print(f"[INFO] Set them in .env or as system environment variables")
    sys.exit(1)

print("[OK] Environment variables validated")

# Import and run the bot
try:
    from src.telegram_bot import main_sync
    print("[INFO] Starting Telegram bot...")
    main_sync()
except KeyboardInterrupt:
    print("\n[OK] Bot stopped by user")
    sys.exit(0)
except Exception as e:
    print(f"[ERROR] Bot error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
