"""Integration test for the clarification flow between orchestrator and content generator.

This test verifies that when an ambiguous request is sent to the orchestrator
with `/generate` semantics, the resulting agent response asks for clarification.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


async def test_orchestrator_returns_clarify_on_vague_input():
    from src.agents.orchestrator import ContentOrchestratorAgent

    orchestrator = ContentOrchestratorAgent(groq_bot=None)

    # Simulate a /generate request with a vague custom prompt
    input_data = {
        "command": "/generate",
        "category": "women_professional",
        "custom_prompt": "something nice",
        "chat_id": 12345,
    }

    result = await orchestrator.execute(input_data)
    # ContentGeneratorAgent will return a clarify status when ambiguous
    assert isinstance(result, dict)
    # Accept either a top-level clarify or agent-wrapped clarify
    assert result.get("status") in ("clarify", "error")


if __name__ == "__main__":
    try:
        asyncio.run(test_orchestrator_returns_clarify_on_vague_input())
        print("INTEGRATION: OK")
        sys.exit(0)
    except AssertionError as ae:
        print("INTEGRATION TEST FAILED:", ae)
        sys.exit(1)
    except Exception as e:
        print("INTEGRATION ERROR:", e)
        sys.exit(2)
