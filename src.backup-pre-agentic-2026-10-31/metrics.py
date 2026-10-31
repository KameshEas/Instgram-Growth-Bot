#!/usr/bin/env python3
"""
Performance Metrics & Monitoring
Tracks bot execution metrics, API calls, and errors
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of metrics to track"""
    API_CALL = "api_call"
    CONTENT_GENERATED = "content_generated"
    ERROR = "error"
    LATENCY = "latency"
    SUCCESS = "success"


class PerformanceMetrics:
    """Track and store performance metrics"""
    
    def __init__(self, metrics_dir: str = "metrics"):
        """Initialize metrics tracker"""
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(exist_ok=True)
        
        self.current_session = {
            "start_time": datetime.now(),
            "metrics": [],
            "total_api_calls": 0,
            "total_errors": 0,
            "total_duration": 0.0,
            "avg_latency": 0.0,
            "success_rate": 0.0
        }
        
        logger.debug(f"✅ Metrics initialized in {metrics_dir}")
    
    def record_api_call(self, model: str, duration: float, success: bool, 
                       prompt_length: int = 0, response_length: int = 0):
        """Record API call metrics"""
        self.current_session["total_api_calls"] += 1
        if not success:
            self.current_session["total_errors"] += 1
        
        metric = {
            "timestamp": datetime.now().isoformat(),
            "type": MetricType.API_CALL.value,
            "model": model,
            "duration": duration,
            "success": success,
            "prompt_length": prompt_length,
            "response_length": response_length
        }
        
        self.current_session["metrics"].append(metric)
        logger.debug(f"📊 API call recorded: {model} ({duration:.2f}s) - {'✅' if success else '❌'}")
    
    def record_content_generation(self, topic: str, captions_count: int, 
                                 virality_score: float):
        """Record content generation"""
        metric = {
            "timestamp": datetime.now().isoformat(),
            "type": MetricType.CONTENT_GENERATED.value,
            "topic": topic,
            "captions": captions_count,
            "virality_score": virality_score
        }
        
        self.current_session["metrics"].append(metric)
        logger.info(f"📝 Content generated: {topic} ({captions_count} captions, virality: {virality_score})")
    
    def record_error(self, error_type: str, error_message: str, agent: str):
        """Record error"""
        self.current_session["total_errors"] += 1
        
        metric = {
            "timestamp": datetime.now().isoformat(),
            "type": MetricType.ERROR.value,
            "error_type": error_type,
            "error_message": str(error_message)[:200],  # Truncate long messages
            "agent": agent
        }
        
        self.current_session["metrics"].append(metric)
        logger.error(f"❌ Error in {agent}: {error_type} - {error_message}")
    
    def finalize_session(self):
        """Calculate session statistics"""
        if not self.current_session["metrics"]:
            logger.warning("⚠️ No metrics recorded in session")
            return
        
        # Calculate statistics
        end_time = datetime.now()
        duration = (end_time - self.current_session["start_time"]).total_seconds()
        self.current_session["total_duration"] = duration
        
        if self.current_session["total_api_calls"] > 0:
            success_count = self.current_session["total_api_calls"] - self.current_session["total_errors"]
            self.current_session["success_rate"] = (success_count / self.current_session["total_api_calls"]) * 100
        
        # Get latencies from API calls
        api_calls = [m for m in self.current_session["metrics"] if m["type"] == MetricType.API_CALL.value]
        if api_calls:
            avg_latency = sum(m["duration"] for m in api_calls) / len(api_calls)
            self.current_session["avg_latency"] = avg_latency
        
        # Save to file
        self._save_session()
    
    def _save_session(self):
        """Save session metrics to JSON file"""
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = self.metrics_dir / f"session_{timestamp}.json"
        
        try:
            with open(filepath, "w") as f:
                json.dump(self.current_session, f, indent=2)
            logger.info(f"💾 Session metrics saved: {filepath}")
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get session summary"""
        return {
            "start_time": self.current_session["start_time"].isoformat(),
            "total_api_calls": self.current_session["total_api_calls"],
            "total_errors": self.current_session["total_errors"],
            "success_rate": f"{self.current_session['success_rate']:.1f}%",
            "total_duration": f"{self.current_session['total_duration']:.2f}s",
            "avg_latency": f"{self.current_session['avg_latency']:.2f}s",
            "metrics_count": len(self.current_session["metrics"])
        }
    
    def print_summary(self):
        """Print readable session summary"""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("📊 SESSION METRICS SUMMARY")
        print("="*60)
        print(f"Start Time:    {summary['start_time']}")
        print(f"API Calls:     {summary['total_api_calls']}")
        print(f"Errors:        {summary['total_errors']}")
        print(f"Success Rate:  {summary['success_rate']}")
        print(f"Duration:      {summary['total_duration']}")
        print(f"Avg Latency:   {summary['avg_latency']}")
        print(f"Metrics Recorded: {summary['metrics_count']}")
        print("="*60 + "\n")


class HealthCheck:
    """Simple health check for monitoring"""
    
    def __init__(self):
        self.status = "healthy"
        self.last_run = None
        self.error_count = 0
        self.consecutive_errors = 0
        self.max_consecutive_errors = 3
    
    def record_success(self):
        """Record successful run"""
        self.status = "healthy"
        self.consecutive_errors = 0
        self.last_run = datetime.now()
        logger.debug("✅ Health check: healthy")
    
    def record_error(self):
        """Record error"""
        self.error_count += 1
        self.consecutive_errors += 1
        
        if self.consecutive_errors >= self.max_consecutive_errors:
            self.status = "unhealthy"
            logger.error(f"🚨 Health check: unhealthy ({self.consecutive_errors} errors)")
        else:
            self.status = "degraded"
            logger.warning(f"⚠️ Health check: degraded ({self.consecutive_errors} errors)")
        
        self.last_run = datetime.now()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current health status"""
        return {
            "status": self.status,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "error_count": self.error_count,
            "consecutive_errors": self.consecutive_errors
        }


# Export metrics instance for easy access
metrics = PerformanceMetrics()
health_check = HealthCheck()

__all__ = ["metrics", "health_check", "MetricType", "PerformanceMetrics", "HealthCheck"]
