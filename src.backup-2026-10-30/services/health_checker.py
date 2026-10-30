"""Health check system for monitoring bot health status.

Provides real-time health status for Docker health checks and monitoring dashboards.
Tracks API availability, database connectivity, and resource usage.
"""

import logging
import psutil
import sqlite3
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status levels."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class ComponentHealth(Enum):
    """Individual component health status."""
    UP = "up"
    DEGRADED = "degraded"
    DOWN = "down"


class HealthChecker:
    """Monitor and report on bot health status."""

    def __init__(self, bot=None):
        """Initialize health checker.

        Args:
            bot: InstagramGrowthBot instance (optional)
        """
        self.bot = bot
        self.check_history: Dict[str, list] = {}
        self.last_check_time: Optional[datetime] = None

    def perform_full_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check.

        Returns:
            Full health status report
        """
        self.last_check_time = datetime.now()

        checks = {
            "timestamp": self.last_check_time.isoformat(),
            "bot_status": self._check_bot_status(),
            "database_status": self._check_database(),
            "api_status": self._check_api(),
            "resource_status": self._check_resources(),
        }

        # Determine overall health
        component_statuses = [
            checks["bot_status"]["status"],
            checks["database_status"]["status"],
            checks["api_status"]["status"],
            checks["resource_status"]["status"],
        ]

        if all(s == ComponentHealth.UP.value for s in component_statuses):
            overall_status = HealthStatus.HEALTHY.value
        elif all(s in [ComponentHealth.UP.value, ComponentHealth.DEGRADED.value] for s in component_statuses):
            overall_status = HealthStatus.DEGRADED.value
        else:
            overall_status = HealthStatus.UNHEALTHY.value

        checks["overall_status"] = overall_status
        checks["overall_status_code"] = 200 if overall_status == HealthStatus.HEALTHY.value else 503

        # Store in history
        self._record_check(checks)

        return checks

    def _check_bot_status(self) -> Dict[str, Any]:
        """Check bot initialization and readiness."""
        try:
            if not self.bot:
                return {
                    "status": ComponentHealth.DEGRADED.value,
                    "details": "Bot instance not available for checking",
                }

            # Check if retry handler is available
            if not hasattr(self.bot, "retry_handler"):
                return {
                    "status": ComponentHealth.DEGRADED.value,
                    "details": "Retry handler not initialized",
                }

            # Check circuit breaker status
            circuit_status = self.bot.retry_handler.get_circuit_status()
            if circuit_status["circuit_open"]:
                return {
                    "status": ComponentHealth.DEGRADED.value,
                    "circuit_breaker": circuit_status,
                    "details": "Circuit breaker open (API recovery in progress)",
                }

            return {
                "status": ComponentHealth.UP.value,
                "details": "Bot fully operational",
                "circuit_breaker": circuit_status,
            }
        except Exception as e:
            logger.error(f"[HEALTH] Bot status check failed: {e}")
            return {
                "status": ComponentHealth.DOWN.value,
                "error": str(e),
            }

    def _check_database(self) -> Dict[str, Any]:
        """Check database connectivity."""
        db_path = Path("data/users.db")
        try:
            if not db_path.exists():
                return {
                    "status": ComponentHealth.DEGRADED.value,
                    "details": "Database file not found",
                }

            # Try to connect
            conn = sqlite3.connect(str(db_path), timeout=2)
            cursor = conn.cursor()

            # Simple query to verify connectivity
            cursor.execute("SELECT 1")
            conn.close()

            return {
                "status": ComponentHealth.UP.value,
                "database_path": str(db_path),
                "file_size_mb": db_path.stat().st_size / (1024 * 1024),
            }
        except Exception as e:
            logger.error(f"[HEALTH] Database check failed: {e}")
            return {
                "status": ComponentHealth.DOWN.value,
                "error": str(e),
            }

    def _check_api(self) -> Dict[str, Any]:
        """Check API connectivity (Groq)."""
        try:
            if not self.bot or not hasattr(self.bot, "client"):
                return {
                    "status": ComponentHealth.DEGRADED.value,
                    "details": "Groq client not available",
                }

            # Check if circuit breaker is open
            if (
                hasattr(self.bot, "retry_handler")
                and self.bot.retry_handler.get_circuit_status()["circuit_open"]
            ):
                return {
                    "status": ComponentHealth.DOWN.value,
                    "details": "Groq API circuit breaker open",
                }

            # Model information
            model = getattr(self.bot, "model", "unknown")

            return {
                "status": ComponentHealth.UP.value,
                "model": model,
                "details": "Groq API available",
            }
        except Exception as e:
            logger.error(f"[HEALTH] API check failed: {e}")
            return {
                "status": ComponentHealth.DOWN.value,
                "error": str(e),
            }

    def _check_resources(self) -> Dict[str, Any]:
        """Check system resource usage."""
        try:
            process = psutil.Process()

            # Memory usage
            memory_info = process.memory_info()
            memory_percent = process.memory_percent()

            # CPU usage
            cpu_percent = process.cpu_percent(interval=0.1)

            # Disk usage
            disk_usage = psutil.disk_usage("/")

            # Determine degradation
            status = ComponentHealth.UP.value
            warnings = []

            if memory_percent > 80:
                status = ComponentHealth.DEGRADED.value
                warnings.append(f"High memory usage: {memory_percent:.1f}%")

            if cpu_percent > 90:
                status = ComponentHealth.DEGRADED.value
                warnings.append(f"High CPU usage: {cpu_percent:.1f}%")

            if disk_usage.percent > 90:
                status = ComponentHealth.DEGRADED.value
                warnings.append(f"Low disk space: {disk_usage.percent:.1f}% used")

            return {
                "status": status,
                "memory_mb": memory_info.rss / (1024 * 1024),
                "memory_percent": memory_percent,
                "cpu_percent": cpu_percent,
                "disk_usage_percent": disk_usage.percent,
                "warnings": warnings,
            }
        except Exception as e:
            logger.error(f"[HEALTH] Resource check failed: {e}")
            return {
                "status": ComponentHealth.DEGRADED.value,
                "error": str(e),
            }

    def _record_check(self, check_result: Dict[str, Any]):
        """Record check result in history.

        Args:
            check_result: Health check result
        """
        status = check_result["overall_status"]
        if status not in self.check_history:
            self.check_history[status] = []

        # Keep last 100 checks per status
        self.check_history[status].append({
            "timestamp": check_result["timestamp"],
            "status_code": check_result["overall_status_code"],
        })

        if len(self.check_history[status]) > 100:
            self.check_history[status] = self.check_history[status][-100:]

    def get_health_status(self, include_history: bool = False) -> Dict[str, Any]:
        """Get current health status.

        Args:
            include_history: Whether to include check history

        Returns:
            Current health status (performs check if not recent)
        """
        # Perform check if not done recently (last 30 seconds)
        if (
            not self.last_check_time
            or datetime.now() - self.last_check_time > timedelta(seconds=30)
        ):
            status = self.perform_full_health_check()
        else:
            status = {
                "timestamp": self.last_check_time.isoformat(),
                "note": "Using cached check result",
            }

        if include_history:
            status["history"] = self.check_history

        return status

    def get_docker_health_check(self) -> int:
        """Get exit code for Docker health check.

        Returns:
            0 if healthy, 1 if unhealthy
        """
        status = self.perform_full_health_check()
        return 0 if status["overall_status"] == HealthStatus.HEALTHY.value else 1


# Global health checker instance
_health_checker: Optional[HealthChecker] = None


def get_health_checker(bot=None) -> HealthChecker:
    """Get or create global health checker instance.

    Args:
        bot: Bot instance to monitor (optional)

    Returns:
        HealthChecker instance
    """
    global _health_checker
    if _health_checker is None:
        _health_checker = HealthChecker(bot=bot)
    return _health_checker
