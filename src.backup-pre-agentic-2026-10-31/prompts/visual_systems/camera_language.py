"""Camera Language - Issue #7 Solution
Professional equipment terminology that dramatically improves photoreal perception.

Modern generation quality improves with:
- Specific sensor types
- Camera body naming
- Shutter behavior
- Film stock emulation  
- Lens rendering style
- Focal length mastery

This creates professional credibility and technical authenticity.
"""

from typing import Dict, Optional, List


class CameraLanguage:
    """Professional camera and lens terminology."""
    
    # Premium camera bodies with rendering signatures
    CAMERA_BODIES = {
        "hasselblad_x2d": {
            "sensor": "medium-format CMOS 100MP",
            "rendering_signature": "creamy bokeh, excellent micro-contrast, natural colors",
            "best_for": "portraits, editorial, luxury, high-detail work",
            "focal_length_note": "50mm is portrait standard on medium-format",
        },
        "arri_alexa_mini": {
            "sensor": "cinema camera ProRes RAW",
            "rendering_signature": "cinematic rendering, extreme dynamic range, film-like gradation",
            "best_for": "cinematic, editorial film, professional production",
            "focal_length_note": "PL mount with cinema lenses",
        },
        "red_komodo": {
            "sensor": "cinema 8K RF mount",
            "rendering_signature": "extreme sharpness, clean highlights, technical precision",
            "best_for": "high-resolution cinema, technical documentation",
            "focal_length_note": "RF mount versatility",
        },
        "phase_one": {
            "sensor": "technical medium-format 80MP",
            "rendering_signature": "absolute sharpness, maximum detail, pristine colors",
            "best_for": "commercial, product, editorial, technical",
            "focal_length_note": "technical camera precision",
        },
        "leica_m": {
            "sensor": "rangefinder full-frame 36MP",
            "rendering_signature": "organic rendering, minimal distortion, documentary feel",
            "best_for": "documentary, editorial, street, lifestyle",
            "focal_length_note": "fixed lens philosophy tradition",
        },
    }
    
    # Professional lenses with rendering characteristics
    PROFESSIONAL_LENSES = {
        "zeiss_milvus_85mm": {
            "focal_length": "85mm (portrait perfect)",
            "aperture_range": "f/1.4 - f/16",
            "rendering": "slight telephoto compression, excellent subject isolation, consistent colors",
            "bokeh": "smooth creamy background blur",
            "use_case": "luxury portrait, fashion editorial",
        },
        "zeiss_otus_55mm": {
            "focal_length": "55mm (50mm equivalent)",
            "rendering": "perfect optical correction, maximum sharpness, scientific precision",
            "bokeh": "neutral smooth bokeh",
            "use_case": "technical excellence, studio work",
        },
        "hasselblad_80mm": {
            "focal_length": "50mm equivalent on medium-format",
            "rendering": "perfect medium-format rendering, creamy bokeh depth",
            "bokeh": "medium-format signature bokeh smoothness",
            "use_case": "portrait editorial, luxury beauty",
        },
        "cooke_anamorphic": {
            "focal_length": "anamorphic variable",
            "rendering": "cinematic anamorphic signature, horizontal oval bokeh",
            "bokeh": "signature horizontal-streaked bokeh balls",
            "use_case": "cinematic, editorial film, dramatic effect",
        },
        "leica_summilux_35mm": {
            "focal_length": "35mm (standard rangefinder)",
            "rendering": "documentary organic feel, minimal distortion",
            "bokeh": "gentle smooth bokeh from f/1.4",
            "use_case": "editorial, lifestyle, street documentary",
        },
    }
    
    # Focal length psychology
    FOCAL_LENGTH_EFFECTS = {
        "24mm": "wide context, environmental emphasis, perspective distortion",
        "35mm": "natural journalism feeling, slight subject compression",
        "50mm": "natural human eye perspective, neutral flattery",
        "85mm": "strong portrait flattery, 1.3x compression, ideal isolation",
        "135mm": "extreme subject isolation, 2x compression, editorial drama",
    }
    
    # Aperture effects on perception
    APERTURE_EFFECTS = {
        1.4: "extreme subject separation, creamy bokeh, shallow depth of field",
        2.0: "strong subject isolation, smooth bokeh, shallow depth of field",
        2.8: "moderate subject separation, pleasant bokeh, working depth of field",
        4.0: "balanced isolation, functional bokeh, useful depth of field",
        5.6: "environmental context visible, subtle bokeh, useful depth of field",
    }
    
    # Shutter speed perception
    SHUTTER_SPEED_EFFECT = {
        "1/1000": "frozen motion, crisp capture, stopped action",
        "1/500": "motion stopped, crisp detail, movement frozen",
        "1/250": "slight motion capture possibility, intentional blur motion",
        "1/125": "potential motion blur from subject movement",
        "1/60": "handheld limit, possible motion blur from hand movement",
        "1/30": "intentional motion blur likely, artistic effect",
    }
    
    @staticmethod
    def generate_camera_string(
        camera_body: Optional[str] = None,
        lens: Optional[str] = None,
        focal_length: Optional[int] = None,
        aperture: float = 2.0,
    ) -> str:
        """Generate professional camera specification string."""
        
        description_parts = []
        
        if camera_body and camera_body in CameraLanguage.CAMERA_BODIES:
            body_info = CameraLanguage.CAMERA_BODIES[camera_body]
            description_parts.append(
                f"Shot on {camera_body} ({body_info.get('sensor', '')})"
            )
        
        if lens and lens in CameraLanguage.PROFESSIONAL_LENSES:
            lens_info = CameraLanguage.PROFESSIONAL_LENSES[lens]
            description_parts.append(
                f"{lens_info.get('focal_length', 'professional lens')}, f/{aperture}"
            )
        elif focal_length:
            description_parts.append(f"{focal_length}mm equivalent, f/{aperture} aperture")
        
        # Add aperture effects
        if aperture in CameraLanguage.APERTURE_EFFECTS:
            description_parts.append(CameraLanguage.APERTURE_EFFECTS[aperture])
        
        return ", ".join(description_parts)
    
    @staticmethod
    def get_rendering_signature(camera: str) -> str:
        """Get camera's rendering signature for prompt."""
        
        if camera in CameraLanguage.CAMERA_BODIES:
            return CameraLanguage.CAMERA_BODIES[camera].get(
                "rendering_signature",
                "professional rendering"
            )
        
        return "professional camera rendering"
    
    @staticmethod
    def focal_length_justification(focal_length: int, purpose: str) -> str:
        """Explain why specific focal length chosen."""
        
        justifications = {
            (24, "landscape"): "wide environmental context with slight perspective drama",
            (35, "editorial"): "journalist natural field of view with subject emphasis",
            (50, "lifestyle"): "natural human perspective maintaining relatable framing",
            (85, "portrait"): "classic portrait focal length with flattering compression",
            (135, "fashion"): "dramatic subject isolation with maximum editorial impact",
        }
        
        key = (focal_length, purpose)
        return justifications.get(key, f"{focal_length}mm focal length for {purpose}")
    
    @staticmethod
    def professional_camera_preset(preset_name: str) -> str:
        """Get preset professional camera setup."""
        
        presets = {
            "luxury_portrait": "Hasselblad X2D with 80mm, f/2.0, medium-format rendering with creamy bokeh",
            "editorial_cinema": "ARRI Alexa Mini ProRes RAW, cinematic rendering with extreme dynamic range",
            "fashion_glamour": "Zeiss Milvus 85mm f/1.4, telephoto portrait flattery with smooth bokeh",
            "documentary": "Leica M with 50mm Summilux, organic rendering with minimal distortion",
            "technical_precision": "Phase One 80MP technical camera, absolute sharpness and detail",
        }
        
        return presets.get(preset_name, "professional camera rendering")
