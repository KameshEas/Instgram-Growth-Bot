from typing import Dict, Any, List, TYPE_CHECKING
from src.agents.base_agent import BaseAgent
from src.prompts.templates import list_categories
from src.services.agent_evaluation_integration import EvaluationHookFactory
from src.services.parameter_recommendation_engine import ParameterRecommendationFactory
from src.services.image_alignment_validator import ImageAlignmentValidatorFactory
from src.services.input_validator import InputValidatorFactory
from src.services.conflict_resolver import ConflictResolverFactory
from src.services.edge_case_handler import EdgeCaseHandlerFactory
from src.services.error_recovery_system import ErrorRecoverySystemFactory, ErrorType
from src.prompts.preference_generator import PreferenceGenerator

if TYPE_CHECKING:
    from src.main import InstagramGrowthBot


class ContentGeneratorAgent(BaseAgent):
    """Generate viral-optimized image generation prompts"""

    # Map categories to optimal ProductType for parameter recommendation
    CATEGORY_TO_PRODUCT_TYPE = {
        # Photography categories - use "poster" for general photos, "canvas" for fine art
        "general_photography": "poster",
        "women_professional": "canvas",
        "men_professional": "canvas",
        "women_transform": "canvas",
        "men_transform": "canvas",
        "couples_general": "canvas",
        "couples_transform": "canvas",
        "photography_styles": "canvas",
        # Design categories
        "design_posters": "poster",
        "design_gifts": "merchandise",
        "print_design": "poster",
        # Logo & branding - high reference preservation
        "logo_create": "merchandise",
        "brand_identity": "merchandise",
        # Product & UI design
        "product_3d": "merchandise",
        "ui_ux_design": "poster",
        # Creative categories
        "illustration_art": "canvas",
        "animation_motion": "poster",
        # Text content (fallback)
        "reel_scripts": "poster",
        "captions_templates": "poster",
        "email_subjects": "poster",
    }

    def __init__(self, groq_bot: "InstagramGrowthBot | None" = None):
        super().__init__("ContentGenerator")
        self._groq_bot = groq_bot
        # Cache categories for quick access
        self.categories = list_categories()
        # Initialize evaluation hook for quality monitoring
        self.eval_hook = EvaluationHookFactory.get_hook("ContentGeneratorAgent")
        # Initialize Phase 2A components
        self.param_engine = ParameterRecommendationFactory.get_engine()
        self.alignment_validator = ImageAlignmentValidatorFactory.get_validator()
        # Initialize Phase 2C components
        self.input_validator = InputValidatorFactory.get_validator()
        self.conflict_resolver = ConflictResolverFactory.get_resolver()
        self.edge_case_handler = EdgeCaseHandlerFactory.get_handler()
        self.error_recovery = ErrorRecoverySystemFactory.get_system()
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content prompts based on category"""
        try:
            # 🔴 PHASE 2C STEP 1: Validate input
            validation_result = await self.input_validator.validate_content_input(input_data)
            if validation_result.status.value == "fail":
                self.logger.warning(f"Input validation failed: {validation_result}")
                if validation_result.corrected_data:
                    input_data = validation_result.corrected_data
                    self.logger.info("Using corrected input data")
                else:
                    return {
                        "status": "error",
                        "message": "Input validation failed",
                        "issues": [str(issue) for issue in validation_result.issues]
                    }
            
            # 🔴 PHASE 2C STEP 2: Resolve conflicts
            conflict_result = await self.conflict_resolver.resolve_conflicts(input_data)
            if conflict_result.has_conflicts():
                self.logger.warning(f"Input conflicts detected: {len(conflict_result.conflicts_detected)}")
                if conflict_result.resolved_data:
                    input_data = conflict_result.resolved_data
            
            # 🔴 PHASE 2C STEP 3: Handle edge cases
            edge_result = await self.edge_case_handler.handle_content_input(input_data)
            if edge_result.has_alerts():
                self.logger.warning(f"Edge cases detected: {len(edge_result.alerts)}")
                if edge_result.corrected_data:
                    input_data = edge_result.corrected_data
            
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
            # 🔴 PHASE 2C: Attempt error recovery
            try:
                recovery_result = await self.error_recovery.handle_error(
                    error=e,
                    error_type=ErrorType.PROCESSING_ERROR,
                    context={"action": input_data.get("action")}
                )
                self.logger.info(f"Error recovery attempted: {recovery_result.recovery_successful}")
            except Exception as recovery_err:
                self.logger.error(f"Error recovery failed: {str(recovery_err)}")
            
            return {"status": "error", "error": str(e)}
    
    async def _generate_prompts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate prompts via AI only — no static library or hardcoded fallbacks."""
        try:
            # If input appears ambiguous, ask for a clarification before generating
            try:
                ambiguous = await self.edge_case_handler.is_ambiguous(data)
            except Exception:
                ambiguous = False
            if ambiguous and not data.get("clarified"):
                try:
                    question_obj = await self.edge_case_handler.get_clarifying_question(data)
                except Exception:
                    question_obj = {"question": "Could you provide a bit more detail for the request?", "fields": ["subject", "colors", "mood"]}
                if isinstance(question_obj, dict):
                    return {"status": "clarify", "question": question_obj.get("question"), "clarify_fields": question_obj.get("fields", [])}
                else:
                    return {"status": "clarify", "question": str(question_obj)}

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

            # Extract aesthetic preferences from input data
            aesthetic_preferences = PreferenceGenerator.extract_from_dict(data)
            user_context_safe = self._build_user_context(data)

            # Extract structured payloads (e.g., logo components) for reference_context
            reference_context = ""
            if data.get("components"):
                # Format structured components dict for LLM (never truncate this)
                components = data["components"]
                components_lines = []
                for k, v in components.items():
                    components_lines.append(f"{k.replace('_', ' ').title()}: {v}")
                reference_context = "STRUCTURAL REQUIREMENTS:\n" + "\n".join(components_lines)

            # For transformation categories with custom requirement, build extra context (IDENTITY-LOCK)
            extra_context = ""
            if category in {"women_transform", "men_transform", "couples_transform"} and user_context_safe:
                from src.prompts.custom_scenario_parser import CustomScenarioParser
                from src.prompts.scene_styling_cohesion import SceneStylingCohesion

                location, mood = CustomScenarioParser.extract_location(user_context_safe)
                custom_scenario_section = CustomScenarioParser.build_custom_scenario_section(
                    location, mood, user_context_safe, count
                )
                styling_section = SceneStylingCohesion.build_styling_prompt_section(
                    location=location,
                    mood=mood,
                    user_context=user_context_safe,
                    blend_level=aesthetic_preferences.blend_level.value if aesthetic_preferences else "50/50",
                    jewelry_style=aesthetic_preferences.jewelry_style.value if aesthetic_preferences else "fusion",
                )
                extra_context = f"{custom_scenario_section}\n\n{styling_section}"
            # For all other categories, inject dynamic context guidance (NICHE-DYNAMIC)
            else:
                from src.prompts.dynamic_context_builder import DynamicContextBuilder
                extra_context = DynamicContextBuilder.build_category_guidance(
                    category=category,
                    niche=niche,
                    user_idea=user_context_safe,
                )

            ai_result = self._groq_bot.generate_universal_prompts(
                category=category,
                user_idea=user_context_safe,
                niche=niche,
                count=count,
                chat_id=data.get("chat_id"),
                extra_context=extra_context,
                reference_context=reference_context,
                aesthetic_preferences=aesthetic_preferences,
            )

            if isinstance(ai_result, dict) and "variations" in ai_result and not ai_result.get("error"):
                # 🎯 PHASE 2A: RECOMMEND OPTIMAL PARAMETERS
                try:
                    # Map category to optimal product type for parameter tuning
                    product_type = self.CATEGORY_TO_PRODUCT_TYPE.get(category, "poster")
                    recommended_params = self.param_engine.recommend_parameters(
                        product_type=product_type,
                        alignment_importance=0.75,
                        quality_level="balanced",
                    )
                    params_dict = {
                        "cfg_scale": recommended_params.cfg_scale,
                        "denoising_strength": recommended_params.denoising_strength,
                        "num_steps": recommended_params.num_steps,
                        "preset_name": recommended_params.preset_name,
                        "reasoning": recommended_params.reasoning,
                    }
                except Exception as e:
                    self.logger.warning(f"Parameter recommendation failed: {str(e)}")
                    params_dict = {}

                result = {
                    "status": "success",
                    "action": "generate",
                    "category": category,
                    "count": len(ai_result["variations"]),
                    "variations": ai_result["variations"],
                    "ai_generated": True,
                    "recommended_parameters": params_dict,
                    "metadata": {
                        "total_in_category": len(ai_result["variations"]),
                    },
                }
                await self.log_execution(data, result, "success")

                # 🎯 EVALUATE OUTPUT QUALITY
                try:
                    await self.eval_hook.evaluate_execution(
                        user_request=data,
                        agent_output=result,
                        model_used="Groq",
                        system_prompt="Generate optimized AI prompts",
                    )
                except Exception as e:
                    self.logger.warning(f"Quality evaluation skipped: {str(e)}")

                return result
            
            # If AI returns error - provide better error message
            error_msg = ai_result.get("error") if isinstance(ai_result, dict) else str(ai_result)

            # More specific error handling
            if "parse" in error_msg.lower():
                help_text = "The AI response couldn't be parsed. Try simplifying your request or try again in a moment."
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

    def _build_user_context(self, data: Dict[str, Any], exclude_keys: List[str] = None) -> str:
        """Build user_context string for AI from input data, excluding structured payloads.

        Args:
            data: Input data dict
            exclude_keys: Keys to exclude (e.g., ['components'] to extract separately via reference_context)

        Returns:
            Context string with increased budget (1500 chars) and warning if truncation occurs
        """
        if exclude_keys is None:
            exclude_keys = []

        try:
            base = {k: v for k, v in data.items() if k not in ("action", "chat_id", "components", "clarified") + tuple(exclude_keys)}
            clar = data.get("clarification_answer")
            if clar:
                if isinstance(clar, dict):
                    base.update(clar)
                else:
                    base["clarification"] = str(clar)
            # Convert to a compact string with larger budget (1500 chars, not 500)
            items = [f"{k}={v}" for k, v in base.items() if v is not None]
            context_str = "; ".join(items)
            # Log warning if truncation occurs (should be rare with 1500-char budget)
            if len(context_str) > 1500:
                self.logger.warning(f"User context truncated from {len(context_str)} to 1500 chars")
                context_str = context_str[:1500]
            return context_str
        except Exception as e:
            self.logger.error(f"Error building user context: {e}")
            return str({k: v for k, v in data.items() if k not in ("action", "chat_id", "components")})
    
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
