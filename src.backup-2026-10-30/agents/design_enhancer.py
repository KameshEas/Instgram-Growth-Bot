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
        """Generate design prompts via universal AI prompt generator"""
        try:
            user_input = data.get("user_input", "")
            # If clarified, merge clarification into the user input
            if data.get("clarified") and data.get("clarification_answer"):
                try:
                    clar = data.get("clarification_answer")
                    if isinstance(clar, dict):
                        parts = [f"{k}: {v}" for k, v in clar.items()]
                        clarified_text = "; ".join(parts)
                    else:
                        clarified_text = str(clar).strip()
                    if clarified_text:
                        user_input = f"{user_input.strip()} — Clarification: {clarified_text}"
                except Exception:
                    pass

            category = data.get("category", "design_posters").lower()
            niche = data.get("niche", "")
            chat_id = data.get("chat_id")

            if not user_input:
                return {
                    "status": "error",
                    "message": "User input required for design generation"
                }

            if not self._groq_bot:
                return {
                    "status": "error",
                    "message": "AI bot not initialized. Design generation requires AI.",
                }

            # Call universal prompt generator
            ai_result = self._groq_bot.generate_universal_prompts(
                category=category,
                user_idea=user_input,
                niche=niche,
                count=3,
                chat_id=chat_id,
            )

            if isinstance(ai_result, dict) and ai_result.get("status") == "success":
                result = {
                    "status": "success",
                    "action": "enhance",
                    "category": category,
                    "variations": ai_result.get("variations", []),
                    "ai_generated": True,
                    "metadata": {
                        "count": len(ai_result.get("variations", [])),
                    },
                }
                await self.log_execution(data, result, "success")
                return result

            # If AI returns error, pass it through
            error_msg = ai_result.get("error", "Unknown error") if isinstance(ai_result, dict) else str(ai_result)
            self.logger.error(f"AI generation failed: {error_msg}")
            return {"status": "error", "error": error_msg}

        except Exception as e:
            self.logger.error(f"Design generation error: {str(e)}")
            return {"status": "error", "error": str(e)}
