from typing import Dict, Any, List, TYPE_CHECKING
from src.agents.base_agent import BaseAgent
from datetime import datetime

if TYPE_CHECKING:
    from src.main import InstagramGrowthBot


class EngagementAgent(BaseAgent):
    """Growth strategies and engagement recommendations (non-automation).

    When a ``groq_bot`` is supplied the agent delegates to Groq for
    AI-powered strategies.  Falls back to built-in static data otherwise.
    """

    def __init__(self, groq_bot: "InstagramGrowthBot | None" = None):
        super().__init__("Engagement")
        self._groq_bot = groq_bot
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute engagement strategy recommendations"""
        try:
            action = input_data.get("action", "strategies")

            if action == "strategy_for_size":
                return await self._strategy_for_account_size(input_data)
            elif action == "strategies":
                return await self._engagement_strategies(input_data)
            elif action == "growth_tips":
                return await self._growth_tips(input_data)
            elif action == "hashtag_strategy":
                return await self._hashtag_strategy(input_data)
            elif action == "posting_schedule":
                return await self._posting_schedule(input_data)
            elif action == "comment_templates":
                return await self._comment_templates(input_data)
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
        
        except Exception as e:
            self.logger.error(f"Engagement error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _strategy_for_account_size(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """AI-powered engagement strategy for a specific account size tier."""
        account_size = data.get("account_size", "micro")
        niche = data.get("niche", "")
        follower_count = data.get("follower_count")
        region = data.get("region", "")
        content_mix = data.get("content_mix")
        if self._groq_bot:
            try:
                result = self._groq_bot.engagement_strategy(
                    account_size=account_size,
                    niche=niche,
                    follower_count=follower_count,
                    region=region,
                    content_mix=content_mix,
                )
                await self.log_execution(data, result, "success")
                return result
            except Exception as e:
                self.logger.warning(f"Groq engagement fallback triggered: {e}")
        return await self._engagement_strategies(data)

    async def _engagement_strategies(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get engagement strategies — AI-powered when Groq is available."""
        if self._groq_bot:
            try:
                result = self._groq_bot.get_engagement_action(
                    action="strategies",
                    niche=data.get("niche", ""),
                    follower_count=data.get("follower_count"),
                    region=data.get("region", ""),
                )
                await self.log_execution(data, result, "success")
                return result
            except Exception as e:
                self.logger.warning(f"Groq fallback (strategies): {e}")
        return {
            "status": "unavailable",
            "action": "strategies",
            "message": "AI is currently unavailable. Please try again shortly.",
            "generated_at": datetime.utcnow().isoformat(),
        }

    async def _growth_tips(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get growth tips — AI-powered when Groq is available."""
        if self._groq_bot:
            try:
                result = self._groq_bot.get_engagement_action(
                    action="growth_tips",
                    niche=data.get("niche", ""),
                    follower_count=data.get("follower_count"),
                    region=data.get("region", ""),
                )
                await self.log_execution(data, result, "success")
                return result
            except Exception as e:
                self.logger.warning(f"Groq fallback (growth_tips): {e}")
        return {
            "status": "unavailable",
            "action": "growth_tips",
            "message": "AI is currently unavailable. Please try again shortly.",
            "generated_at": datetime.utcnow().isoformat(),
        }
    
    async def _hashtag_strategy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get hashtag strategy — AI-powered when Groq is available."""
        if self._groq_bot:
            try:
                result = self._groq_bot.get_engagement_action(
                    action="hashtag_strategy",
                    niche=data.get("niche", ""),
                    follower_count=data.get("follower_count"),
                    region=data.get("region", ""),
                )
                await self.log_execution(data, result, "success")
                return result
            except Exception as e:
                self.logger.warning(f"Groq fallback (hashtag_strategy): {e}")
        return {
            "status": "unavailable",
            "action": "hashtag_strategy",
            "message": "AI is currently unavailable. Please try again shortly.",
            "generated_at": datetime.utcnow().isoformat(),
        }
    
    async def _posting_schedule(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get optimal posting schedule — AI-powered when Groq is available."""
        if self._groq_bot:
            try:
                result = self._groq_bot.get_engagement_action(
                    action="posting_schedule",
                    niche=data.get("niche", ""),
                    follower_count=data.get("follower_count"),
                    region=data.get("region", ""),
                )
                await self.log_execution(data, result, "success")
                return result
            except Exception as e:
                self.logger.warning(f"Groq fallback (posting_schedule): {e}")
        return {
            "status": "unavailable",
            "action": "posting_schedule",
            "message": "AI is currently unavailable. Please try again shortly.",
            "generated_at": datetime.utcnow().isoformat(),
        }
    
    async def _comment_templates(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comment templates — AI-powered when Groq is available."""
        if self._groq_bot:
            try:
                result = self._groq_bot.get_engagement_action(
                    action="comment_templates",
                    niche=data.get("niche", ""),
                    follower_count=data.get("follower_count"),
                    region=data.get("region", ""),
                )
                await self.log_execution(data, result, "success")
                return result
            except Exception as e:
                self.logger.warning(f"Groq fallback (comment_templates): {e}")
        return {
            "status": "unavailable",
            "action": "comment_templates",
            "message": "AI is currently unavailable. Please try again shortly.",
            "generated_at": datetime.utcnow().isoformat(),
        }
