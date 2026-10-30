"""Color Grading Intelligence - Issue #9 Solution
Professional color grading profiles replacing primitive warm/cool descriptions.

Professional grading is much more advanced with:
- Kodak film emulation
- ARRI LogC color science
- Specific color curves
- Bleach bypass effects
- Teal/amber cinema
- Shadow warmth
- Highlight rolloff

This creates cinematic color perception.
"""

from typing import Dict, Optional, List


class ColorGrading:
    """Professional color grading profiles."""
    
    # Industry-standard film emulations
    FILM_EMULATIONS = {
        "kodak_portra_400": {
            "description": "Kodak Portra 400 film emulation",
            "characteristics": "warm skin tones, gentle highlight compression, lifted blacks, visible fine grain",
            "shadow_color": "warm shadows with slight yellow cast",
            "highlight_behavior": "gentle rolloff avoiding oversaturation",
            "midtone_feel": "punchy but forgiving",
            "color_cast": "slight orange/warm cast overall",
            "best_for": "portrait, beauty, lifestyle",
        },
        "kodak_ektar_100": {
            "description": "Kodak Ektar 100 film emulation",
            "characteristics": "highly saturated, punchy colors, fine grain, excellent shadow detail",
            "color_response": "extremely vivid, nearly oversaturated by digital standards",
            "shadow_color": "cool shadows with blue cast",
            "best_for": "fashion, commercial, high-impact visuals",
        },
        "fuji_eterna": {
            "description": "Fuji cinema film emulation (Eterna 500T)",
            "characteristics": "cool highlights with cyan cast, warm lifted blacks",
            "shadow_color": "warm shadows, yellowish cast",
            "highlight_behavior": "cool blue highlights",
            "midtone_feel": "neutral professional cinema",
            "best_for": "cinematic, professional production",
        },
        "kodak_2383": {
            "description": "Kodak 2383 cinema print film",
            "characteristics": "extreme highlight compression, lifted blacks, rich shadow detail",
            "dynamic_range": "film-like compressed dynamic range",
            "color_response": "warm prints with excellent skin rendering",
            "best_for": "cinematic, editorial, luxury branding",
        },
    }
    
    # Professional color grading styles
    GRADING_PROFILES = {
        "teal_amber": {
            "description": "Teal and amber cinema look",
            "shadows": "cool cyan-teal tones",
            "midtones": "neutral balanced",
            "highlights": "warm amber tones",
            "characteristic": "high contrast color split creating cinematic energy",
            "use_case": "action, drama, cinematic",
        },
        "bleach_bypass": {
            "description": "Bleach bypass technique look",
            "characteristics": "crushed blacks, extreme contrast, desaturated shadows",
            "color_response": "colors appear hyper-saturated against gray shadows",
            "emotional": "edgy, dramatic, emotional intensity",
            "use_case": "fashion, drama, emotional storytelling",
        },
        "desaturated_luxury": {
            "description": "Desaturated luxury aesthetic",
            "characteristics": "reduced saturation overall, muted palette, sophisticated",
            "shadow_lift": "lifted blacks creating bright, airy feel",
            "color_restriction": "limited palette (3-4 colors maximum)",
            "emotional": "refined, premium, sophisticated",
            "use_case": "luxury branding, high-end editorial, minimalist design",
        },
        "lifted_black": {
            "description": "Lifted blacks grading style",
            "characteristics": "blacks lifted to dark grey, reduced contrast, bright airy",
            "emotional": "ethereal, dreamy, soft",
            "best_for": "romantic, dreamy, soft editorial",
        },
        "crushed_black": {
            "description": "Crushed black grading style",
            "characteristics": "blacks crushed to pure black, extreme contrast, dramatic",
            "emotional": "dramatic, intense, powerful",
            "best_for": "drama, action, high-impact",
        },
    }
    
    # Color temperature profiles
    COLOR_TEMPERATURE_PROFILES = {
        "warm_5500k_3000k": "warm highlight rolloff with cool shadow support, cinematic warmth",
        "neutral_5500k_5500k": "neutral balanced color temperature throughout",
        "cool_5500k_8000k": "cool highlights with cool shadows, professional cool aesthetic",
    }
    
    # Saturation levels
    SATURATION_LEVELS = {
        "desaturated": "reduced saturation creating sophisticated muted palette",
        "neutral": "standard saturation with accurate color reproduction",
        "saturated": "increased saturation creating punchy colors",
        "hypersaturated": "extreme saturation creating cinematic punch",
    }
    
    @staticmethod
    def get_grading_string(
        film_emulation: Optional[str] = None,
        grading_style: Optional[str] = None,
        saturation: str = "neutral",
    ) -> str:
        """Generate color grading description."""
        
        description_parts = []
        
        if film_emulation and film_emulation in ColorGrading.FILM_EMULATIONS:
            profile = ColorGrading.FILM_EMULATIONS[film_emulation]
            description_parts.append(
                f"Color grade: {profile.get('description', '')} with "
                f"{profile.get('characteristics', '')}"
            )
        
        if grading_style and grading_style in ColorGrading.GRADING_PROFILES:
            profile = ColorGrading.GRADING_PROFILES[grading_style]
            description_parts.append(
                f"Shadow tones: {profile.get('shadows', '')}. "
                f"Highlights: {profile.get('highlights', '')}"
            )
        
        if saturation != "neutral" and saturation in ColorGrading.SATURATION_LEVELS:
            description_parts.append(ColorGrading.SATURATION_LEVELS[saturation])
        
        return ". ".join(description_parts)
    
    @staticmethod
    def luxury_grading_string() -> str:
        """Professional luxury color grading."""
        return (
            "Color grade: Kodak 2383 film emulation with warm highlight rolloff and lifted blacks, "
            "desaturated luxury palette, warm skin tones with cool sophisticated shadows, "
            "muted color restriction creating premium perception"
        )
    
    @staticmethod
    def cinematic_grading_string() -> str:
        """Cinematic color grading."""
        return (
            "Cinematic color grade: Fuji Eterna look with cool cyan highlights and warm lifted blacks, "
            "high contrast color split creating drama, professional cinema color science"
        )
    
    @staticmethod
    def shadow_highlight_color(shadow_temp: str = "warm", highlight_temp: str = "cool") -> str:
        """Describe shadow/highlight color split."""
        
        combinations = {
            ("warm", "cool"): "warm lifted shadows with cool sophisticated highlights",
            ("cool", "warm"): "cool shadows with warm golden highlights",
            ("warm", "warm"): "warm throughout shadows and highlights",
            ("cool", "cool"): "cool throughout maintaining color consistency",
        }
        
        return combinations.get((shadow_temp, highlight_temp), "balanced shadow/highlight color")
