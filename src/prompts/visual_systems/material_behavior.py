"""Material Behavior Intelligence - Issue #4 Solution
Adds material-specific rendering instructions for photorealistic results.

Current prompts barely describe:
- Fabric behavior
- Skin reflectance
- Metallic response
- Glass refraction
- Environmental interaction

Without this, outputs feel "AI plastic". This module encodes material-specific
rendering that creates cinematic realism instantly.
"""

from typing import Dict, List, Optional


class MaterialBehavior:
    """Define how materials render, reflect, absorb light, and interact."""
    
    MATERIAL_DESCRIPTIONS = {
        "skin": {
            "reflectance_type": "soft diffuse with subsurface scattering",
            "light_interaction": "light penetrating thin areas (ears, nostrils), warm undertones visible",
            "texture_detail": "micro-scale texture detail visible at close focus, natural pore structure",
            "color_response": "warm undertones (yellow/orange base) with slight surface redness",
            "moisture_level": "subtle perspiration sheen on forehead/upper lip without oiliness",
            "imperfections": "natural freckles, moles, skin texture variations add authenticity",
            "specular_highlights": "soft specular catches on eyes showing depth and soul",
            "aging_characteristics": "character lines, expression wrinkles suggesting authenticity",
            "foundation_interaction": "if makeup present, flawless blending without visible edges",
        },
        "cotton_fabric": {
            "reflectance_type": "diffuse matte finish, no specular highlights",
            "light_interaction": "soft light absorption, gentle shadow creation",
            "texture_detail": "woven texture visible with directional light, thread structure apparent",
            "color_response": "accurate color reproduction with slight fabric weave variation",
            "draping_behavior": "natural fabric fold geometry creating organic shadows",
            "weathering": "natural wear patterns, slight fading authentic to use",
            "wrinkle_detail": "natural wrinkles and creases following fabric movement",
            "sheen": "matte finish without reflection",
        },
        "silk_fabric": {
            "reflectance_type": "diffuse with subtle specular highlights",
            "light_interaction": "light absorption with lustrous sheen, gentle bounce",
            "texture_detail": "smooth weave with fine thread structure visible",
            "color_response": "rich color reproduction with luminous quality",
            "draping_behavior": "elegant flowing folds with smooth transitions",
            "sheen_behavior": "subtle sheen catching light without glossiness",
            "specular_highlights": "gentle specular from directional light on surface",
            "material_luxury": "luxurious appearance obvious through rendering quality",
        },
        "brushed_metal": {
            "reflectance_type": "diffuse with directional highlight following surface",
            "light_interaction": "directional light creating sharp specular reflection",
            "texture_detail": "visible brush stroke pattern creating directional texture",
            "specular_highlights": "sharp directional highlights showing surface finish",
            "reflection_quality": "reflections showing surface finish quality",
            "oxidation": "subtle oxidation or patina showing authenticity",
            "color_response": "metallic color with surface direction apparent",
            "wear_patterns": "natural wear and oxidation adding character",
        },
        "polished_metal": {
            "reflectance_type": "sharp mirror-like reflection",
            "light_interaction": "crisp directional reflection of light sources and environment",
            "specular_highlights": "bright sharp specular from all light sources",
            "reflection_clarity": "clear reflections visible on surface showing quality",
            "surface_finish": "flawless polished appearance",
            "environmental_reflection": "environmental reflection visible on surface",
            "luxury_appearance": "pristine luxury perception obvious",
        },
        "glass": {
            "reflectance_type": "Fresnel reflection (more reflection at shallow angles)",
            "refraction": "realistic light refraction through transparent material",
            "transparency": "perfect transparency with accurate color transmission",
            "surface_detail": "dust particles visible on surface showing realism",
            "reflection": "environmental reflection visible on glass surface",
            "distortion": "subtle distortion visible through glass",
            "light_transmission": "light passing through with perfect accuracy",
            "surface_imperfections": "natural imperfections suggesting real glass",
        },
        "wood": {
            "reflectance_type": "diffuse with subtle specular from varnish or grain",
            "grain_pattern": "visible wood grain following natural growth rings",
            "texture_detail": "surface texture varying from polished to hand-planed",
            "color_variation": "natural color variation in grain creating depth",
            "reflection": "matte reflection if unfinished, subtle sheen if varnished",
            "weathering": "authentic wear patterns showing age and quality",
            "finish_appearance": "finish quality obvious through rendering detail",
            "material_warmth": "inherent warmth of wood material obvious in color",
        },
        "leather": {
            "reflectance_type": "soft diffuse with slight sheen",
            "light_interaction": "subtle light absorption and bounce",
            "texture_detail": "visible leather grain and natural pore structure",
            "color_response": "rich leather color with subtle variation",
            "wear_patterns": "natural wear and patina showing authenticity",
            "crease_behavior": "natural creases and folds creating organic shadows",
            "luxury_feel": "luxurious material appearance obvious",
            "aging_character": "aging improving leather appearance",
        },
        "cashmere": {
            "reflectance_type": "soft diffuse with subtle luster",
            "light_interaction": "gentle light absorption with luminous quality",
            "texture_detail": "fine fibrous texture creating soft appearance",
            "color_response": "rich color with slight light variation",
            "luster": "subtle lustrous quality suggesting premium material",
            "softness_appearance": "apparent softness obvious through rendering",
            "luxury_perception": "premium material perception immediate",
            "light_handling": "light handling creating premium perception",
        },
        "denim": {
            "reflectance_type": "diffuse matte with subtle texture reflection",
            "light_interaction": "soft light absorption",
            "texture_detail": "woven texture with visible thread pattern",
            "color_response": "rich indigo with natural color variation",
            "wear_patterns": "authentic wear patterns, fading, and creasing",
            "fabric_structure": "fabric weight apparent through rendering",
            "aging": "aging improving appearance (fade lines, creases)",
        },
    }
    
    @staticmethod
    def get_material_rendering(
        material: str,
        context: Optional[str] = None,
        lighting_type: Optional[str] = None,
    ) -> str:
        """
        Generate material-specific rendering instruction.
        
        Args:
            material: Material type (skin, silk_fabric, brushed_metal, etc.)
            context: Usage context ("clothing", "surface", "architectural")
            lighting_type: How material should be lit (directional, diffuse, etc.)
            
        Returns:
            Material rendering instruction for use in prompts
        """
        
        if material not in MaterialBehavior.MATERIAL_DESCRIPTIONS:
            return f"realistic {material} rendering with natural material properties"
        
        material_props = MaterialBehavior.MATERIAL_DESCRIPTIONS[material]
        
        description_parts = [
            f"{material} with {material_props.get('reflectance_type', '')}",
            f"{material_props.get('light_interaction', '')}",
        ]
        
        if "texture_detail" in material_props:
            description_parts.append(f"{material_props['texture_detail']}")
        
        if "wear_patterns" in material_props and context == "aged":
            description_parts.append(f"{material_props['wear_patterns']}")
        
        return ", ".join(description_parts)
    
    @staticmethod
    def fabric_combination(fabric1: str, fabric2: str) -> str:
        """Describe material contrast combination for luxury appearance."""
        
        fabric_pairings = {
            ("cotton", "silk"): "matte cotton absorbing light softly contrasting with lustrous silk sheen",
            ("leather", "linen"): "rich leather material contrast with organic linen texture",
            ("cashmere", "silk"): "ultra-soft cashmere with luminous silk creating premium luxury perception",
            ("wool", "linen"): "brushed wool texture with crisp linen creating visual interest",
            ("velvet", "satin"): "luxurious velvet depth with satin sheen creating dimensional texture",
        }
        
        key = tuple(sorted([fabric1, fabric2]))
        
        if key in fabric_pairings:
            return fabric_pairings[key]
        else:
            return f"material contrast between {fabric1} and {fabric2} creating visual richness"
    
    @staticmethod
    def skin_rendering_luxury(age_range: str = "adult", ethnicity: Optional[str] = None) -> str:
        """Render skin with luxury perception (lived-in authenticity)."""
        
        base = (
            "natural skin texture with subtle imperfections (lived-in luxury, tactile realism), "
            "micro-scale pore structure visible, natural color variation creating depth, "
            "character lines suggesting authenticity, luminous yet grounded presence, "
            "soft specular in eyes showing depth and soul"
        )
        
        age_additions = {
            "young": ", youthful smoothness with subtle character beginning",
            "adult": ", mature character with refined presence",
            "mature": ", distinguished character lines suggesting wisdom",
        }
        
        ethnicity_additions = {
            "warm_undertone": ", warm undertone foundation in skin rendering",
            "cool_undertone": ", cool undertone foundation suggesting refinement",
        }
        
        result = base
        if age_range in age_additions:
            result += age_additions[age_range]
        if ethnicity in ethnicity_additions:
            result += ethnicity_additions[ethnicity]
        
        return result
    
    @staticmethod
    def material_imperfection_authenticity(material: str) -> str:
        """Add authentic imperfections that prove real material."""
        
        imperfection_specs = {
            "fabric": "natural wrinkles from fabric movement, organic fabric draping, authentic wear patterns",
            "skin": "subtle skin texture variation, natural pores visible, authentic character lines",
            "metal": "subtle oxidation or patina showing authenticity, realistic surface marks",
            "wood": "natural grain variation, authentic aging, weathering showing quality",
            "leather": "authentic creasing and wear patterns improving with age, natural texture",
            "glass": "dust particles on surface showing reality, subtle surface imperfections",
        }
        
        return imperfection_specs.get(material, "authentic material imperfections proving reality")
    
    @staticmethod
    def material_response_to_environment(
        material: str,
        environment: str,
    ) -> str:
        """How material responds to environmental conditions."""
        
        responses = {
            ("skin", "humid"): "subtle perspiration sheen, skin flush from humidity, natural moisture",
            ("fabric", "rain"): "fabric darkened with moisture, clinging natural to body, water interaction",
            ("metal", "wet"): "water droplets catching light, reflections distorted by water",
            ("leather", "aged"): "natural patina and creasing improving with time, character development",
            ("wood", "sunny"): "natural fading from sun exposure, grain relief enhanced by UV",
        }
        
        key = (material, environment)
        
        if key in responses:
            return responses[key]
        else:
            return f"{material} authentically responding to {environment} conditions"
