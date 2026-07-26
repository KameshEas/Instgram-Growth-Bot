"""Groq API retry handler with exponential backoff and circuit breaker.

Prevents single API failures from crashing the entire bot. Implements:
- Exponential backoff for transient failures
- Circuit breaker pattern to prevent cascading failures
- Fallback to formula-based prompts when API unavailable
"""

import time
import logging
from typing import Callable, Any, Optional, Dict
from enum import Enum
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker state machine."""
    CLOSED = "closed"  # Normal operation, requests proceed
    OPEN = "open"  # Too many failures, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


class GroqRetryConfig:
    """Configuration for retry behavior."""

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 30.0,
        exponential_base: float = 2.0,
        circuit_failure_threshold: int = 5,
        circuit_recovery_timeout: int = 60,
    ):
        """Initialize retry configuration.

        Args:
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            exponential_base: Multiplier for exponential backoff
            circuit_failure_threshold: Failures before circuit opens
            circuit_recovery_timeout: Seconds before trying to recover circuit
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.circuit_failure_threshold = circuit_failure_threshold
        self.circuit_recovery_timeout = circuit_recovery_timeout


class GroqRetryHandler:
    """Handle Groq API failures with intelligent retry and fallback."""

    def __init__(self, config: Optional[GroqRetryConfig] = None):
        """Initialize retry handler.

        Args:
            config: Retry configuration (uses defaults if None)
        """
        self.config = config or GroqRetryConfig()
        self.circuit_state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.last_recovery_attempt: Optional[datetime] = None

    def _should_attempt_recovery(self) -> bool:
        """Check if circuit should try recovery."""
        if self.circuit_state != CircuitState.OPEN:
            return False

        if not self.last_failure_time:
            return True

        timeout_expired = datetime.now() >= (
            self.last_failure_time
            + timedelta(seconds=self.config.circuit_recovery_timeout)
        )
        return timeout_expired

    def _update_circuit_state(self, success: bool):
        """Update circuit breaker state based on result."""
        if success:
            if self.circuit_state == CircuitState.HALF_OPEN:
                self.circuit_state = CircuitState.CLOSED
                self.failure_count = 0
                logger.info("[CIRCUIT] Circuit recovered, resuming normal operation")
        else:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.config.circuit_failure_threshold:
                self.circuit_state = CircuitState.OPEN
                logger.error(
                    f"[CIRCUIT] Circuit opened after {self.failure_count} failures"
                )
            elif self.circuit_state == CircuitState.HALF_OPEN:
                # Recovery attempt failed, stay open
                logger.warning("[CIRCUIT] Recovery attempt failed, circuit remains open")

    def call_with_retry(
        self,
        func: Callable,
        *args,
        **kwargs,
    ) -> tuple[Any, bool]:
        """Call a Groq API function with retry logic.

        Args:
            func: Function to call (typically Groq API method)
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Tuple of (result, success). If success=False, result is error dict.
        """
        # Check circuit state
        if self.circuit_state == CircuitState.OPEN:
            if self._should_attempt_recovery():
                logger.info("[CIRCUIT] Attempting recovery in half-open state")
                self.circuit_state = CircuitState.HALF_OPEN
            else:
                return {
                    "status": "error",
                    "error": "API circuit breaker open. Service temporarily unavailable.",
                    "recovery_seconds": self.config.circuit_recovery_timeout,
                }, False

        # Attempt with retries
        for attempt in range(self.config.max_retries + 1):
            try:
                result = func(*args, **kwargs)
                self._update_circuit_state(success=True)
                return result, True

            except Exception as e:
                is_last_attempt = attempt >= self.config.max_retries
                error_msg = str(e)

                # Determine if error is retryable
                is_retryable = self._is_retryable_error(e)

                logger.warning(
                    f"[RETRY] Attempt {attempt + 1}/{self.config.max_retries + 1} "
                    f"failed: {error_msg} (retryable={is_retryable})"
                )

                if is_last_attempt or not is_retryable:
                    self._update_circuit_state(success=False)
                    return {
                        "status": "error",
                        "error": error_msg,
                        "attempts": attempt + 1,
                    }, False

                # Calculate backoff delay
                delay = self._calculate_backoff(attempt)
                logger.info(f"[RETRY] Waiting {delay:.1f}s before retry...")
                time.sleep(delay)

        # Should not reach here
        return {
            "status": "error",
            "error": "Max retries exceeded",
        }, False

    def _is_retryable_error(self, error: Exception) -> bool:
        """Check if an error is retryable (vs. permanent failure)."""
        error_msg = str(error).lower()

        # Retryable: timeout, rate limit, server error
        retryable_keywords = [
            "timeout",
            "rate limit",
            "429",
            "503",
            "502",
            "504",
            "temporarily unavailable",
            "connection reset",
            "connection refused",
        ]

        if any(keyword in error_msg for keyword in retryable_keywords):
            return True

        # Not retryable: auth error, malformed request
        non_retryable_keywords = [
            "auth",
            "invalid",
            "malformed",
            "400",
            "401",
            "403",
            "404",
        ]

        if any(keyword in error_msg for keyword in non_retryable_keywords):
            return False

        # Default: assume retryable for unknown errors
        return True

    def _calculate_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff delay with jitter."""
        delay = self.config.initial_delay * (
            self.config.exponential_base ** attempt
        )
        delay = min(delay, self.config.max_delay)

        # Add small jitter (±10%) to avoid thundering herd
        import random
        jitter = delay * random.uniform(-0.1, 0.1)
        return max(0, delay + jitter)

    def get_circuit_status(self) -> Dict[str, Any]:
        """Get current circuit breaker status."""
        return {
            "state": self.circuit_state.value,
            "failure_count": self.failure_count,
            "last_failure": self.last_failure_time.isoformat()
            if self.last_failure_time
            else None,
            "circuit_open": self.circuit_state == CircuitState.OPEN,
        }


# Global retry handler instance
_retry_handler: Optional[GroqRetryHandler] = None


def get_retry_handler() -> GroqRetryHandler:
    """Get or create global retry handler."""
    global _retry_handler
    if _retry_handler is None:
        _retry_handler = GroqRetryHandler()
    return _retry_handler


def reset_retry_handler():
    """Reset retry handler state (for testing)."""
    global _retry_handler
    _retry_handler = None
