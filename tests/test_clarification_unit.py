"""Unit tests for clarification helpers in EdgeCaseHandler"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


async def test_is_ambiguous_and_question():
    from src.services.edge_case_handler import EdgeCaseHandlerFactory

    handler = EdgeCaseHandlerFactory.get_handler()

    vague_input = {"design_prompt": "something nice and cool"}
    is_amb = await handler.is_ambiguous(vague_input)
    assert is_amb is True

    question = await handler.get_clarifying_question(vague_input)
    assert isinstance(question, str) and len(question) > 5


async def test_not_ambiguous():
    from src.services.edge_case_handler import EdgeCaseHandlerFactory

    handler = EdgeCaseHandlerFactory.get_handler()
    good_input = {"design_prompt": "A professional product photo, white background, soft lighting"}
    is_amb = await handler.is_ambiguous(good_input)
    assert is_amb is False


if __name__ == "__main__":
    ok = True
    try:
        asyncio.run(test_is_ambiguous_and_question())
        asyncio.run(test_not_ambiguous())
    except Exception as e:
        print("TEST FAILED:", e)
        ok = False
    sys.exit(0 if ok else 1)
