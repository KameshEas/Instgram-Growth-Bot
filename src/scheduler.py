#!/usr/bin/env python3
"""
Task Scheduler for Instagram Growth Bot
Runs bot on a schedule with retry logic and monitoring
"""

import os
import json
import logging
import time
import atexit
from datetime import datetime, timedelta
from typing import Callable, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging with file output
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_dir}/scheduler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BotScheduler:
    """Simple scheduler for running bot on intervals"""
    
    def __init__(self, task: Callable, interval_minutes: int = 60):
        """
        Initialize scheduler
        
        Args:
            task: Function to run
            interval_minutes: Minutes between runs (default: 60 = hourly)
        """
        self.task = task
        self.interval = timedelta(minutes=interval_minutes)
        self.next_run = datetime.now()
        self.running = False
        self.stats = {
            "runs": 0,
            "successes": 0,
            "failures": 0,
            "total_duration": 0,
            "last_run": None,
            "last_error": None
        }
        
        # Register cleanup on exit
        atexit.register(self.shutdown)
        logger.info(f"✅ Scheduler initialized (interval: {interval_minutes} min)")
    
    def run_once(self) -> bool:
        """Execute task once and track metrics"""
        start_time = time.time()
        logger.info(f"🚀 Running task at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            self.task()
            duration = time.time() - start_time
            
            self.stats["runs"] += 1
            self.stats["successes"] += 1
            self.stats["total_duration"] += duration
            self.stats["last_run"] = datetime.now().isoformat()
            
            logger.info(f"✅ Task completed successfully ({duration:.2f}s)")
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            
            self.stats["runs"] += 1
            self.stats["failures"] += 1
            self.stats["last_error"] = str(e)
            
            logger.error(f"❌ Task failed after {duration:.2f}s: {e}")
            return False
    
    def should_run(self) -> bool:
        """Check if enough time has passed for next run"""
        return datetime.now() >= self.next_run
    
    def schedule_next(self):
        """Schedule next run"""
        self.next_run = datetime.now() + self.interval
        logger.debug(f"Next run scheduled for {self.next_run.strftime('%H:%M:%S')}")
    
    def start(self, run_once: bool = False):
        """Start scheduler loop"""
        if run_once:
            logger.info("Running task once...")
            self.run_once()
            return
        
        self.running = True
        logger.info("🟢 Scheduler started (press Ctrl+C to stop)")
        
        try:
            while self.running:
                if self.should_run():
                    self.run_once()
                    self.schedule_next()
                    self.print_stats()
                
                # Sleep to avoid busy waiting
                time.sleep(30)
                
        except KeyboardInterrupt:
            logger.info("⏹️ Scheduler stopped by user")
        finally:
            self.shutdown()
    
    def print_stats(self):
        """Print scheduler statistics"""
        if self.stats["runs"] == 0:
            return
        
        success_rate = (self.stats["successes"] / self.stats["runs"]) * 100
        avg_duration = self.stats["total_duration"] / self.stats["runs"]
        
        logger.info(f"""
        📊 Scheduler Statistics:
           - Total Runs: {self.stats["runs"]}
           - Successes: {self.stats["successes"]}
           - Failures: {self.stats["failures"]}
           - Success Rate: {success_rate:.1f}%
           - Avg Duration: {avg_duration:.2f}s
           - Last Run: {self.stats["last_run"]}
        """)
    
    def shutdown(self):
        """Clean shutdown"""
        self.running = False
        logger.info("🛑 Scheduler shutdown")
        self.print_stats()
    
    def get_stats(self) -> dict:
        """Get scheduler statistics"""
        return self.stats.copy()


class ExponentialBackoffRetry:
    """Retry decorator with exponential backoff"""
    
    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0):
        """
        Initialize retry decorator
        
        Args:
            max_attempts: Maximum retry attempts
            base_delay: Base delay in seconds (multiplied by 2^attempt)
        """
        self.max_attempts = max_attempts
        self.base_delay = base_delay
    
    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            for attempt in range(1, self.max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == self.max_attempts:
                        logger.error(f"❌ {func.__name__} failed after {self.max_attempts} attempts")
                        raise
                    
                    delay = self.base_delay * (2 ** (attempt - 1))
                    logger.warning(f"⚠️ Attempt {attempt}/{self.max_attempts} failed: {e}")
                    logger.info(f"⏳ Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)
        
        return wrapper


# Example usage
if __name__ == "__main__":
    # Import bot
    from src.main import InstagramGrowthBot
    
    # Create scheduler task
    @ExponentialBackoffRetry(max_attempts=3)
    def bot_task():
        bot = InstagramGrowthBot()
        
        # Run all agents
        bot.generate_content(topic="fitness", style="motivational")
        bot.analyze_trends(niche="fitness")
        bot.engagement_strategy(account_size="micro (5K-100K)")
        bot.monetization_ideas(niche="fitness", follower_count=50000)
    
    # Create scheduler (hourly runs)
    scheduler = BotScheduler(task=bot_task, interval_minutes=60)
    
    # Start scheduler
    # Use run_once=True for testing, False for continuous scheduling
    scheduler.start(run_once=os.getenv("SCHEDULE_ONCE", "false").lower() == "true")
