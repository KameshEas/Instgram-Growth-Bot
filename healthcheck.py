#!/usr/bin/env python3
"""Docker health check script for the Telegram bot.

Called by Docker every 30 seconds to verify bot health.
Exit 0 = healthy, exit 1 = unhealthy.
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Set up logging to suppress noisy output
os.environ["LOG_LEVEL"] = "ERROR"


def check_health() -> int:
    """Perform health check.

    Returns:
        0 if healthy, 1 if unhealthy
    """
    try:
        # Import here to avoid startup delays on container start
        from src.services.health_checker import get_health_checker, HealthStatus

        # Get health checker
        checker = get_health_checker()

        # Perform check
        status = checker.perform_full_health_check()

        # Determine exit code
        if status["overall_status"] == HealthStatus.HEALTHY.value:
            return 0
        else:
            return 1

    except Exception as e:
        # If we can't even perform the check, return unhealthy
        print(f"Health check failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit_code = check_health()
    sys.exit(exit_code)
