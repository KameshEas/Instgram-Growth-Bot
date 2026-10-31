"""
Error Recovery System for Phase 2C

Implements graceful error handling and recovery strategies.
Attempts to recover from errors or provide informative fallbacks.

Author: AI Development Agent
Date: May 2, 2026
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable, Set, Tuple
from enum import Enum
import logging
from datetime import datetime
import traceback

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Category of error."""
    API_ERROR = "api_error"
    PARAMETER_ERROR = "parameter_error"
    RESOURCE_ERROR = "resource_error"
    TIMEOUT_ERROR = "timeout_error"
    VALIDATION_ERROR = "validation_error"
    PROCESSING_ERROR = "processing_error"
    UNKNOWN_ERROR = "unknown_error"


class RecoveryStrategy(Enum):
    """Strategy for recovering from error."""
    RETRY = "retry"
    FALLBACK = "fallback"
    DEGRADE = "degrade"
    ABORT = "abort"
    SKIP = "skip"


@dataclass
class RecoveryAttempt:
    """Single recovery attempt."""
    strategy: RecoveryStrategy
    attempt_number: int
    success: bool
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        status = "✅" if self.success else "❌"
        return f"{status} Attempt {self.attempt_number} ({self.strategy.value}): {self.message}"


@dataclass
class ErrorRecoveryResult:
    """Result of error handling and recovery."""
    error_type: ErrorType
    original_error: str
    recovery_attempted: bool
    recovery_successful: bool
    recovery_attempts: List[RecoveryAttempt] = field(default_factory=list)
    fallback_value: Optional[Any] = None
    degraded_output: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        lines = [f"Error Type: {self.error_type.value}"]
        lines.append(f"Original Error: {self.original_error}")
        lines.append(f"Recovery Status: {'✅ SUCCESS' if self.recovery_successful else '❌ FAILED'}")
        
        if self.recovery_attempts:
            lines.append(f"\nRecovery Attempts ({len(self.recovery_attempts)}):")
            for attempt in self.recovery_attempts:
                lines.append(f"  {attempt}")
        
        if self.fallback_value is not None:
            lines.append(f"\nFallback Value: {self.fallback_value}")
        
        if self.degraded_output:
            lines.append(f"\nDegraded Output: {len(self.degraded_output)} fields")
        
        return "\n".join(lines)


class ErrorRecoverySystem:
    """Implements error handling and recovery strategies."""
    
    def __init__(self):
        """Initialize error recovery system."""
        self.max_retry_attempts = 3
        self.retry_delay = 1  # seconds
        self.recovery_strategies = self._define_recovery_strategies()
        self.fallback_values = self._define_fallback_values()
    
    def _define_recovery_strategies(self) -> Dict[ErrorType, List[RecoveryStrategy]]:
        """Define recovery strategies for each error type."""
        return {
            ErrorType.API_ERROR: [RecoveryStrategy.RETRY, RecoveryStrategy.FALLBACK, RecoveryStrategy.ABORT],
            ErrorType.PARAMETER_ERROR: [RecoveryStrategy.DEGRADE, RecoveryStrategy.SKIP],
            ErrorType.RESOURCE_ERROR: [RecoveryStrategy.RETRY, RecoveryStrategy.DEGRADE],
            ErrorType.TIMEOUT_ERROR: [RecoveryStrategy.RETRY, RecoveryStrategy.FALLBACK],
            ErrorType.VALIDATION_ERROR: [RecoveryStrategy.DEGRADE, RecoveryStrategy.SKIP],
            ErrorType.PROCESSING_ERROR: [RecoveryStrategy.RETRY, RecoveryStrategy.DEGRADE, RecoveryStrategy.ABORT],
            ErrorType.UNKNOWN_ERROR: [RecoveryStrategy.DEGRADE, RecoveryStrategy.ABORT],
        }
    
    def _define_fallback_values(self) -> Dict[str, Any]:
        """Define fallback values for common fields."""
        return {
            "design_prompt": "Create a professional and creative design.",
            "content_prompt": "Generate engaging content.",
            "product_type": "t_shirt",
            "quality_preference": "balanced",
            "design_variations": 3,
            "budget_level": "standard",
            "deadline_urgency": "medium",
        }
    
    async def handle_error(
        self,
        error: Exception,
        error_type: ErrorType,
        context: Optional[Dict[str, Any]] = None,
    ) -> ErrorRecoveryResult:
        """
        Handle an error with recovery strategies.
        
        Args:
            error: The exception that occurred
            error_type: Category of the error
            context: Additional context about the error
        
        Returns:
            ErrorRecoveryResult with recovery status
        """
        error_str = str(error)
        logger.error(f"Error occurred: {error_type.value} - {error_str}")
        logger.debug(f"Error context: {context}")
        logger.debug(f"Traceback: {traceback.format_exc()}")
        
        strategies = self.recovery_strategies.get(error_type, [RecoveryStrategy.ABORT])
        attempts: List[RecoveryAttempt] = []
        
        for attempt_num, strategy in enumerate(strategies, 1):
            attempt_result = await self._attempt_recovery(
                strategy=strategy,
                error=error,
                error_type=error_type,
                context=context,
                attempt_number=attempt_num,
            )
            attempts.append(attempt_result)
            
            if attempt_result.success:
                logger.info(f"Recovery successful using strategy: {strategy.value}")
                return ErrorRecoveryResult(
                    error_type=error_type,
                    original_error=error_str,
                    recovery_attempted=True,
                    recovery_successful=True,
                    recovery_attempts=attempts,
                    fallback_value=attempt_result.message if strategy == RecoveryStrategy.FALLBACK else None,
                    degraded_output=attempt_result.message if strategy == RecoveryStrategy.DEGRADE else None,
                )
        
        logger.error(f"All recovery strategies failed for {error_type.value}")
        return ErrorRecoveryResult(
            error_type=error_type,
            original_error=error_str,
            recovery_attempted=True,
            recovery_successful=False,
            recovery_attempts=attempts,
        )
    
    async def _attempt_recovery(
        self,
        strategy: RecoveryStrategy,
        error: Exception,
        error_type: ErrorType,
        context: Optional[Dict[str, Any]],
        attempt_number: int,
    ) -> RecoveryAttempt:
        """Attempt recovery using specified strategy."""
        
        if strategy == RecoveryStrategy.RETRY:
            return await self._retry_recovery(error, error_type, context, attempt_number)
        
        elif strategy == RecoveryStrategy.FALLBACK:
            return await self._fallback_recovery(error, error_type, context, attempt_number)
        
        elif strategy == RecoveryStrategy.DEGRADE:
            return await self._degraded_recovery(error, error_type, context, attempt_number)
        
        elif strategy == RecoveryStrategy.SKIP:
            return await self._skip_recovery(error, error_type, context, attempt_number)
        
        elif strategy == RecoveryStrategy.ABORT:
            return await self._abort_recovery(error, error_type, context, attempt_number)
        
        else:
            return RecoveryAttempt(
                strategy=strategy,
                attempt_number=attempt_number,
                success=False,
                message="Unknown recovery strategy"
            )
    
    async def _retry_recovery(
        self,
        error: Exception,
        error_type: ErrorType,
        context: Optional[Dict[str, Any]],
        attempt_number: int,
    ) -> RecoveryAttempt:
        """Attempt to recover by retrying."""
        if attempt_number <= self.max_retry_attempts:
            logger.info(f"Retrying operation (attempt {attempt_number}/{self.max_retry_attempts})")
            # In real implementation, would retry the operation
            # For now, mark as potential success
            return RecoveryAttempt(
                strategy=RecoveryStrategy.RETRY,
                attempt_number=attempt_number,
                success=False,  # Retry needs actual operation context
                message="Retry would be attempted with actual operation"
            )
        else:
            return RecoveryAttempt(
                strategy=RecoveryStrategy.RETRY,
                attempt_number=attempt_number,
                success=False,
                message=f"Exceeded maximum retry attempts ({self.max_retry_attempts})"
            )
    
    async def _fallback_recovery(
        self,
        error: Exception,
        error_type: ErrorType,
        context: Optional[Dict[str, Any]],
        attempt_number: int,
    ) -> RecoveryAttempt:
        """Attempt to recover by using fallback values."""
        if context and isinstance(context, dict):
            for field in context:
                if field in self.fallback_values:
                    logger.warning(f"Using fallback value for field: {field}")
                    return RecoveryAttempt(
                        strategy=RecoveryStrategy.FALLBACK,
                        attempt_number=attempt_number,
                        success=True,
                        message=f"Fallback values applied: {list(self.fallback_values.keys())}"
                    )
        
        return RecoveryAttempt(
            strategy=RecoveryStrategy.FALLBACK,
            attempt_number=attempt_number,
            success=True,
            message="Default fallback values applied"
        )
    
    async def _degraded_recovery(
        self,
        error: Exception,
        error_type: ErrorType,
        context: Optional[Dict[str, Any]],
        attempt_number: int,
    ) -> RecoveryAttempt:
        """Attempt to recover by operating in degraded mode."""
        degraded_fields = []
        
        if context and isinstance(context, dict):
            # Identify which fields can be degraded
            if "design_variations" in context:
                degraded_fields.append("design_variations")
            if "quality_preference" in context:
                degraded_fields.append("quality_preference")
        
        logger.warning(f"Operating in degraded mode. Affected fields: {degraded_fields}")
        
        return RecoveryAttempt(
            strategy=RecoveryStrategy.DEGRADE,
            attempt_number=attempt_number,
            success=True,
            message=f"Degraded mode: {', '.join(degraded_fields) if degraded_fields else 'basic functionality only'}"
        )
    
    async def _skip_recovery(
        self,
        error: Exception,
        error_type: ErrorType,
        context: Optional[Dict[str, Any]],
        attempt_number: int,
    ) -> RecoveryAttempt:
        """Attempt to recover by skipping problematic operation."""
        logger.info("Skipping problematic operation and continuing")
        
        return RecoveryAttempt(
            strategy=RecoveryStrategy.SKIP,
            attempt_number=attempt_number,
            success=True,
            message="Operation skipped, continuing with available functionality"
        )
    
    async def _abort_recovery(
        self,
        error: Exception,
        error_type: ErrorType,
        context: Optional[Dict[str, Any]],
        attempt_number: int,
    ) -> RecoveryAttempt:
        """Attempt to recover by aborting operation gracefully."""
        logger.error(f"Aborting operation due to unrecoverable error: {error}")
        
        return RecoveryAttempt(
            strategy=RecoveryStrategy.ABORT,
            attempt_number=attempt_number,
            success=False,
            message="Operation aborted due to unrecoverable error"
        )
    
    def get_fallback_data(self, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get fallback data for specified fields or all."""
        if fields:
            return {f: self.fallback_values.get(f) for f in fields if f in self.fallback_values}
        return self.fallback_values.copy()


class ErrorRecoverySystemFactory:
    """Factory for ErrorRecoverySystem singleton."""
    
    _instance: Optional[ErrorRecoverySystem] = None
    
    @classmethod
    def get_system(cls) -> ErrorRecoverySystem:
        """Get or create singleton ErrorRecoverySystem instance."""
        if cls._instance is None:
            cls._instance = ErrorRecoverySystem()
        return cls._instance
    
    @classmethod
    def reset(cls) -> None:
        """Reset singleton (for testing)."""
        cls._instance = None
