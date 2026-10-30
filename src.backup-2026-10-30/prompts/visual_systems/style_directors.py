"""Style Directors - Issue #18 Solution
Visual Intent Coherence: The biggest leap in quality perception.

Problem: Current system mixes visual languages
- cinematic + editorial + luxury + dramatic + innovative (all at once)

Solution: STYLE DIRECTORS provide coherent visual languages
- A24_film (indie film aesthetics)
- Apple_commercial (minimalist precision)
- Nike_editorial (athletic sophistication)
- BladeRunner_noir (cyberpunk realism)
- Kinfolk_minimalism (editorial minimalism)

Each director controls:
- Lighting language
- Palette language
- Composition philosophy
- Texture/material choices
- Emotional tone
- Lensing approach
- Atmospheric quality

This creates COHERENT CINEMATIC OUTPUT instead of "everything special" chaos.
"""

from typing import Dict, List, Optional


class StyleDirectors:
    """Coherent visual language systems for consistent cinematic output."""
    
    STYLE_PROFILES = {
        "A24_film": {
            "visual_philosophy": "indie film authenticity, naturalistic beauty, emotional depth over spectacle",
            "lighting": "motivational lighting showing light source logic, natural documentary feel, shadows respected",
            "color_palette": "desaturated muted palette, warm flesh tones, cool shadows, minimal color purity",
            "composition": "asymmetrical framing, negative space design, character focus over spectacle",
            "texture_approach": "tactile authenticity, visible imperfections, authentic aging",
            "lensing": "50mm natural perspective or 35mm wider context, shallow focus on character",
            "atmospheric_quality": "intimate close, observational distance, documentary realism",
            "emotional_tone": "introspective, melancholic beauty, authentic emotion over drama",
            "material_choice": "natural materials, authentic wear, character-driven design",
            "rejection_list": "oversaturation, artificial effects, perfect lighting, cinematic bombast",
        },
        
        "Apple_commercial": {
            "visual_philosophy": "minimalist precision, iconic simplicity, whitespace as luxury",
            "lighting": "precise directional lighting, clean shadows with edge control, professional studio quality",
            "color_palette": "pristine whites, pure blacks, minimal accent color (single), highly controlled",
            "composition": "symmetrical or grid-aligned layout, perfect balance, intentional negative space",
            "texture_approach": "polished perfection, material excellence obvious, flawless finish",
            "lensing": "telephoto compression for iconic framing, perfect focus everywhere",
            "atmospheric_quality": "timeless, elevated, aspirational",
            "emotional_tone": "confident certainty, innovation clarity, future-forward positivity",
            "material_choice": "premium materials, polished surfaces, technological precision",
            "rejection_list": "chaos, imperfection, aging, shadows, complexity, busy composition",
        },
        
        "Nike_editorial": {
            "visual_philosophy": "athletic sophistication, movement discipline, human achievement",
            "lighting": "dramatic athletic lighting, high contrast energy, motion-responsive",
            "color_palette": "primary accent colors (black/white + vibrant single), high contrast punch",
            "composition": "dynamic diagonal lines, leading motion, athlete-centric framing",
            "texture_approach": "performance materials, technical textile detail, athletic authenticity",
            "lensing": "wide 24-35mm capturing environmental context, motion implied",
            "atmospheric_quality": "energetic, aspirational, performance-focused",
            "emotional_tone": "achievement, discipline, human potential, competitive energy",
            "material_choice": "technical materials, performance textiles, athletic innovation",
            "rejection_list": "stillness, softness, gentleness, muted colors, contemplation",
        },
        
        "BladeRunner_noir": {
            "visual_philosophy": "cyberpunk realism, technological authenticity, dystopian beauty",
            "lighting": "neon practical lighting, dramatic color-cast shadows, volumetric light",
            "color_palette": "cyan/magenta cyberpunk, warm practical lights, cool atmospheric", 
            "composition": "layered depth, foreground/midground/background rich, architectural framing",
            "texture_approach": "worn technological surfaces, visible technology, material decay",
            "lensing": "wide environmental context, depth-layered, architecture-prominent",
            "atmospheric_quality": "volumetric particle interaction, visible air, dystopian haze",
            "emotional_tone": "sophisticated noir melancholy, technological wonder, mysterious depth",
            "material_choice": "weathered tech, industrial surfaces, architectural elements",
            "rejection_list": "softness, warmth, simplicity, whitespace, organic materials, hope",
        },
        
        "Kinfolk_minimalism": {
            "visual_philosophy": "editorial minimalism, lifestyle authenticity, quiet beauty",
            "lighting": "soft natural window light, gentle diffusion, no artificial feel",
            "color_palette": "earth tones, warm neutrals, restrained natural colors",
            "composition": "minimal negative space, horizontal lines, lifestyle context minimal",
            "texture_approach": "natural materials, artisanal imperfection, aged authenticity",
            "lensing": "50mm natural perspective, conversational distance",
            "atmospheric_quality": "peaceful, approachable, intimate, present-moment quality",
            "emotional_tone": "calm contemplation, authentic connection, present-moment awareness",
            "material_choice": "natural materials, handmade aesthetic, organic aging",
            "rejection_list": "technology, perfection, color saturation, complexity, artificial effects",
        },
        
        "luxury_hotel_campaign": {
            "visual_philosophy": "premium sophistication, architectural luxury, curated experience",
            "lighting": "professional hotel lighting, warm welcomes with cool sophistication",
            "color_palette": "champagne golds, deep charcoals, cream whites, single accent luxury",
            "composition": "architectural precision, balanced composition, hotel aesthetic framing",
            "texture_approach": "luxury material excellence, textile richness, surface quality obvious",
            "lensing": "85mm portrait feel, environmental context minimized",
            "atmospheric_quality": "timeless luxury, aspirational experience, curated beauty",
            "emotional_tone": "refined confidence, welcoming premium, sophisticated ease",
            "material_choice": "luxury textiles, premium surfaces, architectural materials",
            "rejection_list": "homey feeling, casual aesthetic, imperfection, visible technology",
        },
        
        "fashion_editorial": {
            "visual_philosophy": "high fashion sophistication, model-centric beauty, editorial presence",
            "lighting": "dramatic fashion lighting, skin-flattering positioning, runway quality",
            "color_palette": "editorial sophisticated, often desaturated with color pops",
            "composition": "model-dominant, fashion detail emphasized, environmental minimal",
            "texture_approach": "fabric luxury obvious, textile detail emphasized",
            "lensing": "85mm portrait compression, subject-focused isolation",
            "atmospheric_quality": "runway presence, editorial glamour, professional beauty",
            "emotional_tone": "confident presence, fashion authority, aspirational elegance",
            "material_choice": "designer materials, textile excellence, fashion innovation",
            "rejection_list": "casual feeling, natural imperfection, environmental context, documentary feel",
        },
        
        "hyperreal_portrait": {
            "visual_philosophy": "photorealistic mastery, perfect rendering, technical excellence",
            "lighting": "perfect three-point studio setup, optimal modeling light",
            "color_palette": "color accurate, perfect reproduction, vibrant within realism",
            "composition": "centered subject framing, portrait tradition, beauty-optimized",
            "texture_approach": "skin perfection, texture detail mastery, flawless rendering",
            "lensing": "85mm portrait compression, beauty-specific focal length",
            "atmospheric_quality": "technical perfection, masterpiece rendering, exhibition-ready",
            "emotional_tone": "beauty celebration, technical mastery, artistic rendering",
            "material_choice": "material perfection, texture excellence, rendering mastery",
            "rejection_list": "imperfection, aging, decay, document feel, casual capture",
        },
    }
    
    @staticmethod
    def get_style_director(style: str) -> Dict[str, str]:
        """Get complete style director profile."""
        
        if style not in StyleDirectors.STYLE_PROFILES:
            return {"error": f"Unknown style: {style}"}
        
        return StyleDirectors.STYLE_PROFILES[style]
    
    @staticmethod
    def apply_director_to_component(
        style: str,
        component: str,
        base_description: str,
    ) -> str:
        """
        Apply style director philosophy to a component description.
        
        Args:
            style: Style director name (A24_film, Apple_commercial, etc.)
            component: Component type (lighting, composition, color, texture)
            base_description: Base component description
            
        Returns:
            Style-modified component description
        """
        
        if style not in StyleDirectors.STYLE_PROFILES:
            return base_description
        
        profile = StyleDirectors.STYLE_PROFILES[style]
        
        if component == "lighting":
            return f"{profile.get('lighting', base_description)}"
        elif component == "color":
            return f"{profile.get('color_palette', base_description)}"
        elif component == "composition":
            return f"{profile.get('composition', base_description)}"
        elif component == "texture":
            return f"{profile.get('texture_approach', base_description)}"
        elif component == "emotional_tone":
            return f"{profile.get('emotional_tone', base_description)}"
        
        return base_description
    
    @staticmethod
    def generate_style_constraint_string(style: str) -> str:
        """Generate negative prompt constraints for style coherence."""
        
        if style not in StyleDirectors.STYLE_PROFILES:
            return ""
        
        profile = StyleDirectors.STYLE_PROFILES[style]
        rejections = profile.get("rejection_list", [])
        
        if isinstance(rejections, str):
            rejections = [rejections]
        
        return f"Avoid: {', '.join(rejections)}"
    
    @staticmethod
    def describe_visual_intent(style: str) -> str:
        """
        Describe the overall visual intent without component details.
        Ensures coherent visual language throughout.
        """
        
        if style not in StyleDirectors.STYLE_PROFILES:
            return "professional visual rendering"
        
        profile = StyleDirectors.STYLE_PROFILES[style]
        
        return (
            f"Overall visual intent: {profile.get('visual_philosophy', '')}. "
            f"Atmospheric quality: {profile.get('atmospheric_quality', '')}. "
            f"Emotional tone: {profile.get('emotional_tone', '')}."
        )
    
    @staticmethod
    def select_appropriate_director(
        context: str,
        audience: Optional[str] = None,
        brand: Optional[str] = None,
    ) -> str:
        """
        Intelligently select appropriate style director for context.
        
        Args:
            context: "transformation", "campaign", "editorial", "luxury", "lifestyle"
            audience: "luxury_premium", "athletic", "indie_cultural", "tech_forward"
            brand: specific brand aesthetic if known
            
        Returns:
            Recommended style director name
        """
        
        recommendations = {
            ("transformation", "luxury_premium"): "luxury_hotel_campaign",
            ("transformation", "athletic"): "Nike_editorial",
            ("transformation", "indie_cultural"): "A24_film",
            ("campaign", "luxury_premium"): "Apple_commercial",
            ("campaign", "athletic"): "Nike_editorial",
            ("editorial", "lifestyle"): "Kinfolk_minimalism",
            ("editorial", "fashion"): "fashion_editorial",
            ("editorial", "tech"): "BladeRunner_noir",
            ("portrait", "luxury"): "fashion_editorial",
            ("portrait", "hyperreal"): "hyperreal_portrait",
        }
        
        key = (context, audience) if audience else (context,)
        
        # Try full key first
        if key in recommendations:
            return recommendations[key]
        
        # Fallback to context only
        context_fallbacks = {
            "luxury": "luxury_hotel_campaign",
            "athletic": "Nike_editorial",
            "indie": "A24_film",
            "minimalist": "Kinfolk_minimalism",
            "fashion": "fashion_editorial",
            "tech": "BladeRunner_noir",
        }
        
        return context_fallbacks.get(context, "A24_film")
