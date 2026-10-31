"""Request context for tracing: one request ID (and chat ID) per user request.

The ID is stored in contextvars, so it follows the request through `await` calls and into
`asyncio.to_thread` workers (which copy the current context). The LLM gateway writes it to every
prompt-log row, which links a Telegram update -> orchestrator -> agent -> each Groq call.
"""

import contextvars
import uuid
from typing import Optional

_request_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("request_id", default=None)
_chat_id: contextvars.ContextVar[Optional[int]] = contextvars.ContextVar("chat_id", default=None)


def start_request(chat_id: Optional[int] = None, request_id: Optional[str] = None) -> str:
    """Begin a traced request in the current context and return its ID."""
    rid = request_id or uuid.uuid4().hex[:12]
    _request_id.set(rid)
    _chat_id.set(chat_id)
    return rid


def ensure_request(chat_id: Optional[int] = None) -> str:
    """Return the current request ID, starting one if none is active."""
    rid = _request_id.get()
    if rid is None:
        return start_request(chat_id)
    if chat_id is not None and _chat_id.get() is None:
        _chat_id.set(chat_id)
    return rid


def current_request_id() -> Optional[str]:
    return _request_id.get()


def current_chat_id() -> Optional[int]:
    return _chat_id.get()
