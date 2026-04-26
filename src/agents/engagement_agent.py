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
        """AI-powered engagement strategy for a specific account size tier.

        Calls ``groq_bot.engagement_strategy()`` when available so the
        response is dynamic and AI-generated.  Falls back to the built-in
        static strategies dict otherwise.
        """
        account_size = data.get("account_size", "micro")
        if self._groq_bot:
            try:
                result = self._groq_bot.engagement_strategy(account_size=account_size)
                await self.log_execution(data, result, "success")
                return result
            except Exception as e:
                self.logger.warning(f"Groq engagement fallback triggered: {e}")
        # Static fallback
        return await self._engagement_strategies({**data, "niche": account_size})

    async def _engagement_strategies(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get engagement strategies for niche"""
        try:
            niche = data.get("niche", "photography")
            
            strategies = {
                "status": "success",
                "niche": niche,
                "action": "strategies",
                "note": "These are strategy recommendations. Actual automation is out of scope for MVP.",
                "strategies": [
                    {
                        "strategy": "Engagement Pod Coordination",
                        "description": "Join 5-10 accounts of similar size and engage with each other's content within 1 hour of posting",
                        "expected_impact": "15-30 extra likes per post, boosted algorithm reach",
                        "frequency": "For every post",
                        "effort": "Medium"
                    },
                    {
                        "strategy": "Strategic Commenting",
                        "description": "Leave thoughtful comments (min 3 words) on 20-30 posts in trending hashtags daily",
                        "expected_impact": "5-15 new followers per day",
                        "frequency": "Daily",
                        "effort": "High"
                    },
                    {
                        "strategy": "Hashtag Following",
                        "description": "Follow accounts who post in your niche hashtags, engage with their content",
                        "expected_impact": "Follow-back rate 20-30%",
                        "frequency": "Daily",
                        "effort": "Medium"
                    },
                    {
                        "strategy": "DM Outreach",
                        "description": "Send personalized DMs to new followers with value (tips, collaboration offers)",
                        "expected_impact": "5-10% conversion to engaged followers",
                        "frequency": "3x per week",
                        "effort": "High"
                    },
                    {
                        "strategy": "Call-to-Action Optimization",
                        "description": "Add specific CTAs in captions (Ask question, suggest engagement, link in bio)",
                        "expected_impact": "30-50% increase in comments and saves",
                        "frequency": "Every post",
                        "effort": "Low"
                    }
                ],
                "daily_time_investment": "45-60 minutes",
                "projected_monthly_growth": "100-200 followers (sustainable, organic)",
                "generated_at": datetime.utcnow().isoformat()
            }
            
            await self.log_execution(data, strategies, "success")
            return strategies
        
        except Exception as e:
            self.logger.error(f"Strategy error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _growth_tips(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get growth tips"""
        try:
            tips = {
                "status": "success",
                "action": "growth_tips",
                "tips": [
                    {
                        "priority": 1,
                        "tip": "Post Consistently",
                        "detail": "Post 2-3 times daily at peak hours (10 AM, 1 PM, 7 PM)",
                        "impact": "Highest - 40% of growth"
                    },
                    {
                        "priority": 2,
                        "tip": "Focus on Video Content",
                        "detail": "70% Reels, 20% Stories, 10% Static posts",
                        "impact": "Very High - 30% of growth"
                    },
                    {
                        "priority": 3,
                        "tip": "Use Trending Sounds",
                        "detail": "Research trending sounds for your niche weekly",
                        "impact": "High - 15% of growth"
                    },
                    {
                        "priority": 4,
                        "tip": "Engage in First Hour",
                        "description": "Respond to ALL comments in first 60 minutes of posting",
                        "impact": "Medium - 10% of growth"
                    },
                    {
                        "priority": 5,
                        "tip": "Optimize Hashtags",
                        "detail": "Use 25-30 hashtags: 5 high-reach, 10 medium-reach, 15 niche",
                        "impact": "Medium - 5% of growth"
                    }
                ],
                "generated_at": datetime.utcnow().isoformat()
            }
            
            return tips
        
        except Exception as e:
            self.logger.error(f"Tips error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _hashtag_strategy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get hashtag strategy"""
        try:
            strategy = {
                "status": "success",
                "action": "hashtag_strategy",
                "strategy": {
                    "total_hashtags_recommended": 30,
                    "breakdown": {
                        "high_reach": {
                            "count": 5,
                            "followers": "100K-1M",
                            "competition": "Very High",
                            "use_case": "Branding, reach"
                        },
                        "medium_reach": {
                            "count": 10,
                            "followers": "10K-100K",
                            "competition": "High",
                            "use_case": "Visibility, discoverability"
                        },
                        "niche": {
                            "count": 15,
                            "followers": "1K-10K",
                            "competition": "Low",
                            "use_case": "Targeted audience, conversion"
                        }
                    },
                    "rotation_strategy": "Rotate 30% of hashtags every post to avoid looking like bot",
                    "best_practices": [
                        "Research hashtags before using",
                        "Check competition (posts using it)",
                        "Follow hashtags to see trending content",
                        "Create branded hashtag for your niche",
                        "Use hashtags in first comment, not caption (for visibility)"
                    ]
                },
                "generated_at": datetime.utcnow().isoformat()
            }
            
            return strategy
        
        except Exception as e:
            self.logger.error(f"Hashtag strategy error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _posting_schedule(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get optimal posting schedule"""
        try:
            schedule = {
                "status": "success",
                "action": "posting_schedule",
                "note": "Optimal times based on typical Instagram audience patterns",
                "schedule": {
                    "weekday": [
                        {"time": "8:00 AM", "reason": "Morning coffee routine, high engagement"},
                        {"time": "1:00 PM", "reason": "Lunch break browsing"},
                        {"time": "7:00 PM", "reason": "Evening wind-down, peak engagement"}
                    ],
                    "weekend": [
                        {"time": "9:00 AM", "reason": "Weekend morning leisure"},
                        {"time": "3:00 PM", "reason": "Afternoon activity planning"},
                        {"time": "8:00 PM", "reason": "Evening social time"}
                    ],
                    "tip": "Test these times for 2 weeks and analyze your own audience data"
                },
                "frequency": "2-3 posts per day recommended",
                "generated_at": datetime.utcnow().isoformat()
            }
            
            return schedule
        
        except Exception as e:
            self.logger.error(f"Schedule error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _comment_templates(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comment templates for engagement"""
        try:
            templates = {
                "status": "success",
                "action": "comment_templates",
                "warning": "These are templates. Personalize them! Generic comments get ignored.",
                "templates": {
                    "praise": [
                        "This is absolutely stunning! The [specific element] is perfection 🔥",
                        "The detail in [specific element] is incredible! 😍",
                        "This deserves way more engagement! [specific observation] ✨"
                    ],
                    "question": [
                        "How did you achieve [specific technique] in this shot?",
                        "What camera settings did you use for this? The [specific element] is beautiful!",
                        "Is this [specific location/setup]? Would love to visit!"
                    ],
                    "relatable": [
                        "I struggle with this too! Would love to learn your approach 💪",
                        "This is exactly what I needed to see today. How did you overcome [problem]?",
                        "Same, I've been trying to master [skill] too!"
                    ],
                    "call_to_action": [
                        "Saving this for inspiration! Do you have a tutorial on this?",
                        "This deserves to be featured! 🙌",
                        "Collaborating is a great idea. Are you open to [collab type]?"
                    ]
                },
                "comment_rules": [
                    "Always be genuine - no generic emoji spamming",
                    "Keep comments 3-15 words minimum",
                    "Reference something specific from the post",
                    "Add 1-2 emojis for personality",
                    "Ask questions to start conversations",
                    "Avoid self-promotion in comments"
                ],
                "generated_at": datetime.utcnow().isoformat()
            }
            
            return templates
        
        except Exception as e:
            self.logger.error(f"Templates error: {str(e)}")
            return {"status": "error", "error": str(e)}
