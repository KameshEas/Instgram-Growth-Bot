"""
Parameter Recommendation Engine
Recommends optimal image generation parameters (CFG, denoising, steps) based on context
"""

import logging
import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class ProductType(Enum):
    """Product types for parameter optimization"""
    T_SHIRT = "t-shirt"
    MUG = "mug"
    CANVAS = "canvas"
    POSTER = "poster"
    MERCHANDISE = "merchandise"


class QualityLevel(Enum):
    """Quality levels for generation speed/quality tradeoff"""
    QUICK = "quick"           # Fast preview
    BALANCED = "balanced"     # Default
    HIGH = "high"             # High quality


@dataclass
class ParameterSet:
    """Recommended parameter values"""
    cfg_scale: float
    denoising_strength: float
    num_steps: int
    preset_name: str
    reasoning: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for use in image generation"""
        return {
            "cfg_scale": self.cfg_scale,
            "denoising_strength": self.denoising_strength,
            "num_steps": self.num_steps
        }


@dataclass
class ParameterPreset:
    """A parameter preset with metadata"""
    name: str
    cfg_scale: float
    denoising_strength: float
    num_steps: int
    quality_score: float  # Expected quality (1-10)
    alignment_score: float  # Expected alignment (1-10)
    use_cases: list  # When to use
    

class ParameterRecommendationEngine:
    """
    Recommends optimal parameters for image generation based on context.
    
    Parameters analyzed:
    - CFG Scale (7-20): Guidance strength
      - Low (7-9): Creative, may ignore input
      - Medium (10-12): Balanced
      - High (15-20): Strong adherence to prompt
    
    - Denoising Strength (0.0-1.0): Reference preservation
      - Low (0.4-0.6): Subtle changes only
      - Medium (0.65-0.75): Moderate transformation
      - High (0.85-1.0): Major transformation
    
    - Num Steps (20-100): Quality vs speed
      - 20-30: Quick preview
      - 40-50: Good reference preservation
      - 70-100: High quality output
    """
    
    def __init__(self):
        """Initialize with presets from Phase 1C analysis"""
        self.presets = self._build_presets()
        self.product_type_recommendations = self._build_product_recommendations()
        logger.info("ParameterRecommendationEngine initialized")
    
    def _build_presets(self) -> Dict[str, ParameterPreset]:
        """Build parameter presets from Phase 1C findings"""
        return {
            "high_quality": ParameterPreset(
                name="High Quality",
                cfg_scale=15.0,
                denoising_strength=0.85,
                num_steps=100,
                quality_score=9.5,
                alignment_score=7.5,
                use_cases=["final_render", "showcase", "high_value_product"]
            ),
            "balanced": ParameterPreset(
                name="Balanced",
                cfg_scale=12.0,
                denoising_strength=0.75,
                num_steps=70,
                quality_score=8.5,
                alignment_score=7.0,
                use_cases=["default", "general_use", "most_products"]
            ),
            "quick_preview": ParameterPreset(
                name="Quick Preview",
                cfg_scale=9.0,
                denoising_strength=0.6,
                num_steps=30,
                quality_score=6.5,
                alignment_score=5.5,
                use_cases=["iteration", "rapid_testing", "draft"]
            ),
            "reference_preservation": ParameterPreset(
                name="Reference Preservation",
                cfg_scale=10.0,
                denoising_strength=0.65,
                num_steps=50,
                quality_score=8.0,
                alignment_score=8.5,
                use_cases=["mockup_based", "logo_preservation", "brand_consistency"]
            ),
            "subtle_enhancement": ParameterPreset(
                name="Subtle Enhancement",
                cfg_scale=8.0,
                denoising_strength=0.5,
                num_steps=40,
                quality_score=7.5,
                alignment_score=9.0,
                use_cases=["minor_tweaks", "slight_changes", "preserve_original"]
            )
        }
    
    def _build_product_recommendations(self) -> Dict[str, str]:
        """Product type → recommended preset mapping"""
        return {
            ProductType.T_SHIRT.value: "balanced",
            ProductType.MUG.value: "high_quality",
            ProductType.CANVAS.value: "balanced",
            ProductType.POSTER.value: "balanced",
            ProductType.MERCHANDISE.value: "reference_preservation"
        }
    
    def recommend_parameters(
        self,
        product_type: str = "t-shirt",
        alignment_importance: float = 0.5,  # 0.0-1.0, importance of preserving reference
        quality_level: str = "balanced",     # "quick", "balanced", "high"
        design_complexity: str = "moderate", # "simple", "moderate", "complex"
        is_first_generation: bool = True,   # First attempt or iteration?
        user_request_specificity: float = 0.5,  # 0.0-1.0, how specific is user input?
    ) -> ParameterSet:
        """
        Recommend parameters based on context.
        
        Args:
            product_type: Type of product ("t-shirt", "mug", etc.)
            alignment_importance: How important is preserving input features (0.0-1.0)
            quality_level: Speed/quality tradeoff ("quick", "balanced", "high")
            design_complexity: Design complexity level
            is_first_generation: First attempt or refinement iteration?
            user_request_specificity: How specific is user request (0.0-1.0)?
        
        Returns:
            ParameterSet with recommended parameters
        
        Examples:
            >>> engine.recommend_parameters(
            ...     product_type="mug",
            ...     alignment_importance=0.9,
            ...     quality_level="high"
            ... )
            ParameterSet(cfg_scale=15.0, denoising_strength=0.85, num_steps=100, ...)
        """
        
        # Normalize inputs
        product_type = product_type.lower()
        quality_level = quality_level.lower()
        design_complexity = design_complexity.lower()
        
        # Validate inputs
        alignment_importance = max(0.0, min(1.0, alignment_importance))
        user_request_specificity = max(0.0, min(1.0, user_request_specificity))
        
        # Start with product-type default preset
        base_preset_key = self.product_type_recommendations.get(
            product_type, 
            "balanced"
        )
        base_preset = self.presets[base_preset_key]
        
        # Adjust based on quality level
        if quality_level == "quick":
            selected_preset = self.presets["quick_preview"]
            reasoning = "Quality level: Quick preview mode"
        elif quality_level == "high":
            selected_preset = self.presets["high_quality"]
            reasoning = "Quality level: High quality mode"
        else:  # balanced
            selected_preset = base_preset
            reasoning = f"Quality level: Balanced (default for {product_type})"
        
        # Adjust for alignment importance (very important = preserve reference)
        if alignment_importance > 0.75:
            # High alignment importance: use reference preservation
            if selected_preset.name != "Reference Preservation":
                # Blend towards reference preservation
                cfg_blend = 0.7 * selected_preset.cfg_scale + 0.3 * self.presets["reference_preservation"].cfg_scale
                denoise_blend = 0.7 * selected_preset.denoising_strength + 0.3 * self.presets["reference_preservation"].denoising_strength
                
                return ParameterSet(
                    cfg_scale=cfg_blend,
                    denoising_strength=denoise_blend,
                    num_steps=selected_preset.num_steps,
                    preset_name=f"{selected_preset.name} (alignment-tuned)",
                    reasoning=f"High alignment importance ({alignment_importance:.1f}) - prioritizing reference preservation"
                )
        
        elif alignment_importance < 0.25:
            # Low alignment importance: allow more creative freedom
            if selected_preset.name != "Subtle Enhancement":
                # Use higher CFG for more prompt adherence
                cfg_adjusted = min(selected_preset.cfg_scale + 2, 20.0)
                denoise_adjusted = min(selected_preset.denoising_strength + 0.1, 1.0)
                
                return ParameterSet(
                    cfg_scale=cfg_adjusted,
                    denoising_strength=denoise_adjusted,
                    num_steps=selected_preset.num_steps,
                    preset_name=f"{selected_preset.name} (creative-tuned)",
                    reasoning=f"Low alignment importance ({alignment_importance:.1f}) - allowing creative freedom"
                )
        
        # First generation vs iteration
        if not is_first_generation and design_complexity == "complex":
            # For iterative refinement of complex designs, use subtle changes
            selected_preset = self.presets["subtle_enhancement"]
            reasoning += " | Iteration on complex design: subtle enhancement"
        
        # Vague input → lower quality to save time
        if user_request_specificity < 0.3:
            selected_preset = self.presets["quick_preview"]
            reasoning = f"Vague input (specificity {user_request_specificity:.1f}) - quick preview"
        
        logger.info(
            f"Recommended parameters for {product_type}: "
            f"CFG={selected_preset.cfg_scale}, "
            f"Denoise={selected_preset.denoising_strength}, "
            f"Steps={selected_preset.num_steps} "
            f"({selected_preset.name})"
        )
        
        return ParameterSet(
            cfg_scale=selected_preset.cfg_scale,
            denoising_strength=selected_preset.denoising_strength,
            num_steps=selected_preset.num_steps,
            preset_name=selected_preset.name,
            reasoning=reasoning
        )
    
    def get_preset_by_name(self, preset_name: str) -> Optional[ParameterPreset]:
        """Get preset by name"""
        key = preset_name.lower().replace(" ", "_")
        return self.presets.get(key)
    
    def list_presets(self) -> Dict[str, Dict]:
        """List all available presets"""
        return {
            name: {
                "cfg_scale": preset.cfg_scale,
                "denoising_strength": preset.denoising_strength,
                "num_steps": preset.num_steps,
                "quality_score": preset.quality_score,
                "alignment_score": preset.alignment_score,
                "use_cases": preset.use_cases
            }
            for name, preset in self.presets.items()
        }
    
    def get_parameters_for_iteration(
        self,
        previous_parameters: Dict,
        quality_feedback: str  # "too_fast", "too_slow", "good", "needs_alignment"
    ) -> ParameterSet:
        """
        Adjust parameters based on feedback from previous generation.
        
        Args:
            previous_parameters: The parameters used in previous generation
            quality_feedback: User/system feedback on quality
        
        Returns:
            Adjusted ParameterSet
        """
        
        current_cfg = previous_parameters.get("cfg_scale", 12.0)
        current_denoise = previous_parameters.get("denoising_strength", 0.75)
        current_steps = previous_parameters.get("num_steps", 70)
        
        if quality_feedback == "too_slow":
            # Reduce steps but maintain quality
            adjusted_steps = max(30, int(current_steps * 0.6))
            adjusted_cfg = min(current_cfg + 1, 20.0)
            reasoning = f"Iteration: Reduced steps {current_steps} → {adjusted_steps}"
            
        elif quality_feedback == "needs_alignment":
            # Reduce denoising to preserve reference
            adjusted_denoise = max(0.4, current_denoise - 0.1)
            adjusted_cfg = current_cfg - 1
            adjusted_steps = current_steps
            reasoning = f"Iteration: Reduced denoising {current_denoise:.2f} → {adjusted_denoise:.2f} for better alignment"
            
            return ParameterSet(
                cfg_scale=adjusted_cfg,
                denoising_strength=adjusted_denoise,
                num_steps=adjusted_steps,
                preset_name="Alignment-Adjusted",
                reasoning=reasoning
            )
            
        elif quality_feedback == "too_fast":
            # Increase quality
            adjusted_steps = min(100, int(current_steps * 1.5))
            adjusted_cfg = min(current_cfg + 2, 20.0)
            reasoning = f"Iteration: Increased steps {current_steps} → {adjusted_steps}, CFG {current_cfg} → {adjusted_cfg}"
            
        else:  # "good" or unknown
            # Keep same parameters
            adjusted_cfg = current_cfg
            adjusted_denoise = current_denoise
            adjusted_steps = current_steps
            reasoning = "Previous parameters were good, maintaining"
        
        return ParameterSet(
            cfg_scale=adjusted_cfg if quality_feedback in ["too_slow", "too_fast"] else current_cfg,
            denoising_strength=adjusted_denoise if quality_feedback == "needs_alignment" else current_denoise,
            num_steps=adjusted_steps if quality_feedback in ["too_slow", "too_fast"] else current_steps,
            preset_name="Feedback-Adjusted",
            reasoning=reasoning
        )


class ParameterRecommendationFactory:
    """Factory for getting singleton instance of ParameterRecommendationEngine"""
    
    _instance: Optional[ParameterRecommendationEngine] = None
    
    @classmethod
    def get_engine(cls) -> ParameterRecommendationEngine:
        """Get or create singleton instance"""
        if cls._instance is None:
            cls._instance = ParameterRecommendationEngine()
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset singleton (for testing)"""
        cls._instance = None
