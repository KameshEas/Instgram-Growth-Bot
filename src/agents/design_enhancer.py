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
                    clar = data.get("clarification_answer")
                    if isinstance(clar, dict):
                        parts = []
                        for k, v in clar.items():
                            parts.append(f"{k}: {v}")
                        clarified_text = "; ".join(parts)
                    else:
                        clarified_text = str(clar).strip()
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
            
            # Call Groq to generate design brief (may return error dict)
            ai_result = self._groq_bot.generate_design_brief(
                category=category,
                user_input=user_input,
                niche=niche,
                brand_context=brand_context,
                chat_id=chat_id,
            )

            def _normalize_brief_item(b: dict) -> dict:
                """Ensure brief fields are strings and color palette is in expected shape"""
                normalized = {}
                text_fields = [
                    "title", "core_message", "visual_style", "typography",
                    "requirements", "key_elements", "composition", "deliverables",
                ]
                for k in text_fields:
                    v = b.get(k, "")
                    if isinstance(v, (dict, list)):
                        try:
                            normalized[k] = json.dumps(v, ensure_ascii=False)
                        except Exception:
                            normalized[k] = str(v)
                    else:
                        normalized[k] = str(v) if v is not None else ""

                # Tools
                tools = b.get("tools", [])
                if isinstance(tools, list):
                    normalized["tools"] = [str(t) for t in tools]
                else:
                    normalized["tools"] = [str(tools)] if tools else []

                # Color palette: expect list of {name, hex}
                palette = b.get("color_palette", [])
                parsed_palette = []
                if isinstance(palette, list):
                    for item in palette:
                        if isinstance(item, dict):
                            name = str(item.get("name", ""))
                            hexv = str(item.get("hex", item.get("color", "")))
                            parsed_palette.append({"name": name, "hex": hexv})
                        else:
                            # If items are strings, attempt to split "Name:#hex" or just hex
                            s = str(item)
                            if ":" in s:
                                n, h = s.split(":", 1)
                                parsed_palette.append({"name": n.strip(), "hex": h.strip()})
                            else:
                                parsed_palette.append({"name": "", "hex": s.strip()})
                normalized["color_palette"] = parsed_palette

                return normalized

            # Helper to create a lightweight fallback brief when AI fails
            def _create_fallback_briefs(n_variations: int = 3):
                briefs = []
                base_title = user_input.strip()[:60] or "Design Brief"
                for i in range(n_variations):
                    briefs.append({
                        "title": f"{base_title} — Variation {i+1}",
                        "core_message": f"{user_input.strip()}",
                        "visual_style": f"{category.replace('_',' ').title()} style, modern, professional",
                        "color_palette": [
                            {"name": "Primary", "hex": "#1f77b4"},
                            {"name": "Accent", "hex": "#ff7f0e"},
                        ],
                        "typography": "Sans-serif headings, readable body text",
                        "requirements": "Deliver print-ready and web-ready assets; include logo variations",
                        "key_elements": "Logo, tagline, hero image, color palette",
                        "composition": "Centered logo with supporting imagery and clear whitespace",
                        "deliverables": "PNG, SVG, PDF; source files (AI/PSD)",
                        "tools": ["Illustrator", "Photoshop"],
                    })
                return briefs

            # If AI returned an error or produced no usable briefs, fallback to deterministic briefs
            briefs_list = []
            try:
                if isinstance(ai_result, dict) and ai_result.get("error"):
                    briefs_list = _create_fallback_briefs(3)
                elif isinstance(ai_result, dict) and "brief" in ai_result:
                    brief_obj = ai_result["brief"]
                    if isinstance(brief_obj, dict) and "briefs" in brief_obj:
                        briefs_list = brief_obj.get("briefs", [])
                    elif isinstance(brief_obj, list):
                        briefs_list = brief_obj
                    elif isinstance(brief_obj, dict):
                        # Convert values that look like briefs
                        for v in brief_obj.values():
                            if isinstance(v, dict):
                                briefs_list.append(v)
                    else:
                        briefs_list = [{
                            "title": "AI Brief",
                            "core_message": str(brief_obj),
                            "visual_style": "",
                            "color_palette": [],
                            "typography": "",
                            "requirements": "",
                            "key_elements": "",
                            "composition": "",
                            "deliverables": "",
                            "tools": [],
                        }]
                elif isinstance(ai_result, dict) and "briefs" in ai_result:
                    briefs_list = ai_result.get("briefs", [])
                else:
                    # Unknown shape or None → create fallback
                    briefs_list = _create_fallback_briefs(3)
            except Exception:
                briefs_list = _create_fallback_briefs(3)

            # Normalize all briefs to expected types/fields
            import json
            normalized_briefs = []
            for b in briefs_list:
                if not isinstance(b, dict):
                    b = {"core_message": str(b)}
                normalized_briefs.append(_normalize_brief_item(b))

            result = {
                "status": "success",
                "action": "enhance",
                "category": category,
                "brief": {"briefs": normalized_briefs},
                "ai_generated": False if isinstance(ai_result, dict) and ai_result.get("error") else True,
                "metadata": {
                    "sections": [b.get("title", f"Brief {i+1}") for i, b in enumerate(normalized_briefs)],
                    "total_sections": len(normalized_briefs),
                },
            }

            await self.log_execution(data, result, "success")
            return result
        
        except Exception as e:
            self.logger.error(f"Design brief generation error: {str(e)}")
            return {"status": "error", "error": str(e)}
