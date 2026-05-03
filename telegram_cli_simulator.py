#!/usr/bin/env python3
"""Local CLI simulator for Telegram interactions.

Run this to experience the /generate flow (including the one-question
clarification) without creating a Telegram bot or using networked webhooks.

Usage:
  py -3 telegram_cli_simulator.py

Commands supported:
  /generate [category] ["custom prompt"]  - generate prompts for a category
  any free text                            - routed through intent classification
  exit                                     - quit
"""

import asyncio
import json
import sys
import io
from pathlib import Path

# Ensure stdout/stderr use UTF-8 to avoid Windows console encoding errors
try:
    if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    # Fallback: wrap stdout/stderr
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.main import InstagramGrowthBot
from src.agents.orchestrator import ContentOrchestratorAgent


async def main():
    print("Starting local Telegram CLI simulator...")
    bot = InstagramGrowthBot()
    orchestrator = ContentOrchestratorAgent(groq_bot=bot)

    print("Type 'exit' to quit. Examples:")
    print("  /generate women_professional")
    print("  /generate design_posters \"something nice\"")

    while True:
        try:
            cmd = input("cmd> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting")
            return

        if not cmd:
            continue
        if cmd.lower() in ("exit", "quit"):
            print("Goodbye")
            return

        # Basic /generate parsing
        if cmd.startswith("/generate") or cmd.startswith("generate"):
            text_after = cmd.replace("/generate", "", 1).strip()
            if not text_after:
                print("Usage: /generate [category] [\"custom prompt\"]")
                continue

            category = text_after.split()[0]
            remaining = text_after[len(category):].strip()
            custom_prompt = None
            if remaining:
                custom_prompt = remaining.strip().strip('"').strip("'")

            input_data = {
                "command": "/generate",
                "category": category,
                "custom_prompt": custom_prompt,
                "user_input": custom_prompt,
                "chat_id": 123456,
            }

            result = await orchestrator.execute(input_data)

            # Handle clarification request
            if isinstance(result, dict) and result.get("status") == "clarify":
                question = result.get("question", "Could you clarify?")
                fields = result.get("clarify_fields", [])
                if fields:
                    print(f"Bot: {question}")
                    print("Please reply with key:value pairs separated by semicolons, e.g. subject: woman; colors: white; mood: editorial")
                    answer = input("You> ")
                    # Try to parse key:value pairs
                    parsed = {}
                    try:
                        parts = [p.strip() for p in answer.split(";") if p.strip()]
                        for part in parts:
                            if ":" in part:
                                k, v = part.split(":", 1)
                                parsed[k.strip()] = v.strip()
                    except Exception:
                        parsed = {}
                    # If parsing yielded nothing, store raw text under 'text'
                    if not parsed:
                        input_data["clarification_answer"] = {"text": answer}
                    else:
                        input_data["clarification_answer"] = parsed
                else:
                    question = result.get("question", "Could you clarify?")
                    answer = input(f"Bot: {question}\nYou> ")
                    input_data["clarification_answer"] = answer
                input_data["clarified"] = True
                result = await orchestrator.execute(input_data)

            print(json.dumps(result, indent=2, ensure_ascii=False))
            continue

        # Fallback: free-text routed through orchestrator (intent classification)
        input_data = {"text": cmd, "chat_id": 123456}
        result = await orchestrator.execute(input_data)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
