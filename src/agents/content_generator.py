from typing import Dict, Any, List, TYPE_CHECKING
from src.agents.base_agent import BaseAgent
from src.prompts.templates import list_categories

if TYPE_CHECKING:
    from src.main import InstagramGrowthBot


class ContentGeneratorAgent(BaseAgent):
    """Generate viral-optimized image generation prompts"""

    def __init__(self, groq_bot: "InstagramGrowthBot | None" = None):
        super().__init__("ContentGenerator")
        self._groq_bot = groq_bot
        # Cache categories for quick access
        self.categories = list_categories()
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content prompts based on category"""
        try:
            action = input_data.get("action", "generate")
            
            if action == "generate":
                return await self._generate_prompts(input_data)
            elif action == "list_categories":
                return await self._list_all_categories(input_data)
            elif action == "search":
                return await self._search_category(input_data)
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
            
        except Exception as e:
            self.logger.error(f"Content generation error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _generate_prompts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate prompts via AI only — no static library or hardcoded fallbacks."""
        try:
            requested_category = data.get("category", "").lower()
            count = data.get("count", 3)
            niche = data.get("niche", "")
            goal = data.get("goal", "")

            # AI selects best category when no explicit category supplied
            category = requested_category
            if not category and self._groq_bot and (niche or goal or data):
                try:
                    ai_pick = self._groq_bot.suggest_content_category(
                        user_context=str(data),
                        available_categories=self.categories,
                        niche=niche,
                        goal=goal,
                    )
                    if isinstance(ai_pick, dict) and ai_pick.get("suggested_category"):
                        category = ai_pick["suggested_category"].lower()
                except Exception as e:
                    self.logger.warning(f"AI category suggestion failed: {e}")

            if not category:
                category = "general_photography"

            # ── AI prompt generation (only source) ──
            if not self._groq_bot:
                return {
                    "status": "error",
                    "message": "AI bot not initialized. Prompts must be generated via AI only.",
                }

            ai_result = self._groq_bot.generate_image_prompts(
                category=category,
                niche=niche,
                count=count,
                user_context=str({k: v for k, v in data.items() if k not in ("action", "chat_id")}),
                chat_id=data.get("chat_id"),
            )
            
            if isinstance(ai_result, dict) and "prompts" in ai_result and not ai_result.get("error"):
                result = {
                    "status": "success",
                    "action": "generate",
                    "category": category,
                    "count": len(ai_result["prompts"]),
                    "prompts": ai_result["prompts"],
                    "ai_generated": True,
                    "metadata": {
                        "tip": ai_result.get("tip", ""),
                        "total_in_category": len(ai_result["prompts"]),
                    },
                }
                await self.log_execution(data, result, "success")
                return result
            
            # If AI returns error - provide better error message
            error_msg = ai_result.get("error") if isinstance(ai_result, dict) else str(ai_result)
            
            # More specific error handling
            if "parse" in error_msg.lower():
                help_text = "The AI response couldn't be parsed. Try simplifying your custom prompt or try again in a moment."
            else:
                help_text = "Try again in a moment or provide more context (niche, goal, etc.)"
            
            return {
                "status": "error",
                "message": f"AI prompt generation failed",
                "details": error_msg,
                "help": help_text,
            }

        except Exception as e:
            self.logger.error(f"Prompt generation error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _list_all_categories(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """List all available prompt categories for AI generation."""
        try:
            categories_info = {}
            
            for category in self.categories:
                categories_info[category] = {
                    "friendly_name": category.replace("_", " ").title(),
                    "ai_generated": True,
                }
            
            return {
                "status": "success",
                "action": "list_categories",
                "categories": categories_info,
                "total_categories": len(self.categories),
                "note": "All prompts are generated via AI for this category",
                "usage": "Use action='generate' with category parameter to get AI-generated prompts",
                "example": {
                    "action": "generate",
                    "category": "women_professional",
                    "count": 3
                }
            }
        
        except Exception as e:
            self.logger.error(f"Category list error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _search_category(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Search for categories by keyword (AI-generated prompts available)."""
        try:
            keyword = data.get("keyword", "").lower()
            
            if not keyword:
                return {"status": "error", "message": "Keyword parameter required"}
            
            # Find matching categories
            matching = [cat for cat in self.categories if keyword in cat.lower()]
            
            results = {}
            for category in matching:
                results[category] = {
                    "friendly_name": category.replace("_", " ").title(),
                    "ai_generated": True,
                }
            
            return {
                "status": "success",
                "action": "search",
                "keyword": keyword,
                "matches_found": len(matching),
                "results": results,
                "note": "All prompts are generated via AI",
                "usage": "Use action='generate' with any category to get AI-generated prompts"
            }
        
        except Exception as e:
            self.logger.error(f"Search error: {str(e)}")
            return {"status": "error", "error": str(e)}
