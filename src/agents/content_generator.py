from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent
from src.prompts.templates import get_category_prompts, list_categories
import random

class ContentGeneratorAgent(BaseAgent):
    """Generate viral-optimized image generation prompts"""
    
    def __init__(self):
        super().__init__("ContentGenerator")
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
        """Generate prompts from library by category"""
        try:
            category = data.get("category", "general_photography").lower()
            count = data.get("count", 3)
            
            # Get prompts for category
            prompts = get_category_prompts(category)
            
            if not prompts:
                return {
                    "status": "error",
                    "message": f"Category '{category}' not found",
                    "available_categories": self.categories,
                    "help": "Use action='list_categories' to see all available categories"
                }
            
            # Return random selection of prompts
            selected_prompts = random.sample(prompts, min(count, len(prompts)))
            
            result = {
                "status": "success",
                "action": "generate",
                "category": category,
                "count": len(selected_prompts),
                "prompts": selected_prompts,
                "metadata": {
                    "total_in_category": len(prompts),
                    "tip": "Copy any prompt and use with DALL-E 3, Midjourney, or Stable Diffusion",
                    "quality_modifiers": "8k, ultra HD, professional photography, highly detailed, sharp focus, masterpiece"
                }
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
