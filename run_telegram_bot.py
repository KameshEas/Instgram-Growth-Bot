#!/usr/bin/env python3
"""
Setup and run Telegram bot with proper environment
This script handles all setup steps before running the bot
"""

import subprocess
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent
os.chdir(PROJECT_ROOT)

# Load .env file FIRST to get the token
env_file = PROJECT_ROOT / ".env"
if env_file.exists():
    load_dotenv(dotenv_path=str(env_file))
else:
    print("[WARN] .env file not found at:", env_file)

# Explicitly remove any conflicting environment variable
if "TELEGRAM_BOT_TOKEN" in os.environ:
    # Get the token from .env if available
    env_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if env_token and len(env_token) > 50:
        # This looks like a real token (not from env var cache)
        del os.environ["TELEGRAM_BOT_TOKEN"]
        os.environ["TELEGRAM_BOT_TOKEN"] = env_token

print("="*60)
print("Instagram Growth Bot - Telegram Interface Launcher")
print("="*60)
print()

# Determine if we're in a virtual environment
in_venv = sys.prefix != sys.base_prefix

if not in_venv:
    print("[ERROR] Not running in virtual environment!")
    print("[INFO] Activate venv first:")
    print()
    if os.name == 'nt':  # Windows
        print("  .\\venv\\Scripts\\activate.bat")
    else:  # Linux/Mac
        print("  source venv/bin/activate")
    print()
    sys.exit(1)

print("[OK] Virtual environment activated")
print(f"[INFO] Python: {sys.executable}")
print()

# Check if python-telegram-bot is installed
print("[INFO] Checking dependencies...")
try:
    import telegram
    print("[OK] python-telegram-bot is installed")
except ImportError:
    print("[WARN] python-telegram-bot not found, installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot"])
    print("[OK] python-telegram-bot installed")

# Check other dependencies
deps = ["groq", "dotenv", "requests"]
for dep in deps:
    try:
        __import__(dep)
        print(f"[OK] {dep} is installed")
    except ImportError:
        print(f"[WARN] {dep} not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", {
            "dotenv": "python-dotenv",
            "groq": "groq"
        }.get(dep, dep)])

print()
print("="*60)
print("[OK] All dependencies ready!")
print("="*60)
print()

# Run the telegram bot
print("[INFO] Starting Telegram bot...")
print("[INFO] Press Ctrl+C to stop")
print()

# Import and run
try:
    from src.telegram_bot import main_sync
    
    # Run the synchronous main function
    main_sync()
    
except KeyboardInterrupt:
    print()
    print("[OK] Bot stopped by user")
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
