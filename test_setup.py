#!/usr/bin/env python3
"""
Test script to verify Telegram bot setup
Run this to check if all dependencies are installed
"""

import sys
import os

print("[INFO] Telegram Bot Setup Verification\n")

# Check Python version
print(f"✅ Python version: {sys.version.split()[0]}")

# Check .env file
env_path = ".env"
if os.path.exists(env_path):
    print(f"✅ .env file exists")
    with open(env_path) as f:
        content = f.read()
        if "TELEGRAM_BOT_TOKEN" in content:
            print("✅ TELEGRAM_BOT_TOKEN found in .env")
        else:
            print("❌ TELEGRAM_BOT_TOKEN not found in .env")
        if "GROQ_API_KEY" in content:
            print("✅ GROQ_API_KEY found in .env")
        else:
            print("❌ GROQ_API_KEY not found in .env")
else:
    print(f"❌ .env file not found")

print("\n[INFO] Checking dependencies...\n")

# Check groq
try:
    import groq
    print(f"✅ groq {groq.__version__} installed")
except ImportError as e:
    print(f"❌ groq not installed: {e}")

# Check telegram
try:
    import telegram
    print(f"✅ python-telegram-bot installed")
except ImportError as e:
    print(f"❌ python-telegram-bot not installed: {e}")
    print("   Install with: pip install python-telegram-bot==20.3")

# Check requests
try:
    import requests
    print(f"✅ requests installed")
except ImportError as e:
    print(f"❌ requests not installed: {e}")

# Check dotenv
try:
    import dotenv
    print(f"✅ python-dotenv installed")
except ImportError as e:
    print(f"❌ python-dotenv not installed: {e}")

print("\n[INFO] Verifying InstagramGrowthBot...\n")

try:
    from src.main import InstagramGrowthBot
    print("✅ InstagramGrowthBot can be imported")
    
    # Try to initialize (requires GROQ_API_KEY)
    try:
        bot = InstagramGrowthBot()
        print("✅ InstagramGrowthBot initialized successfully")
        print(f"   Model: {bot.model}")
    except Exception as e:
        print(f"❌ InstagramGrowthBot initialization failed: {e}")
except ImportError as e:
    print(f"❌ Cannot import InstagramGrowthBot: {e}")

print("\n" + "="*60)
print("Setup Verification Complete!")
print("="*60)
print("\nTo start the Telegram bot, run:")
print("  python src/telegram_bot.py")
print("\nThen send commands to your bot on Telegram:")
print("  /start")
print("  /help")
print("  /content fitness transformation motivational")
