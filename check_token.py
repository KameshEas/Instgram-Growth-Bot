#!/usr/bin/env python3
from dotenv import load_dotenv
import os
from pathlib import Path

# Check multiple possible .env locations
print("Checking .env files:")
print(f"Current dir: {os.getcwd()}")
print(f"Script dir: {Path(__file__).parent}")
print()

# Try loading from explicit path
env_path = Path(__file__).parent / ".env"
print(f"Loading from: {env_path}")
print(f"File exists: {env_path.exists()}")

if env_path.exists():
    with open(env_path) as f:
        print(f"File contents (first 5 lines):")
        for i, line in enumerate(f):
            if i < 5:
                if "TOKEN" in line:
                    print(f"  {line.strip()}")
            else:
                break

load_dotenv(dotenv_path=str(env_path))
token = os.getenv("TELEGRAM_BOT_TOKEN")
print()
print(f"Bot Token loaded: {token}")
print(f"Token is valid: {len(token) if token else 0 > 0}")
