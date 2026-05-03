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

if TYPE_CHECKING:
    from src.main import InstagramGrowthBot


class ContentGeneratorAgent(BaseAgent):
    """Generate viral-optimized image generation prompts"""

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
                    question = await self.edge_case_handler.get_clarifying_question(data)
                except Exception:
                    question = "Could you provide a bit more detail for the request?"
                return {"status": "clarify", "question": question}

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
                # 🎯 PHASE 2A: RECOMMEND OPTIMAL PARAMETERS
                try:
                    recommended_params = self.param_engine.recommend_parameters(
                        product_type="poster",  # Default to poster for general content
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
                    "count": len(ai_result["prompts"]),
                    "prompts": ai_result["prompts"],
                    "ai_generated": True,
                    "recommended_parameters": params_dict,
                    "metadata": {
                        "tip": ai_result.get("tip", ""),
                        "total_in_category": len(ai_result["prompts"]),
                    },
                }
                await self.log_execution(data, result, "success")
                
                # 🎯 EVALUATE OUTPUT QUALITY
                try:
                    await self.eval_hook.evaluate_execution(
                        user_request=data,
                        agent_output=result,
                        model_used="Groq",
                        system_prompt="Generate viral-optimized image generation prompts",
                    )
                except Exception as e:
                    self.logger.warning(f"Quality evaluation skipped: {str(e)}")
                
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
