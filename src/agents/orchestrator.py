from typing import Dict, Any, TYPE_CHECKING
from src.agents.base_agent import BaseAgent
from src.agents.content_generator import ContentGeneratorAgent
from src.agents.engagement_agent import EngagementAgent
from src.agents.monetization_agent import MonetizationAgent
from src.agents.analytics_agent import AnalyticsAgent
from src.agents.trends_agent import TrendsAgent

if TYPE_CHECKING:
    from src.main import InstagramGrowthBot


class ContentOrchestratorAgent(BaseAgent):
    """Master orchestrator that routes every Telegram command to the correct agent.

    All agents that need AI power receive a reference to the shared
    ``InstagramGrowthBot`` (Groq wrapper) so they can call its methods while
    still falling back to their built-in static data when the bot is unavailable.
    """

    def __init__(self, groq_bot: "InstagramGrowthBot | None" = None):
        super().__init__("Orchestrator")
        self._groq_bot = groq_bot
        self.agents = {
            "content_generator": ContentGeneratorAgent(),
            "engagement": EngagementAgent(groq_bot=groq_bot),
            "monetization": MonetizationAgent(groq_bot=groq_bot),
            "analytics": AnalyticsAgent(),
            "trends": TrendsAgent(groq_bot=groq_bot),
        }

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Route the request to the correct agent based on the Telegram command."""
        try:
            command = input_data.get("command", "help")

            # ── Content library commands ──────────────────────────────────────
            if command == "/generate":
                custom_prompt = input_data.get("custom_prompt")
                category = input_data.get("category", "general_photography")
                level = input_data.get("level")
                if custom_prompt and custom_prompt.strip() and self._groq_bot:
                    # Custom-concept path: delegate to Groq for AI enhancement
                    result = self._groq_bot.image_generation_prompts(
                        category=category,
                        custom_prompt=custom_prompt,
                        level=level,
                    )
                else:
                    # Library path: serve from static prompt templates via agent
                    agent_result = await self.agents["content_generator"].execute({
                        **input_data,
                        "action": "generate",
                    })
                    # Normalise to the shape the telegram handler expects
                    if agent_result.get("status") == "success":
                        # Prompts may be dicts or plain strings
                        raw_prompts = agent_result.get("prompts", [])
                        prompt_strings = [
                            p["prompt"] if isinstance(p, dict) else p
                            for p in raw_prompts
                        ]
                        result = {
                            "status": "success",
                            "category": category,
                            "custom": False,
                            "level": level or "mixed",
                            "count": len(prompt_strings),
                            "prompts": prompt_strings,
                            "meta": {},
                            "available_categories": agent_result.get("available_categories", []),
                        }
                    else:
                        result = agent_result

            elif command == "/categories":
                result = await self.agents["content_generator"].execute({
                    **input_data,
                    "action": "list_categories",
                })

            elif command == "/search":
                result = await self.agents["content_generator"].execute({
                    **input_data,
                    "action": "search",
                    "keyword": input_data.get("keyword", ""),
                })

            # ── Caption / content generation (Groq direct — no agent covers it) ──
            elif command == "/content":
                if self._groq_bot:
                    result = self._groq_bot.generate_content(
                        topic=input_data.get("topic", ""),
                        style=input_data.get("style", "engaging"),
                    )
                else:
                    result = {"status": "error", "error": "Groq bot not available"}

            # ── Inspire — handler calls Groq client directly; pass through ─────
            elif command == "/inspire":
                result = {"status": "passthrough"}

            # ── Trends agent (real scrape + AI analysis) ──────────────────────
            elif command in ("/trends", "/viral", "/hashtags"):
                result = await self.agents["trends"].execute({
                    **input_data,
                    "action": "analyze_for_niche",
                    "niche": input_data.get("niche", "photography"),
                })

            # ── Engagement agent (AI strategy) ────────────────────────────────
            elif command == "/engagement":
                result = await self.agents["engagement"].execute({
                    **input_data,
                    "action": "strategy_for_size",
                    "account_size": input_data.get("account_size", "micro"),
                })

            # ── Monetization agent (AI ideas) ─────────────────────────────────
            elif command == "/monetize":
                result = await self.agents["monetization"].execute({
                    **input_data,
                    "action": "ideas_for_niche",
                    "niche": input_data.get("niche", "general"),
                    "follower_count": input_data.get("follower_count", 10000),
                })

            # ── Analytics agent ───────────────────────────────────────────────
            elif command in ("/analytics", "/report", "/stats"):
                result = await self.agents["analytics"].execute({
                    **input_data,
                    "report_type": input_data.get("report_type", "daily"),
                })

            # ── Help ──────────────────────────────────────────────────────────
            elif command in ("/help", "help"):
                result = self._get_help()

            else:
                result = {"status": "error", "message": f"Unknown command: {command}"}

            await self.log_execution(input_data, result, "success")
            return result

        except Exception as e:
            self.logger.error(f"Orchestrator error: {str(e)}")
            return {"status": "error", "error": str(e)}

    def _get_help(self) -> Dict[str, Any]:
        """Return the list of available commands mapped to their active agents."""
        return {
            "status": "success",
            "available_agents": 5,
            "commands": {
                "Content Library": {
                    "commands": ["/generate", "/categories", "/search"],
                    "agent": "ContentGeneratorAgent",
                },
                "Caption Generation": {
                    "commands": ["/content"],
                    "agent": "InstagramGrowthBot (Groq direct)",
                },
                "Trends": {
                    "commands": ["/trends"],
                    "agent": "TrendsAgent → InstagramGrowthBot",
                },
                "Engagement": {
                    "commands": ["/engagement"],
                    "agent": "EngagementAgent → InstagramGrowthBot",
                },
                "Monetization": {
                    "commands": ["/monetize"],
                    "agent": "MonetizationAgent → InstagramGrowthBot",
                },
                "Analytics": {
                    "commands": ["/analytics", "/report", "/stats"],
                    "agent": "AnalyticsAgent",
                },
            },
        }
