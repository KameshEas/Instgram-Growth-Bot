"""Optical Characteristics - Issue #5 Solution
Introduces realistic lens imperfections and optical effects that improve realism perception.

Modern AI models can now render:
- Lens breathing effects
- Bloom and glow
- Chromatic aberration
- Sensor noise patterns
- Halation effects
- Natural depth falloff
- Micro contrast

Real photography has these imperfections. AI perfection looks fake.
This module balances perfection with optical authenticity.
"""

from typing import Dict, List, Optional


class OpticalCharacteristics:
    """Model realistic optical effects that improve photorealism perception."""
    
    # Optical profiles by camera/sensor type
    LENS_CHARACTERISTICS = {
        "hasselblad_x2d": {
            "focal_length_feel": "natural perspective with minimal distortion",
            "bloom": "subtle halation around highlights on glossy surfaces",
            "chromatic_aberration": "minimal color fringing, premium lens control",
            "lens_breathing": "imperceptible focus breathing (premium glass)",
            "edge_falloff": "natural soft vignetting at extreme edges",
            "bokeh_quality": "creamy smooth background bokeh from medium-format",
            "micro_contrast": "excellent micro contrast revealing texture detail",
        },
        "anamorphic_lens": {
            "focal_length_feel": "elongated horizontal compression, cinematic aspect",
            "bloom": "signature bloom on highlights, characteristic glow",
            "chromatic_aberration": "controlled color separation on lens edges",
            "lens_breathing": "noticeable focal length shift during focus (characteristic)",
            "edge_falloff": "characteristic oval bokeh, anamorphic bokeh balls",
            "bokeh_quality": "horizontal-streaked bokeh (signature anamorphic)",
            "micro_contrast": "slightly lower micro contrast than spherical (film quality)",
            "flare_characteristic": "signature lens flares from internal glass",
        },
        "film_emulation": {
            "grain_structure": "organic film grain pattern with natural randomness",
            "color_response": "film-accurate color response with slight color shifts",
            "halation": "visible halation effect on bright highlights (backlight glow)",
            "fade": "slight overall image fade suggesting film age",
            "color_fringing": "subtle color fringing in shadows (Kodak characteristic)",
            "dynamic_range": "compression in highlights, lifted blacks (film curve)",
            "contrast_curve": "S-curve in midtones, compressed shadows (film)",
        },
        "digital_cinematic": {
            "noise_pattern": "clean digital noise floor with organized pattern",
            "dynamic_range": "extreme dynamic range with clean blacks",
            "color_accuracy": "precise color reproduction without cast",
            "focus_falloff": "sharp focus transition with smooth falloff",
            "bloom": "minimal bloom unless specifically motivated",
            "micro_contrast": "extremely high micro contrast detail",
        },
    }
    
    # Optical effects that add realism
    OPTICAL_EFFECTS = {
        "subtle_halation": "gentle halation around bright highlights creating dreamy quality",
        "lens_bloom": "subtle bloom effect on bright lights without overexposure",
        "focus_falloff": "natural focus falloff in background with smooth transition",
        "organic_grain": "organic sensor/film grain showing authentic capture",
        "micro_contrast": "enhanced micro contrast revealing material texture detail",
        "chromatic_aberration_subtle": "minimal controlled color fringing at lens edges only",
        "motion_blur": "natural motion blur suggesting captured movement",
        "depth_compression": "compression of depth from telephoto lens perspective",
    }
    
    # Avoid these
    OPTICAL_ANTIS = [
        "avoid digital perfection (too clean, no noise, no grain)",
        "avoid plastic lens rendition (no organic falloff)",
        "avoid flat depth (use natural focus transition)",
        "avoid harsh digital noise (use organic grain pattern)",
        "avoid over-bloom (subtle effects only)",
        "avoid artificial sharpening (use natural micro contrast)",
        "avoid forced chromatic aberration (only where optically motivated)",
    ]
    
    # Sensor/Film combinations
    SENSOR_PROFILES = {
        "arri_logc": {
            "color_science": "ARRI LogC color space providing extreme dynamic range",
            "highlight_preservation": "excellent highlight detail retention",
            "shadow_detail": "lifted blacks with preserved shadow information",
            "color_reproduction": "accurate color with slight magenta/skin tone boost",
            "noise_floor": "very clean noise floor",
        },
        "kodak_portra": {
            "color_science": "Kodak Portra film emulation with warm skin tone rendering",
            "highlight_preservation": "gentle highlight compression (film curve)",
            "shadow_detail": "lifted blacks creating punchy contrast",
            "color_reproduction": "warm pleasing colors with slight orange/yellow cast",
            "grain_structure": "visible organic film grain pattern",
            "halation": "characteristic halation on bright highlights",
        },
        "fuji_eterna": {
            "color_science": "Fuji cinema film emulation with cool highlights",
            "highlight_preservation": "film-like highlight compression",
            "shadow_detail": "warm lifted blacks (shadow warmth characteristic)",
            "color_reproduction": "slight cyan cast in highlights, warm shadows",
            "grain_structure": "fine-grain structure",
            "dynamic_range": "film-typical dynamic range compression",
        },
        "bleach_bypass": {
            "color_science": "bleach bypass technique creating silver-based look",
            "contrast": "extreme contrast with crushed blacks",
            "color_response": "colors appear more saturated with desaturated shadows",
            "highlight_preservation": "reduced highlight recovery",
            "shadow_detail": "deep blacks with reduced detail",
        },
    }
    
    @staticmethod
    def get_optical_string(
        equipment: str,
        optical_effects: Optional[List[str]] = None,
        sensor_profile: Optional[str] = None,
    ) -> str:
        """Generate optical characteristics string for use in prompts."""
        
        if equipment not in OpticalCharacteristics.LENS_CHARACTERISTICS:
            return "professional optical rendering with natural characteristics"
        
        characteristics = OpticalCharacteristics.LENS_CHARACTERISTICS[equipment]
        
        description_parts = [
            f"Optical rendering: {characteristics.get('focal_length_feel', '')}.",
            f"Bokeh quality: {characteristics.get('bokeh_quality', '')}.",
        ]
        
        if optical_effects:
            effects_str = ", ".join(
                OpticalCharacteristics.OPTICAL_EFFECTS.get(effect, effect)
                for effect in optical_effects
            )
            description_parts.append(f"Optical effects: {effects_str}.")
        
        if sensor_profile and sensor_profile in OpticalCharacteristics.SENSOR_PROFILES:
            profile = OpticalCharacteristics.SENSOR_PROFILES[sensor_profile]
            description_parts.append(
                f"Sensor profile: {profile.get('color_science', '')} with "
                f"{profile.get('highlight_preservation', '')}."
            )
        
        return " ".join(description_parts)
    
    @staticmethod
    def realistic_grain_specification(
        grain_type: str = "organic",
        intensity: str = "subtle",
    ) -> str:
        """Specify realistic grain that avoids digital perfection."""
        
        grain_specs = {
            "organic": {
                "subtle": "imperceptible organic grain preserving micro-texture detail",
                "moderate": "visible organic grain pattern suggesting authentic capture",
                "heavy": "prominent organic grain from high-ISO authentic film aesthetic",
            },
            "film_emulation": {
                "subtle": "subtle film grain pattern from 800ISO film stock",
                "moderate": "organic film grain from 1600ISO stock creating texture",
                "heavy": "prominent film grain from 3200ISO stock (authentic film feel)",
            },
            "digital_noise": {
                "subtle": "minimal digital noise floor showing sensor capture",
                "moderate": "visible digital noise pattern authentic to camera",
                "heavy": "prominent digital noise maintaining realistic capture",
            },
        }
        
        spec = grain_specs.get(grain_type, {}).get(intensity, "organic subtle grain")
        return f"{spec} while maintaining sharp detail and micro-texture visibility"
    
    @staticmethod
    def depth_of_field_optical(
        aperture: float,
        focal_length: str,
        focus_subject: str = "subject",
    ) -> str:
        """Specify optical depth of field characteristics."""
        
        dof_descriptions = {
            1.4: "extremely shallow depth of field, creamy bokeh, sharp subject isolation",
            1.8: "very shallow depth of field, strong subject separation, smooth bokeh",
            2.0: "shallow depth of field isolating subject from background",
            2.8: "moderate shallow depth of field with pleasing subject separation",
            4.0: "moderate depth of field maintaining environmental context",
            5.6: "deeper depth of field keeping foreground and background in focus",
        }
        
        base_description = dof_descriptions.get(
            aperture,
            f"depth of field characteristic of f/{aperture} aperture",
        )
        
        return f"{base_description}, focus on {focus_subject}, natural focus falloff in background"
    
    @staticmethod
    def lens_imperfection_string() -> str:
        """Generate lens imperfection description that adds realism without artificiality."""
        
        return (
            "optical imperfections adding authenticity: subtle halation on bright highlights, "
            "natural lens bloom without oversaturation, organic grain pattern showing genuine capture, "
            "micro-contrast revealing material texture, realistic depth falloff with smooth transition, "
            "no digital perfection artifacts, authentic optical rendering"
        )
