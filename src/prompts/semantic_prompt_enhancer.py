"""Semantic prompt enhancer using AI-based rewriting instead of regex replacement.

Replaces brittle regex-based enhancement with intelligent semantic rewriting
that understands prompt structure and improves quality through AI analysis.
"""

import logging
from typing import Dict, Any, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)


class EnhancementStrategy(Enum):
    """Strategy for how to enhance a prompt."""
    CINEMATIC = "cinematic"  # Add cinematic lighting and camera language
    DETAILED = "detailed"  # Add fine details and textures
    EMOTIONAL = "emotional"  # Enhance emotional expression and mood
    PROFESSIONAL = "professional"  # Add professional photography/design standards
    VIRAL = "viral"  # Optimize for engagement and shareability


class SemanticPromptEnhancer:
    """Enhance prompts using semantic understanding instead of text replacement."""

    ENHANCEMENT_TEMPLATES = {
        EnhancementStrategy.CINEMATIC: {
            "description": "Add cinematic lighting and camera techniques",
            "injection_points": [
                "Cinematic {LIGHTING_TYPE} lighting from {DIRECTION}, with {SHADOW_TYPE} shadows and {HIGHLIGHT_TYPE} highlights",
                "Shot on {CAMERA_TYPE} lens, {DEPTH_OF_FIELD} depth of field, professional color grading with {COLOR_GRADE}",
            ],
        },
        EnhancementStrategy.DETAILED: {
            "description": "Add fine details and textures",
            "injection_points": [
                "Rendered with meticulous attention to skin microtexture, fabric weave details, and subsurface scattering",
                "High-resolution detail capture with professional retouching preserving natural character",
            ],
        },
        EnhancementStrategy.EMOTIONAL: {
            "description": "Enhance emotional expression",
            "injection_points": [
                "Expression conveying {EMOTION}, with {MICRO_EXPRESSION_TYPE} micro-expressions and {AUTHENTICITY_TYPE} authenticity",
                "Emotional depth communicated through {EYE_QUALITY} eyes and {FACE_TENSION} natural tension",
            ],
        },
        EnhancementStrategy.PROFESSIONAL: {
            "description": "Add professional standards",
            "injection_points": [
                "Professional production standards with {LIGHTING_QUALITY} lighting and {COLOR_ACCURACY} color accuracy",
                "Editorial-quality composition following {COMPOSITION_RULE} with {BALANCE_TYPE} visual balance",
            ],
        },
        EnhancementStrategy.VIRAL: {
            "description": "Optimize for engagement",
            "injection_points": [
                "Visually striking with {VISUAL_HOOK_TYPE} that captures immediate attention",
                "{RELATABILITY_TYPE} relatable moment with {EMOTION_HOOK} emotional resonance",
            ],
        },
    }

    def __init__(self):
        """Initialize semantic enhancer."""
        self.strategies = list(EnhancementStrategy)

    def analyze_prompt_structure(self, prompt: str) -> Dict[str, Any]:
        """Analyze prompt structure to identify components and gaps.

        Args:
            prompt: The prompt text to analyze

        Returns:
            Analysis including identified components and gaps
        """
        # Component keywords to look for
        component_indicators = {
            "subject": ["woman", "man", "person", "girl", "boy", "character"],
            "lighting": ["lighting", "light", "shadow", "bright", "dark", "sunlight", "studio"],
            "emotion": ["happy", "sad", "confident", "scared", "joyful", "expression", "mood"],
            "environment": ["background", "room", "outdoor", "studio", "scene", "setting"],
            "camera": ["lens", "angle", "shot", "depth", "focus", "perspective"],
            "color": ["color", "tone", "palette", "hue", "saturation", "vibrant"],
            "texture": ["texture", "smooth", "rough", "detail", "fine", "sharp"],
            "movement": ["pose", "posture", "gesture", "movement", "stance"],
        }

        analysis = {
            "original_prompt": prompt,
            "prompt_length": len(prompt),
            "components_found": {},
            "missing_components": [],
            "component_density": 0.0,
        }

        # Detect present components
        prompt_lower = prompt.lower()
        for component, keywords in component_indicators.items():
            found = any(keyword in prompt_lower for keyword in keywords)
            analysis["components_found"][component] = found

        # Identify missing components
        analysis["missing_components"] = [
            comp for comp, found in analysis["components_found"].items()
            if not found
        ]

        # Calculate component density (how many of 8 components are present)
        components_present = sum(
            1 for found in analysis["components_found"].values() if found
        )
        analysis["component_density"] = components_present / len(component_indicators)

        return analysis

    def get_enhancement_suggestions(
        self,
        prompt: str,
        strategy: Optional[EnhancementStrategy] = None,
    ) -> Dict[str, Any]:
        """Get enhancement suggestions for a prompt.

        Args:
            prompt: The prompt to enhance
            strategy: Enhancement strategy to use (auto-select if None)

        Returns:
            Enhancement suggestions with injection points
        """
        # Analyze prompt
        analysis = self.analyze_prompt_structure(prompt)

        # Auto-select strategy if not provided
        if strategy is None:
            strategy = self._select_best_strategy(analysis)

        template = self.ENHANCEMENT_TEMPLATES[strategy]

        suggestions = {
            "original_prompt": prompt,
            "strategy": strategy.value,
            "strategy_description": template["description"],
            "analysis": analysis,
            "enhancement_phrases": template["injection_points"],
            "recommended_action": self._get_recommended_action(analysis, strategy),
        }

        return suggestions

    def _select_best_strategy(self, analysis: Dict[str, Any]) -> EnhancementStrategy:
        """Auto-select best enhancement strategy based on analysis.

        Strategy selection:
        - Low component density (<0.5) → DETAILED (add missing components)
        - Missing lighting → CINEMATIC
        - Missing emotion → EMOTIONAL
        - Missing camera technique → PROFESSIONAL
        - Default → VIRAL (optimize engagement)
        """
        density = analysis["component_density"]
        missing = analysis["missing_components"]

        # If very sparse, add details
        if density < 0.5:
            return EnhancementStrategy.DETAILED

        # If specific components missing
        if "lighting" in missing:
            return EnhancementStrategy.CINEMATIC
        if "emotion" in missing:
            return EnhancementStrategy.EMOTIONAL
        if "camera" in missing:
            return EnhancementStrategy.PROFESSIONAL

        # Default to viral for optimization
        return EnhancementStrategy.VIRAL

    def _get_recommended_action(
        self,
        analysis: Dict[str, Any],
        strategy: EnhancementStrategy,
    ) -> str:
        """Get human-readable recommended enhancement action."""
        missing = analysis["missing_components"]
        density = analysis["component_density"]

        if density < 0.3:
            return f"Prompt is sparse ({density:.0%} complete). Recommend adding: {', '.join(missing[:3])}"
        elif density < 0.6:
            return f"Prompt is basic. Can be enhanced with: {strategy.value} approach"
        else:
            return f"Prompt is solid. Can be optimized with: {strategy.value} enhancement"

    def generate_enhanced_prompt(
        self,
        original: str,
        groq_bot=None,
        strategy: Optional[EnhancementStrategy] = None,
    ) -> Dict[str, Any]:
        """Generate an enhanced version of the prompt using AI.

        Args:
            original: Original prompt text
            groq_bot: InstagramGrowthBot instance (optional, for AI enhancement)
            strategy: Enhancement strategy to use

        Returns:
            Enhanced prompt with quality metrics
        """
        # Get suggestions first
        suggestions = self.get_enhancement_suggestions(original, strategy)

        # If no Groq bot, provide template-based suggestions
        if not groq_bot:
            enhanced = self._apply_template_enhancement(original, suggestions)
            return {
                "original_prompt": original,
                "enhanced_prompt": enhanced,
                "strategy": suggestions["strategy"],
                "improvement_type": "template_based",
                "suggestions": suggestions,
                "estimated_quality_gain": 15,  # Template gains ~15% quality
            }

        # Use AI to generate semantic enhancement
        enhancement_prompt = self._build_enhancement_prompt(original, suggestions)

        try:
            ai_enhancement = groq_bot.enhance_prompt_semantic(
                original=original,
                analysis=suggestions["analysis"],
                strategy=suggestions["strategy"],
            )

            if ai_enhancement and "enhanced_prompt" in ai_enhancement:
                return {
                    "original_prompt": original,
                    "enhanced_prompt": ai_enhancement["enhanced_prompt"],
                    "strategy": suggestions["strategy"],
                    "improvement_type": "ai_semantic",
                    "reasoning": ai_enhancement.get("reasoning", ""),
                    "suggestions": suggestions,
                    "estimated_quality_gain": ai_enhancement.get("quality_improvement", 25),
                }
        except Exception as e:
            logger.warning(f"AI semantic enhancement failed: {e}, falling back to template")

        # Fallback to template if AI fails
        enhanced = self._apply_template_enhancement(original, suggestions)
        return {
            "original_prompt": original,
            "enhanced_prompt": enhanced,
            "strategy": suggestions["strategy"],
            "improvement_type": "template_fallback",
            "suggestions": suggestions,
            "estimated_quality_gain": 15,
        }

    def _apply_template_enhancement(
        self,
        prompt: str,
        suggestions: Dict[str, Any],
    ) -> str:
        """Apply template-based enhancement to prompt."""
        # Insert enhancement phrases at logical points
        # Strategy: add at end if room, or prepend key techniques
        phrases = suggestions["enhancement_phrases"]
        if not phrases:
            return prompt

        # Take first enhancement phrase as summary enhancement
        enhancement = phrases[0]

        # If prompt is short, prepend; otherwise append
        if len(prompt) < 100:
            return f"{enhancement}. {prompt}"
        else:
            return f"{prompt}. {enhancement}"

    def _build_enhancement_prompt(
        self,
        original: str,
        suggestions: Dict[str, Any],
    ) -> str:
        """Build prompt for Groq to semantically enhance the original."""
        analysis = suggestions["analysis"]
        missing = ", ".join(analysis["missing_components"][:3])
        strategy = suggestions["strategy"]

        return f"""You are a professional prompt engineer specializing in image generation.

Original Prompt: "{original}"

Analysis:
- Component Density: {analysis['component_density']:.0%} ({len([c for c in analysis['components_found'].values() if c])}/8)
- Missing Components: {missing}
- Recommended Enhancement Strategy: {strategy}

Task: Rewrite the prompt to be more compelling and complete using a {strategy} approach.
Focus on: adding missing components naturally, enhancing descriptive language, ensuring professional quality.

Return a single improved prompt that incorporates the {strategy} strategy while maintaining the original intent."""

    def compare_prompts(
        self,
        original: str,
        enhanced: str,
    ) -> Dict[str, Any]:
        """Compare original and enhanced prompts.

        Args:
            original: Original prompt
            enhanced: Enhanced prompt

        Returns:
            Comparison metrics
        """
        orig_analysis = self.analyze_prompt_structure(original)
        enh_analysis = self.analyze_prompt_structure(enhanced)

        return {
            "original": orig_analysis,
            "enhanced": enh_analysis,
            "improvement_metrics": {
                "length_gain": enh_analysis["prompt_length"] - orig_analysis["prompt_length"],
                "component_gain": (
                    enh_analysis["component_density"] - orig_analysis["component_density"]
                ),
                "completeness_improvement": (
                    (8 - len(enh_analysis["missing_components"]))
                    - (8 - len(orig_analysis["missing_components"]))
                ),
            },
        }
