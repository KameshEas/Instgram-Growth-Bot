import asyncio
from typing import Dict, Any, TYPE_CHECKING
from src.agents.base_agent import BaseAgent
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from src.main import InstagramGrowthBot


class AnalyticsAgent(BaseAgent):
    """Daily/weekly/monthly AI-powered reporting"""

    def __init__(self, groq_bot: "InstagramGrowthBot | None" = None):
        super().__init__("Analytics")
        self._groq_bot = groq_bot
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analytics operations"""
        try:
            report_type = input_data.get("report_type", "daily")
            
            if report_type == "daily":
                return await self._daily_report(input_data)
            elif report_type == "weekly":
                return await self._weekly_report(input_data)
            elif report_type == "monthly":
                return await self._monthly_report(input_data)
            else:
                return {"status": "error", "message": f"Unknown report type: {report_type}"}
        
        except Exception as e:
            self.logger.error(f"Analytics error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    @staticmethod
    def _wrap_report(result, report_type: str) -> Dict[str, Any]:
        """Shape the LLM output the way telegram_bot.analytics_command expects."""
        if isinstance(result, dict) and result and "error" not in result:
            return {"status": "success", "report_type": report_type, "report": result}
        error = result.get("error", "Empty report") if isinstance(result, dict) else str(result)
        return {"status": "error", "report_type": report_type, "error": error}

    async def _daily_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate daily AI-estimated report"""
        niche = data.get("niche", "")
        follower_count = data.get("follower_count")
        account_stage = data.get("account_stage", "")
        content_mix = data.get("content_mix")
        region = data.get("region", "")
        chat_id = data.get("chat_id")

        if self._groq_bot:
            try:
                result = await asyncio.to_thread(self._groq_bot.generate_analytics_report, 
                    report_type="daily",
                    niche=niche,
                    follower_count=follower_count,
                    account_stage=account_stage,
                    content_mix=content_mix,
                    region=region,
                    chat_id=chat_id,
                )
                result = self._wrap_report(result, "daily")
                await self.log_execution(data, result, result["status"])
                return result
            except Exception as e:
                self.logger.warning(f"Groq daily report fallback: {e}")

        return {
            "status": "unavailable",
            "report_type": "daily",
            "message": "AI is currently unavailable. Please try again shortly.",
            "generated_at": datetime.utcnow().isoformat(),
        }
    
    async def _weekly_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate weekly AI-estimated report"""
        niche = data.get("niche", "")
        follower_count = data.get("follower_count")
        account_stage = data.get("account_stage", "")
        content_mix = data.get("content_mix")
        region = data.get("region", "")
        chat_id = data.get("chat_id")

        if self._groq_bot:
            try:
                result = await asyncio.to_thread(self._groq_bot.generate_analytics_report, 
                    report_type="weekly",
                    niche=niche,
                    follower_count=follower_count,
                    account_stage=account_stage,
                    content_mix=content_mix,
                    region=region,
                    chat_id=chat_id,
                )
                result = self._wrap_report(result, "weekly")
                await self.log_execution(data, result, result["status"])
                return result
            except Exception as e:
                self.logger.warning(f"Groq weekly report fallback: {e}")

        return {
            "status": "unavailable",
            "report_type": "weekly",
            "message": "AI is currently unavailable. Please try again shortly.",
            "generated_at": datetime.utcnow().isoformat(),
        }
    
    async def _monthly_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate monthly AI-estimated report"""
        niche = data.get("niche", "")
        follower_count = data.get("follower_count")
        account_stage = data.get("account_stage", "")
        content_mix = data.get("content_mix")
        region = data.get("region", "")
        chat_id = data.get("chat_id")

        if self._groq_bot:
            try:
                result = await asyncio.to_thread(self._groq_bot.generate_analytics_report, 
                    report_type="monthly",
                    niche=niche,
                    follower_count=follower_count,
                    account_stage=account_stage,
                    content_mix=content_mix,
                    region=region,
                    chat_id=chat_id,
                )
                result = self._wrap_report(result, "monthly")
                await self.log_execution(data, result, result["status"])
                return result
            except Exception as e:
                self.logger.warning(f"Groq monthly report fallback: {e}")

        return {
            "status": "unavailable",
            "report_type": "monthly",
            "message": "AI is currently unavailable. Please try again shortly.",
            "generated_at": datetime.utcnow().isoformat(),
        }

