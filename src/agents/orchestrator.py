from typing import Dict, Any, TYPE_CHECKING
from src.agents.base_agent import BaseAgent
from src.agents.content_generator import ContentGeneratorAgent
from src.agents.design_enhancer import DesignPromptEnhancerAgent
from src.agents.gift_design_agent import GiftDesignAgent
from src.agents.engagement_agent import EngagementAgent
from src.agents.monetization_agent import MonetizationAgent
from src.agents.analytics_agent import AnalyticsAgent
from src.agents.trends_agent import TrendsAgent
from src.prompts.templates import get_category_meta

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
            "content_generator": ContentGeneratorAgent(groq_bot=groq_bot),
            "design_enhancer": DesignPromptEnhancerAgent(groq_bot=groq_bot),
            "gift_design": GiftDesignAgent(groq_bot=groq_bot),
            "engagement": EngagementAgent(groq_bot=groq_bot),
            "monetization": MonetizationAgent(groq_bot=groq_bot),
            "analytics": AnalyticsAgent(groq_bot=groq_bot),
            "trends": TrendsAgent(groq_bot=groq_bot),
        }

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Route the request to the correct agent based on the Telegram command.
        
        For any message that is NOT a direct slash command, use AI intent classification
        to determine the best command to execute. This allows natural language inputs like
        'show me viral content about fitness' to route correctly without requiring /commands.
        """
        try:
            # ── Extract UserContext (thread into every agent call) ─────────────────
            niche = input_data.get("niche", "")
            follower_count = input_data.get("follower_count")
            region = input_data.get("region", "")
            language = input_data.get("language", "")
            account_stage = input_data.get("account_stage", "")
            chat_id = input_data.get("chat_id")

            # ── AI INTENT CLASSIFICATION (primary router for natural language) ─────
            command = input_data.get("command", "").strip()
            user_message = input_data.get("text", "").strip()
            
            # If message doesn't start with / and AI is available, classify intent first
            if (
                self._groq_bot
                and user_message
                and not command.startswith("/")
                and not input_data.get("_intent_classified")
            ):
                available_commands = [
                    "/generate", "/categories", "/search", "/content",
                    "/inspire", "/trends", "/viral", "/hashtags",
                    "/engagement", "/monetize", "/analytics", "/report",
                    "/stats", "/help",
                ]
                try:
                    intent = self._groq_bot.classify_intent(
                        user_message=user_message,
                        available_commands=available_commands,
                        chat_id=chat_id,
                    )
                    if (
                        isinstance(intent, dict)
                        and not intent.get("fallback_to_chat")
                        and float(intent.get("confidence", 0)) >= 0.5
                    ):
                        classified_cmd = intent.get("command", "")
                        extracted = intent.get("extracted_params", {}) or {}
                        self.logger.info(
                            f"[INTENT] Classified '{user_message[:40]}...' → {classified_cmd} "
                            f"(confidence: {intent.get('confidence', 0):.2f})"
                        )
                        return await self.execute({
                            **input_data,
                            **extracted,
                            "command": classified_cmd,
                            "_intent_classified": True,
                        })
                    else:
                        confidence = float(intent.get("confidence", 0))
                        self.logger.info(
                            f"[INTENT] Low confidence ({confidence:.2f}) or fallback_to_chat requested"
                        )
                except Exception as ie:
                    self.logger.warning(f"Intent classification failed: {ie}")
            
            # Fallback: if no command and classification failed/unavailable, use "help"
            if not command or not command.startswith("/"):
                command = "/help"

            # ── Content library commands ──────────────────────────────────────
            if command == "/generate":
                custom_prompt = input_data.get("custom_prompt")
                category = input_data.get("category", "general_photography").lower()
                level = input_data.get("level")
                user_input = input_data.get("user_input", "")  # For design briefs
                
                # Design categories that require design enhancement
                design_categories = {
                    "design_posters", 
                    "ui_ux_design", 
                    "brand_identity"
                }
                
                # Route design categories to design enhancer agent
                if category in design_categories and user_input:
                    result = await self.agents["design_enhancer"].execute({
                        **input_data,
                        "action": "enhance",
                        "category": category,
                        "user_input": user_input,
                        "brand_context": {"niche": niche, "region": region},
                    })
                elif category in design_categories and custom_prompt and custom_prompt.strip():
                    # Design brief from custom prompt
                    result = await self.agents["design_enhancer"].execute({
                        **input_data,
                        "action": "enhance",
                        "category": category,
                        "user_input": custom_prompt,
                        "brand_context": {"niche": niche, "region": region},
                    })
                elif custom_prompt and custom_prompt.strip() and self._groq_bot:
                    # Custom-concept path: delegate to Groq for AI enhancement
                    ai_result = self._groq_bot.image_generation_prompts(
                        category=category,
                        custom_prompt=custom_prompt,
                        level=level,
                    )
                    # Normalize to the shape the telegram handler expects
                    if ai_result and "error" not in ai_result:
                        raw_prompts = ai_result.get("prompts", [])
                        prompt_strings = [
                            p["prompt"] if isinstance(p, dict) else p
                            for p in raw_prompts
                        ]
                        result = {
                            "status": "success",
                            "category": category,
                            "custom": True,
                            "level": level or "mixed",
                            "count": len(prompt_strings),
                            "prompts": prompt_strings,
                            "meta": get_category_meta(category) or {"emoji": "🎯", "tools": [], "best_for": ""},
                        }
                    else:
                        result = ai_result
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

            # ── Gift Design commands ──────────────────────────────────────────
            elif command == "/design_gift":
                action = input_data.get("action", "generate_concepts")
                
                if action == "list_products":
                    result = await self.agents["gift_design"].execute({
                        **input_data,
                        "action": "list_products",
                    })
                elif action == "list_tones":
                    result = await self.agents["gift_design"].execute({
                        **input_data,
                        "action": "list_tones",
                    })
                elif action == "get_product_specs":
                    result = await self.agents["gift_design"].execute({
                        **input_data,
                        "action": "get_product_specs",
                        "product_type": input_data.get("product_type", ""),
                    })
                else:  # generate_concepts (default)
                    result = await self.agents["gift_design"].execute({
                        **input_data,
                        "action": "generate_concepts",
                        "product_type": input_data.get("product_type", ""),
                        "concept_idea": input_data.get("concept_idea", ""),
                        "brand_colors": input_data.get("brand_colors", []),
                        "tone": input_data.get("tone", ""),
                        "occasion": input_data.get("occasion", ""),
                        "recipient_type": input_data.get("recipient_type", ""),
                    })

            # ── Caption / content generation (Groq direct — no agent covers it) ──
            elif command == "/content":
                if self._groq_bot:
                    result = self._groq_bot.generate_content(
                        topic=input_data.get("topic", ""),
                        style=input_data.get("style", "engaging"),
                        niche=niche,
                        follower_count=follower_count,
                        region=region,
                        language=language,
                        account_stage=account_stage,
                        chat_id=chat_id,
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
                    "niche": niche or input_data.get("niche", "photography"),
                    "region": region,
                })

            # ── Engagement agent (AI strategy) ────────────────────────────────
            elif command == "/engagement":
                result = await self.agents["engagement"].execute({
                    **input_data,
                    "action": "strategy_for_size",
                    "account_size": input_data.get("account_size", "micro"),
                    "niche": niche, "follower_count": follower_count, "region": region,
                })

            # ── Monetization agent (AI ideas) ─────────────────────────────────
            elif command == "/monetize":
                result = await self.agents["monetization"].execute({
                    **input_data,
                    "action": "ideas_for_niche",
                    "niche": niche or input_data.get("niche", "general"),
                    "follower_count": follower_count or input_data.get("follower_count", 10000),
                    "region": region,
                })

            # ── Analytics agent ───────────────────────────────────────────────
            elif command in ("/analytics", "/report", "/stats"):
                result = await self.agents["analytics"].execute({
                    **input_data,
                    "report_type": input_data.get("report_type", "daily"),
                    "niche": niche, "follower_count": follower_count,
                    "account_stage": account_stage, "region": region,
                })

            # ── Help ──────────────────────────────────────────────────────────
            elif command in ("/help", "help"):
                result = self._get_help()

            else:
                # No recognized command at this point
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
            "available_agents": 6,
            "commands": {
                "Content Library": {
                    "commands": ["/generate", "/categories", "/search"],
                    "agent": "ContentGeneratorAgent",
                },
                "Gift Design": {
                    "commands": ["/design_gift"],
                    "agent": "GiftDesignAgent",
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
