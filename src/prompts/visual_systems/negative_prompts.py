"""Negative Prompts System - Issue #10 Solution
One of the biggest missing systems in the current architecture.

Without negative prompts, common quality failures:
- Extra fingers and distorted anatomy
- Plastic-looking skin
- Overprocessed texture
- Distorted eyes
- Oversharpening artifacts
- Uncanny face symmetry
- Duplicate accessories
- Floating limbs
- Bad hands/feet

This system organizes negative prompts by category, quality tier, and style.
Applied strategically to prevent model confusion and quality degradation.
"""

from typing import Dict, List, Optional


class NegativePrompts:
    """Strategic negative prompts preventing quality failures."""
    
    # Universal negatives that always apply
    UNIVERSAL_NEGATIVES = [
        "extra fingers, missing fingers, hand deformity",
        "extra limbs, floating limbs, disconnected limbs",
        "distorted eyes, uneven eyes, asymmetrical irises",
        "bad teeth, deformed teeth, broken teeth",
        "distorted mouth, twisted lips, uneven smile",
        "overprocessed skin, overly filtered look, artificial texture",
        "uncanny valley symmetry, uncanny perfection, artificial beauty",
        "duplicate objects, duplicate accessories, doubled elements",
        "blurry areas, soft focus except intended, muddled composition",
        "oversharpened texture, digital artifacts, compression artifacts",
    ]
    
    # Portrait-specific negatives
    PORTRAIT_NEGATIVES = {
        "anatomy": [
            "neck too long or too short",
            "shoulders asymmetrical",
            "proportions wrong",
            "head too large or small",
        ],
        "facial": [
            "closed eyes, crossed eyes",
            "misaligned eyes, wandering gaze",
            "nose asymmetrical, broken nose",
            "uneven skin tone, splotchy skin",
            "unnatural expression, frozen face",
            "lazy eye, drooping eyelid",
        ],
        "hair": [
            "hair floating, disconnected from head",
            "hair weird texture, plastic hair look",
            "baldness or extreme thinning unexpected",
            "color banding in hair",
        ],
        "skin": [
            "waxy skin, plastic skin appearance",
            "grey cast to skin, wrong undertones",
            "visible makeup edges, unblended makeup",
            "spots and blemishes excessive",
        ],
    }
    
    # Transformation-specific negatives
    TRANSFORMATION_NEGATIVES = {
        "identity": [
            "face doesn't match reference identity",
            "completely different person",
            "unrecognizable from reference image",
            "wrong age, wrong gender appearance",
        ],
        "coherence": [
            "lighting inconsistent with environment",
            "shadows pointing wrong direction",
            "subject too bright/dark for environment",
            "depth cues inconsistent",
        ],
        "realism": [
            "AI plastic look, obviously AI-generated",
            "uncanny imperfection balance",
            "texture too perfect or too damaged",
            "material behavior impossible",
        ],
    }
    
    # Product/design negatives
    PRODUCT_NEGATIVES = [
        "warped product shape, distorted product",
        "color wrong, inaccurate color rendering",
        "missing product parts, incomplete product",
        "product floating, impossible positioning",
        "shadow glitches, unrealistic shadows",
        "reflections impossible, wrong reflections",
    ]
    
    # Common quality failure negatives
    QUALITY_FAILURE_NEGATIVES = [
        "extreme close-up of pores, gross magnification",
        "visible digital noise, excessive grain",
        "compression artifacts, pixelation",
        "color fringing, chromatic aberration extreme",
        "motion blur unintended, ghosting",
        "aliasing, jagged edges",
        "tearing artifacts, discontinuity glitches",
    ]
    
    # Style-inappropriate negatives
    STYLE_ANTIS = {
        "luxury": [
            "cheap appearance, budget aesthetic",
            "obvious advertising, commercial feel",
            "trendy elements, dated design",
            "busy composition, visual clutter",
        ],
        "cinema": [
            "flat lighting, no dimensionality",
            "artificial color grading, oversaturated",
            "video game look, unreal engine feel",
            "CGI plastic quality",
        ],
        "minimalism": [
            "busy composition, cluttered background",
            "multiple focal points, scattered attention",
            "colorful chaos, palette confusion",
            "ornate decoration, excessive detail",
        ],
        "portrait": [
            "headless shot, cropped face",
            "too wide framing, body dominant not face",
            "crowded frame, environmental distraction",
            "odd perspective, unflattering angle",
        ],
    }
    
    # Model-specific failure modes
    MODEL_FAILURE_NEGATIVES = {
        "sdxl": [
            "repetitive text, watermark text",
            "distorted hands that look like paws",
            "melted features, face deformation",
        ],
        "midjourney": [
            "multiple people when single requested",
            "abstract instead of literal",
            "style blending chaos",
        ],
        "flux": [
            "oversaturation, extreme colors",
            "extreme sharpness artefacts",
            "loss of detail in shadows",
        ],
    }
    
    @staticmethod
    def get_category_negatives(category: str) -> List[str]:
        """Get negatives for a specific category."""
        
        category_negatives = {
            "portrait": NegativePrompts.UNIVERSAL_NEGATIVES + NegativePrompts.PORTRAIT_NEGATIVES.get("anatomy", []),
            "transformation": NegativePrompts.UNIVERSAL_NEGATIVES + NegativePrompts.TRANSFORMATION_NEGATIVES.get("identity", []),
            "product": NegativePrompts.UNIVERSAL_NEGATIVES + NegativePrompts.PRODUCT_NEGATIVES,
            "design": NegativePrompts.QUALITY_FAILURE_NEGATIVES + NegativePrompts.PRODUCT_NEGATIVES,
            "landscape": ["people in frame, humans visible", "text, watermarks", "artificial structures"],
            "couple": NegativePrompts.UNIVERSAL_NEGATIVES + ["faces different people", "wrong number of people"],
        }
        
        return category_negatives.get(category, NegativePrompts.UNIVERSAL_NEGATIVES)
    
    @staticmethod
    def generate_negative_prompt_string(
        category: str,
        quality_level: str = "professional",
        style: Optional[str] = None,
        model: Optional[str] = None,
    ) -> str:
        """
        Generate complete negative prompt string for quality guardrails.
        
        Args:
            category: "portrait", "transformation", "product", "design"
            quality_level: "web", "professional", "exhibition"
            style: Style director if applicable
            model: "sdxl", "midjourney", "flux", etc.
            
        Returns:
            Negative prompt string formatted for model
        """
        
        negatives = NegativePrompts.get_category_negatives(category)
        
        # Add quality-level specific negatives
        quality_additions = {
            "web": ["excessive detail", "overwhelming texture"],
            "professional": [],  # Base negatives sufficient
            "exhibition": ["visible compression", "lost detail in shadows"],
        }
        
        negatives.extend(quality_additions.get(quality_level, []))
        
        # Add style-specific antis
        if style and style in NegativePrompts.STYLE_ANTIS:
            negatives.extend(NegativePrompts.STYLE_ANTIS[style])
        
        # Add model-specific failures
        if model and model in NegativePrompts.MODEL_FAILURE_NEGATIVES:
            negatives.extend(NegativePrompts.MODEL_FAILURE_NEGATIVES[model])
        
        # Format as comma-separated negative string
        return ", ".join(negatives)
    
    @staticmethod
    def get_portrait_negatives() -> str:
        """Quick portrait negatives string."""
        negatives = NegativePrompts.UNIVERSAL_NEGATIVES + [
            "closed eyes, lazy eye, wall eye",
            "distorted face, melted features",
            "unnatural expression, frozen smile",
            "bad anatomy, wrong proportions",
            "plastic skin, waxy appearance",
            "oversharpenedface, grain excessive",
        ]
        return ", ".join(negatives)
    
    @staticmethod
    def get_transformation_negatives() -> str:
        """Quick transformation negatives string."""
        negatives = NegativePrompts.UNIVERSAL_NEGATIVES + [
            "unrecognizable from reference",
            "completely different person",
            "wrong age or gender",
            "inconsistent lighting",
            "impossible shadows",
            "AI plastic aesthetic",
            "uncanny valley appearance",
        ]
        return ", ".join(negatives)
    
    @staticmethod
    def get_luxury_product_negatives() -> str:
        """Quick luxury product negatives."""
        negatives = [
            "cheap appearance, budget look",
            "distorted product shape",
            "wrong product color, inaccurate",
            "impossible shadows, glitchy reflection",
            "background distraction, visual clutter",
            "oversharping, digital artifacts",
            "poor lighting, uneven illumination",
        ]
        return ", ".join(negatives)
    
    @staticmethod
    def add_negative_emphasis(
        base_negatives: str,
        priority_negatives: Optional[List[str]] = None,
    ) -> str:
        """
        Add emphasis to specific negatives (for models supporting weights).
        Format: (negative1:1.5), (negative2:1.2), etc.
        
        Args:
            base_negatives: Base negative prompt string
            priority_negatives: Negatives to emphasize with higher weight
            
        Returns:
            Weighted negative prompt string
        """
        
        if not priority_negatives:
            return base_negatives
        
        # Add emphasis (1.5x weight) to priority negatives
        emphasized = [f"({neg}:1.5)" for neg in priority_negatives]
        
        return f"{', '.join(emphasized)}, {base_negatives}"
    
    @staticmethod
    def get_safety_negatives() -> str:
        """Basic safety negatives that always apply."""
        return (
            "extra fingers, wrong anatomy, distorted limbs, "
            "plastic skin, waxy appearance, artificial beauty, "
            "uncanny valley, obvious AI artifacts, digital glitches"
        )
