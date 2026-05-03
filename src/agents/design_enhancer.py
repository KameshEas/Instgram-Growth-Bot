"""Design Brief Enhancement Agent - Transforms user input into structured design briefs"""

from typing import Dict, Any, TYPE_CHECKING
from src.agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from src.main import InstagramGrowthBot


class DesignPromptEnhancerAgent(BaseAgent):
    """Transform user design concepts into comprehensive design briefs with specifications"""

    def __init__(self, groq_bot: "InstagramGrowthBot | None" = None):
        super().__init__("DesignPromptEnhancer")
        self._groq_bot = groq_bot
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate design brief from user input"""
        try:
            action = input_data.get("action", "enhance")
            
            if action == "enhance":
                return await self._generate_design_brief(input_data)
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
            
        except Exception as e:
            self.logger.error(f"Design enhancement error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _generate_design_brief(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured design brief via AI"""
        try:
            user_input = data.get("user_input", "")
            # If clarified, merge clarification into the user input to preserve user's extra detail
            if data.get("clarified") and data.get("clarification_answer"):
                try:
                    clarified_text = str(data.get("clarification_answer")).strip()
                    if clarified_text:
                        user_input = f"{user_input.strip()} — Clarification: {clarified_text}"
                except Exception:
                    pass
            category = data.get("category", "design_posters").lower()
            niche = data.get("niche", "")
            brand_context = data.get("brand_context", {})
            chat_id = data.get("chat_id")
            
            if not user_input:
                return {
                    "status": "error",
                    "message": "User input required for design brief enhancement"
                }
            
            if not self._groq_bot:
                return {
                    "status": "error",
                    "message": "AI bot not initialized. Design briefs require AI generation.",
                }
            
            # Call Groq to generate design brief
            ai_result = self._groq_bot.generate_design_brief(
                category=category,
                user_input=user_input,
                niche=niche,
                brand_context=brand_context,
                chat_id=chat_id,
            )
            
            if isinstance(ai_result, dict) and "brief" in ai_result and not ai_result.get("error"):
                result = {
                    "status": "success",
                    "action": "enhance",
                    "category": category,
                    "brief": ai_result["brief"],
                    "ai_generated": True,
                    "metadata": {
                        "sections": ai_result.get("sections", []),
                        "total_sections": ai_result.get("total_sections", 0),
                    },
                }
                await self.log_execution(data, result, "success")
                return result
            
            # If AI returns error
            return {
                "status": "error",
                "message": "Design brief generation failed",
                "details": ai_result.get("error") if isinstance(ai_result, dict) else str(ai_result),
                "help": "Try again in a moment or provide more detailed design information.",
            }
        
        except Exception as e:
            self.logger.error(f"Design brief generation error: {str(e)}")
            return {"status": "error", "error": str(e)}
