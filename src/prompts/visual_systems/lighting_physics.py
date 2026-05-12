"""Lighting Physics - Issue #2 Deep Resolution
Realistic physical light behavior and interaction modeling.

Replaces generic "cinematic lighting" with:
- Physical light source angles
- Shadow direction and falloff
- Bounce light calculations
- Material light interaction
- Atmospheric light scattering
- Color temperature accuracy
- Temporal consistency with time of day
"""

from typing import Dict, Optional


class LightingPhysics:
    """Model realistic light behavior for scene coherence."""
    
    # Physical light setups
    PROFESSIONAL_SETUPS = {
        "three_point_portrait": {
            "key_light": "primary directional light at 45 degrees, 3 stops brighter than fill",
            "fill_light": "opposite side at 50% key intensity, softening shadows",
            "rim_light": "behind subject at 45 degrees from side, 1-2 stops above key",
            "background_light": "separate light on background or distance creates separation",
            "result": "dimensional three-dimensional modeling with controlled shadows",
        },
        "two_point_editorial": {
            "key_light": "primary directional light creating dominant shadow",
            "fill_light": "opposite side 30-40% key intensity, showing fill shadow area",
            "result": "editorial drama with preserved detail in shadows",
        },
        "rembrandt": {
            "key_light": "45 degree directional light creating triangle of light on shadow side",
            "characteristics": "one eye in highlight, other in shadow, triangle light visible",
            "emotional": "classic beauty portrait with dramatic refinement",
        },
        "butterfly": {
            "key_light": "directly in front and slightly above subject",
            "characteristics": "butterfly-shaped shadow under nose, flattering for wide faces",
            "fill_light": "broad fill creating minimal shadow",
        },
    }
    
    # Time-based lighting
    DAYLIGHT_PHASES = {
        "golden_hour_morning": {
            "sun_angle": "15-25 degrees above horizon",
            "color_temperature": "3500K warm amber light",
            "shadow_length": "extremely long soft shadows",
            "quality": "diffuse warm light with soft edges",
            "intensity": "moderate, warm, flattering",
        },
        "midday": {
            "sun_angle": "60-90 degrees overhead",
            "color_temperature": "5500K neutral daylight",
            "shadow_length": "short harsh shadows under subject",
            "quality": "hard directional light, high contrast",
            "intensity": "extreme, flat midtone, harsh",
        },
        "golden_hour_evening": {
            "sun_angle": "15-25 degrees above horizon",
            "color_temperature": "2700K-3200K warm amber",
            "shadow_length": "extremely long soft shadows",
            "quality": "diffuse warm light, magic hour",
            "intensity": "moderate-low, extremely flattering",
        },
        "blue_hour": {
            "sun_angle": "below horizon, -6 to 0 degrees",
            "color_temperature": "7000K cool blue daylight",
            "shadow_length": "no shadows, ambient light only",
            "quality": "soft diffuse twilight",
            "intensity": "very low, moody, atmospheric",
        },
    }
    
    # Artificial lighting temperature
    ARTIFICIAL_TEMPERATURES = {
        "tungsten": "2700K warm household bulbs",
        "halogen": "3000K-3500K stage lights",
        "sodium_vapor": "2000-2500K street lighting",
        "led_warm": "2700K-3000K warm whites",
        "led_neutral": "4000-5000K neutral whites",
        "led_cool": "5600-6500K cool whites",
        "neon_red": "red glow from neon signs",
        "neon_blue": "blue glow from neon signs",
    }
    
    @staticmethod
    def get_physical_lighting_description(
        setup_type: str,
        time_of_day: Optional[str] = None,
        location: str = "studio",
    ) -> str:
        """Generate physically accurate lighting description."""
        
        if location == "outdoor" and time_of_day:
            daylight_info = LightingPhysics.DAYLIGHT_PHASES.get(
                time_of_day,
                {"result": "natural daylight"}
            )
            return (
                f"Outdoor lighting: sun at {daylight_info.get('sun_angle', '')}. "
                f"Color temperature: {daylight_info.get('color_temperature', '')}. "
                f"Shadow quality: {daylight_info.get('quality', '')}. "
                f"Light intensity: {daylight_info.get('intensity', '')}."
            )
        
        elif setup_type in LightingPhysics.PROFESSIONAL_SETUPS:
            setup = LightingPhysics.PROFESSIONAL_SETUPS[setup_type]
            return (
                f"Professional lighting setup: {setup.get('key_light', '')}. "
                f"{setup.get('fill_light', '')}. {setup.get('result', '')}."
            )
        
        return f"Professional {setup_type} lighting"
    
    @staticmethod
    def calculate_shadow_direction(
        light_angle_degrees: int,
        light_height_ratio: float = 0.75,
    ) -> str:
        """Calculate shadow direction from light position."""
        
        if light_angle_degrees < 45:
            direction = "long shadows cast away from light"
        elif light_angle_degrees < 70:
            direction = "moderate-length shadows tapering below subject"
        else:
            direction = "short shadows visible only at subject base"
        
        return direction
    
    @staticmethod
    def bounce_light_calculation(
        primary_intensity: float,
        surface_reflectance: str,
        distance: str = "close",
    ) -> str:
        """Calculate bounce light from surfaces."""
        
        reflectance_values = {
            "white": 0.9,
            "grey": 0.5,
            "skin": 0.35,
            "black": 0.1,
            "polished_metal": 0.95,
            "dull_wood": 0.2,
        }
        
        reflectance = reflectance_values.get(surface_reflectance, 0.5)
        bounce_intensity = primary_intensity * reflectance
        
        if bounce_intensity > 0.7:
            return "strong bounce light creating fill automatically"
        elif bounce_intensity > 0.3:
            return "moderate bounce light softening shadows gradually"
        else:
            return "minimal bounce light with hard shadow edges"
