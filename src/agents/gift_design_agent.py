"""Gift Design Agent - Generates personalized design concepts for customized gifts"""

from typing import Dict, Any, TYPE_CHECKING
from src.agents.base_agent import BaseAgent
from src.prompts.templates import (
    list_gift_products,
    get_gift_product_meta,
    get_all_tones,
    get_tone_description,
    list_professional_roles,
    get_role_metadata,
    get_role_guidance,
    GIFT_DESIGN_SYSTEM_PROMPT,
)
from src.services.agent_evaluation_integration import EvaluationHookFactory

if TYPE_CHECKING:
    from src.main import InstagramGrowthBot


class GiftDesignAgent(BaseAgent):
    """Transform gift design concepts into comprehensive design briefs + image generation prompts"""

    def __init__(self, groq_bot: "InstagramGrowthBot | None" = None):
        super().__init__("GiftDesign")
        self._groq_bot = groq_bot
        # Cache product types, tones, and roles for quick access
        self.products = list_gift_products()
        self.tones = get_all_tones()
        self.roles = list_professional_roles()
        # Initialize evaluation hook for quality monitoring
        self.eval_hook = EvaluationHookFactory.get_hook("GiftDesignAgent")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution handler for gift design operations"""
        try:
            action = input_data.get("action", "generate_concepts")

            if action == "generate_concepts":
                return await self._generate_design_concepts(input_data)
            elif action == "list_products":
                return await self._list_products(input_data)
            elif action == "list_tones":
                return await self._list_tones(input_data)
            elif action == "get_product_specs":
                return await self._get_product_specs(input_data)
            elif action == "list_roles":
                return await self._list_roles(input_data)
            elif action == "get_role_info":
                return await self._get_role_info(input_data)
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}

        except Exception as e:
            self.logger.error(f"Gift design error: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def _generate_design_concepts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate 3 design concepts with briefs + image prompts for a gift product"""
        try:
            product_type = data.get("product_type", "").lower()
            concept_idea = data.get("concept_idea", "")
            brand_colors = data.get("brand_colors", [])  # List of hex codes
            tone = data.get("tone", "").lower()  # Design tone (minimalist, playful, etc.)
            occasion = data.get("occasion", "").lower()  # birthday, anniversary, etc.
            recipient_type = data.get("recipient_type", "").lower()  # friend, family, etc.
            user_role = data.get("user_role", "").lower()  # Professional role (ui_ux_designer, developer, etc.)
            chat_id = data.get("chat_id")
            niche = data.get("niche", "")

            # Validate product type
            if not product_type:
                return {
                    "status": "error",
                    "message": "product_type is required (e.g., 't_shirt', 'mug', 'hoodie')",
                    "available_products": self.products,
                }

            if product_type not in self.products:
                return {
                    "status": "error",
                    "message": f"Unknown product type: {product_type}",
                    "available_products": self.products,
                }

            # Validate concept idea
            if not concept_idea or len(concept_idea.strip()) < 3:
                return {
                    "status": "error",
                    "message": "concept_idea is required and should be descriptive (min 3 characters)",
                }

            # Get product specs
            product_meta = get_gift_product_meta(product_type)

            # Build personalization context
            personalization = {
                "brand_colors": brand_colors if brand_colors else [],
                "tone": tone if tone in self.tones else "creative",
                "tone_description": get_tone_description(tone) if tone in self.tones else None,
                "occasion": occasion,
                "recipient_type": recipient_type,
                "user_role": user_role if user_role in self.roles else None,
                "user_role_guidance": get_role_guidance(user_role) if user_role in self.roles else None,
                "product_specs": {
                    "printable_area": product_meta.get("printable_area"),
                    "constraints": product_meta.get("constraints"),
                },
            }

            if not self._groq_bot:
                return {
                    "status": "error",
                    "message": "AI bot not initialized. Design concepts require AI generation.",
                }

            # Call Groq to generate design concepts
            ai_result = self._groq_bot.generate_gift_design_concepts(
                product_type=product_type,
                concept_idea=concept_idea,
                personalization=personalization,
                chat_id=chat_id,
                niche=niche,
            )

            if isinstance(ai_result, dict) and "concepts" in ai_result and not ai_result.get("error"):
                result = {
                    "status": "success",
                    "action": "generate_concepts",
                    "product_type": product_type,
                    "product_display_name": product_meta.get("display_name"),
                    "product_emoji": product_meta.get("emoji"),
                    "concept_idea": concept_idea,
                    "personalization": personalization,
                    "concepts": ai_result["concepts"],
                    "concept_count": len(ai_result["concepts"]),
                    "ai_generated": True,
                    "metadata": {
                        "product_tools": product_meta.get("tools", []),
                        "design_tip": ai_result.get("design_tip", ""),
                    },
                }
                await self.log_execution(data, result, "success")
                
                # 🎯 EVALUATE OUTPUT QUALITY
                try:
                    await self.eval_hook.evaluate_execution(
                        user_request=data,
                        agent_output=result,
                        model_used="Groq",
                        system_prompt=GIFT_DESIGN_SYSTEM_PROMPT,
                    )
                except Exception as e:
                    self.logger.warning(f"Quality evaluation skipped: {str(e)}")
                
                return result

            # If AI returns error
            return {
                "status": "error",
                "message": "Gift design concept generation failed",
                "details": ai_result.get("error") if isinstance(ai_result, dict) else str(ai_result),
                "help": "Try again or provide more specific concept details (e.g., 'motivational quote for gym enthusiasts')",
            }

        except Exception as e:
            self.logger.error(f"Design concept generation error: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def _list_products(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """List all available gift product types"""
        try:
            products_info = {}

            for product_type in self.products:
                meta = get_gift_product_meta(product_type)
                products_info[product_type] = {
                    "emoji": meta.get("emoji"),
                    "display_name": meta.get("display_name"),
                    "printable_area": meta.get("printable_area"),
                    "best_for": meta.get("best_for"),
                    "tools": meta.get("tools", []),
                }

            return {
                "status": "success",
                "action": "list_products",
                "products": products_info,
                "total_products": len(self.products),
                "usage": "Use product_type with generate_concepts action",
                "example": {
                    "action": "generate_concepts",
                    "product_type": "t_shirt",
                    "concept_idea": "Motivational quote for gym enthusiasts",
                    "tone": "sporty",
                    "occasion": "personal",
                    "recipient_type": "friend",
                },
            }

        except Exception as e:
            self.logger.error(f"Product list error: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def _list_tones(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """List all available design tones"""
        try:
            tones_info = {}

            for tone in self.tones:
                tones_info[tone] = get_tone_description(tone)

            return {
                "status": "success",
                "action": "list_tones",
                "tones": tones_info,
                "total_tones": len(self.tones),
                "usage": "Use tone with generate_concepts action to guide design style",
                "example_tones": list(self.tones[:3]),
            }

        except Exception as e:
            self.logger.error(f"Tone list error: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def _get_product_specs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed specifications for a product type"""
        try:
            product_type = data.get("product_type", "").lower()

            if not product_type or product_type not in self.products:
                return {
                    "status": "error",
                    "message": f"Unknown product type: {product_type}",
                    "available_products": self.products,
                }

            meta = get_gift_product_meta(product_type)

            return {
                "status": "success",
                "action": "get_product_specs",
                "product_type": product_type,
                "specifications": meta,
            }

        except Exception as e:
            self.logger.error(f"Product specs error: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def _list_roles(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """List all available professional roles"""
        try:
            roles_info = []
            for role_key in self.roles:
                role_meta = get_role_metadata(role_key)
                roles_info.append({
                    "key": role_key,
                    "emoji": role_meta.get("emoji"),
                    "display_name": role_meta.get("display_name"),
                    "expertise": role_meta.get("expertise", []),
                })

            return {
                "status": "success",
                "action": "list_roles",
                "roles": roles_info,
                "total_roles": len(self.roles),
                "usage": "Use user_role with generate_concepts action to personalize designs for specific professionals",
                "example_roles": roles_info[:3] if len(roles_info) > 3 else roles_info,
            }

        except Exception as e:
            self.logger.error(f"Role list error: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def _get_role_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed information for a specific professional role"""
        try:
            role = data.get("user_role", "").lower()

            if not role or role not in self.roles:
                return {
                    "status": "error",
                    "message": f"Unknown role: {role}",
                    "available_roles": self.roles,
                }

            role_meta = get_role_metadata(role)

            return {
                "status": "success",
                "action": "get_role_info",
                "role": role,
                "role_info": role_meta,
                "how_to_use": f"Include user_role='{role}' in your generate_concepts request to get designs tailored for {role_meta.get('display_name')}",
            }

        except Exception as e:
            self.logger.error(f"Role info error: {str(e)}")
            return {"status": "error", "error": str(e)}
