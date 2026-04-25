from typing import Dict, Any
from src.agents.base_agent import BaseAgent
from src.agents.content_generator import ContentGeneratorAgent
from src.agents.instagram_agent import InstagramIntegrationAgent
from src.agents.engagement_agent import EngagementAgent
from src.agents.monetization_agent import MonetizationAgent
from src.agents.analytics_agent import AnalyticsAgent
from src.agents.trends_agent import TrendsAgent
from src.agents.privacy_agent import PrivacyAgent

class ContentOrchestratorAgent(BaseAgent):
    """Master orchestrator routing requests to 9 specialized agents"""
    
    def __init__(self):
        super().__init__("Orchestrator")
        self.agents = {
            "content_generator": ContentGeneratorAgent(),
            "instagram": InstagramIntegrationAgent(),
            "engagement": EngagementAgent(),
            "monetization": MonetizationAgent(),
            "analytics": AnalyticsAgent(),
            "trends": TrendsAgent(),
            "privacy": PrivacyAgent()
        }
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Route requests to appropriate agents"""
        try:
            command = input_data.get("command", "help")
            
            # Content Generation Commands
            if command in ["/generate", "/create", "/content"]:
                result = await self.agents["content_generator"].execute(input_data)
            
            # Instagram Commands
            elif command in ["/post", "/schedule", "/cross_post"]:
                result = await self.agents["instagram"].execute(input_data)
            
            # Engagement Commands
            elif command in ["/engage", "/follow", "/comment", "/dm"]:
                result = await self.agents["engagement"].execute(input_data)
            
            # Monetization Commands
            elif command in ["/revenue", "/affiliate", "/sponsored", "/monetize"]:
                result = await self.agents["monetization"].execute(input_data)
            
            # Analytics Commands
            elif command in ["/analytics", "/report", "/stats"]:
                result = await self.agents["analytics"].execute(input_data)
            
            # Trends Commands
            elif command in ["/trends", "/viral", "/hashtags"]:
                result = await self.agents["trends"].execute(input_data)
            
            # Privacy Commands
            elif command in ["/security", "/privacy", "/backup"]:
                result = await self.agents["privacy"].execute(input_data)
            
            # Help Command
            elif command in ["/help", "help"]:
                result = self._get_help()
            
            else:
                result = {"status": "error", "message": f"Unknown command: {command}"}
            
            await self.log_execution(input_data, result, "success")
            return result
        
        except Exception as e:
            self.logger.error(f"Orchestrator error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def _get_help(self) -> Dict[str, Any]:
        """Get available commands and agent info"""
        return {
            "status": "success",
            "available_agents": 9,
            "commands": {
                "Content Generation": {
                    "command": "/generate",
                    "args": ["category", "style", "request"],
                    "agent": "ContentGeneratorAgent"
                },
                "Instagram": {
                    "command": "/post",
                    "args": ["action", "caption", "image"],
                    "agent": "InstagramIntegrationAgent"
                },
                "Engagement": {
                    "command": "/engage",
                    "args": ["action", "hashtag", "max_actions"],
                    "agent": "EngagementAgent"
                },
                "Monetization": {
                    "command": "/revenue",
                    "args": ["action", "details"],
                    "agent": "MonetizationAgent"
                },
                "Analytics": {
                    "command": "/analytics",
                    "args": ["report_type"],
                    "agent": "AnalyticsAgent"
                },
                "Trends": {
                    "command": "/trends",
                    "args": ["action", "platforms"],
                    "agent": "TrendsAgent"
                },
                "Privacy": {
                    "command": "/security",
                    "args": ["action"],
                    "agent": "PrivacyAgent"
                }
            }
        }
