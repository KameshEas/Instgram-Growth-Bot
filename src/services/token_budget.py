"""Per-user token budget over a sliding one-minute window.

The Groq key is shared by every user and is limited to a fixed number of tokens per minute
(8,000 on the current plan). Without a per-user budget, one user tapping buttons can push
everyone else into 429 rate-limit waits. Disabled unless USER_TOKENS_PER_MIN is set to a
positive number.
"""

import os
import threading
import time
from collections import defaultdict, deque
from typing import Deque, Dict, Optional, Tuple

WINDOW_SECONDS = 60.0


class TokenBudget:
    def __init__(self, tokens_per_minute: Optional[int] = None, clock=time.monotonic):
        if tokens_per_minute is None:
            try:
                tokens_per_minute = int(os.getenv("USER_TOKENS_PER_MIN", "0") or 0)
            except ValueError:
                tokens_per_minute = 0
        self.limit = max(0, tokens_per_minute)
        self._clock = clock
        self._usage: Dict[object, Deque[Tuple[float, int]]] = defaultdict(deque)
        self._lock = threading.Lock()  # gateway calls run in worker threads

    @property
    def enabled(self) -> bool:
        return self.limit > 0

    def _trim(self, key, now: float) -> int:
        window = self._usage[key]
        while window and now - window[0][0] >= WINDOW_SECONDS:
            window.popleft()
        return sum(tokens for _, tokens in window)

    def check(self, key) -> Tuple[bool, int]:
        """Return (allowed, seconds_until_allowed). Unknown/None keys are never limited."""
        if not self.enabled or key is None:
            return True, 0
        with self._lock:
            now = self._clock()
            used = self._trim(key, now)
            if used < self.limit:
                return True, 0
            oldest = self._usage[key][0][0]
            return False, max(1, int(WINDOW_SECONDS - (now - oldest)) + 1)

    def record(self, key, tokens: Optional[int]) -> None:
        if not self.enabled or key is None or not tokens:
            return
        with self._lock:
            self._usage[key].append((self._clock(), int(tokens)))

    def used(self, key) -> int:
        with self._lock:
            return self._trim(key, self._clock())


_budget: Optional[TokenBudget] = None


def get_budget() -> TokenBudget:
    global _budget
    if _budget is None:
        _budget = TokenBudget()
    return _budget


def rate_limited_message(retry_after: int) -> str:
    return (f"You're sending requests faster than the shared AI limit allows. "
            f"Please wait about {retry_after} seconds and try again.")
