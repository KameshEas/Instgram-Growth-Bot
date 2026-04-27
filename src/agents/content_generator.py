from typing import Dict, Any, List, TYPE_CHECKING
from src.agents.base_agent import BaseAgent
from src.prompts.templates import get_category_prompts, list_categories
import random

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
        """Generate prompts — AI-generated when groq_bot available, static library fallback otherwise."""
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

            # ── AI prompt generation (primary path when groq_bot available) ──
            if self._groq_bot:
                try:
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
                except Exception as e:
                    self.logger.warning(f"AI prompt generation failed, falling back to library: {e}")

            # ── Static library fallback ───────────────────────────────────────
            prompts = get_category_prompts(category)

            if not prompts:
                return {
                    "status": "error",
                    "message": f"Category '{category}' not found",
                    "available_categories": self.categories,
                    "help": "Use action='list_categories' to see all available categories",
                }

            selected_prompts = random.sample(prompts, min(count, len(prompts)))

            result = {
                "status": "success",
                "action": "generate",
                "category": category,
                "count": len(selected_prompts),
                "prompts": selected_prompts,
                "ai_generated": False,
                "metadata": {
                    "total_in_category": len(prompts),
                    "tip": "Copy any prompt and use with DALL-E 3, Midjourney, or Stable Diffusion",
                },
            }

            await self.log_execution(data, result, "success")
            return result

        except Exception as e:
            self.logger.error(f"Prompt generation error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _list_all_categories(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """List all available prompt categories"""
        try:
            categories_info = {}
            
            for category in self.categories:
                prompts = get_category_prompts(category)
                categories_info[category] = {
                    "count": len(prompts),
                    "friendly_name": category.replace("_", " ").title()
                }
            
            return {
                "status": "success",
                "action": "list_categories",
                "categories": categories_info,
                "total_categories": len(self.categories),
                "usage": "Use action='generate' with category parameter to get prompts",
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
        """Search for categories by keyword"""
        try:
            keyword = data.get("keyword", "").lower()
            
            if not keyword:
                return {"status": "error", "message": "Keyword parameter required"}
            
            # Find matching categories
            matching = [cat for cat in self.categories if keyword in cat.lower()]
            
            results = {}
            for category in matching:
                prompts = get_category_prompts(category)
                results[category] = {
                    "count": len(prompts),
                    "friendly_name": category.replace("_", " ").title()
                }
            
            return {
                "status": "success",
                "action": "search",
                "keyword": keyword,
                "matches_found": len(matching),
                "results": results,
                "usage": "Use action='generate' with any category to get prompts"
            }
        
        except Exception as e:
            self.logger.error(f"Search error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def get_quick_prompts(self, category: str, count: int = 3) -> List[str]:
        """Synchronous method to get prompts quickly"""
        prompts = get_category_prompts(category)
        if not prompts:
            return []
        return random.sample(prompts, min(count, len(prompts)))
