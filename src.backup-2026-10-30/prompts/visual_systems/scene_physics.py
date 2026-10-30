"""Scene Physics Layer - Issue #2 Solution
Introduces realistic physical scene logic and spatial understanding.

Instead of describing things independently, scene physics models:
- How light physically interacts with surfaces
- Shadow direction and behavior based on light angle
- Atmospheric density and particle interaction
- Bounce lighting on surfaces
- Material reflective response
- Environmental interaction coherence

This creates photorealistic depth and removes "fake-looking renders" feel.
"""

from typing import Dict, List, Optional


class ScenePhysics:
    """Model physical interactions in scenes for realistic depth."""
    
    # Golden hour physics (most used in transformations)
    GOLDEN_HOUR_PHYSICS = {
        "light_angle": "low-angle sunset (15-25 degrees above horizon)",
        "shadow_direction": "long soft shadows casting away from light source",
        "shadow_behavior": "feathered soft falloff, no hard edges",
        "bounce_light": "warm bounce light reflecting subtly onto shadow areas",
        "atmospheric_density": "humid evening air softly diffusing light",
        "reflection_quality": "soft warm reflections on polished surfaces (eyes, skin, metal)",
        "color_temperature": "warm 3200K-4500K with cool blue shadows",
        "material_response": "matte surfaces absorbing warmth, specular surfaces catching directional light",
    }
    
    # Studio photography physics
    STUDIO_PHYSICS = {
        "light_direction": "soft key light at 45 degrees, professional fill at 50% key intensity",
        "shadow_behavior": "controlled shadows with precise falloff curves",
        "material_response": "all materials optimized for three-dimensional modeling",
        "reflection_quality": "catchlights visible in eyes, specular highlights on textured surfaces",
        "background_interaction": "no light spillage, clean subject separation",
        "atmospheric_density": "climate-controlled, zero air particles",
        "bounce_lighting": "professional reflectors creating fill light with precision",
    }
    
    # Cinematic outdoor physics
    CINEMATIC_OUTDOOR_PHYSICS = {
        "light_direction": "motivated by visible light source (sun, moon, practicals)",
        "shadow_behavior": "consistent shadow angle matching light direction exactly",
        "bounce_lighting": "realistic ground/surface bounce creating fill automatically",
        "atmospheric_density": "motivated air quality (fog, mist, dust, rain particles)",
        "reflection_quality": "environmental reflections on surfaces (water, glass, metal)",
        "material_weathering": "surfaces show environmental interaction (wet, dusty, sun-faded)",
        "temporal_consistency": "lighting and shadows match specific time of day",
        "directional_authenticity": "north-south sun position matches stated time/location",
    }
    
    # Luxury product photography physics
    LUXURY_PRODUCT_PHYSICS = {
        "light_angle": "directional key light at 45 degrees catching material texture",
        "shadow_behavior": "soft feathered shadows emphasizing form without obscuring detail",
        "specular_highlights": "sharp specular highlights on glossy surfaces catching light precisely",
        "material_texture_emphasis": "lighting specifically revealing material quality",
        "surface_interaction": "light interacting realistically with material properties",
        "bounce_light": "subtle bounce revealing surface contours",
        "background_separation": "clean three-dimensional separation through lighting",
    }
    
    # Night/artificial lighting physics
    NIGHT_LIGHTING_PHYSICS = {
        "light_sources": "motivated by visible practicals (neon, LEDs, streetlights)",
        "color_temperature": "cool 5600K-8000K for artificial light, warm 2700K-3200K for practicals",
        "shadow_behavior": "sharp directional shadows from point-source practicals",
        "color_spillage": "realistic color bleeding from colored light sources",
        "atmospheric_particles": "visible atmospheric interaction (fog, smoke, rain)",
        "reflection_quality": "dramatic reflections on wet surfaces, glass, metal",
        "contrast_ratio": "high contrast between lit and shadow areas",
    }
    
    @staticmethod
    def generate_scene_physics_description(
        scenario_type: str,
        time_of_day: Optional[str] = None,
        location_type: Optional[str] = None,
        key_materials: Optional[List[str]] = None,
    ) -> str:
        """
        Generate a scene physics description for realistic coherence.
        
        Args:
            scenario_type: "golden_hour", "studio", "cinematic", "product", "night"
            time_of_day: "morning", "midday", "afternoon", "evening", "night"
            location_type: "indoor", "outdoor", "luxury_venue", "natural_landscape"
            key_materials: ["polished_concrete", "brushed_brass", "silk", "skin"]
            
        Returns:
            Scene physics description incorporating all physical interactions
        """
        physics_template = ""
        
        if scenario_type == "golden_hour":
            physics = ScenePhysics.GOLDEN_HOUR_PHYSICS
            physics_template = (
                f"Low-angle sunset light ({physics['light_angle']}) casting {physics['shadow_direction']} "
                f"with {physics['shadow_behavior']}. {physics['bounce_light']} while "
                f"{physics['atmospheric_density']}. {physics['reflection_quality']} throughout the scene. "
                f"Material response: {physics['material_response']}"
            )
        
        elif scenario_type == "studio":
            physics = ScenePhysics.STUDIO_PHYSICS
            physics_template = (
                f"Professional studio setup: {physics['light_direction']}. "
                f"{physics['shadow_behavior']}. {physics['material_response']}. "
                f"{physics['reflection_quality']}. {physics['background_interaction']}."
            )
        
        elif scenario_type == "product":
            physics = ScenePhysics.LUXURY_PRODUCT_PHYSICS
            physics_template = (
                f"Product lighting optimized for material quality: {physics['light_angle']}. "
                f"{physics['shadow_behavior']} revealing material texture. "
                f"Specular highlights: {physics['specular_highlights']}. "
                f"{physics['material_texture_emphasis']}. {physics['surface_interaction']}."
            )
        
        elif scenario_type == "night":
            physics = ScenePhysics.NIGHT_LIGHTING_PHYSICS
            physics_template = (
                f"Night lighting physics: {physics['light_sources']}. "
                f"Color temperature: {physics['color_temperature']}. "
                f"{physics['shadow_behavior']}. {physics['color_spillage']}. "
                f"{physics['atmospheric_particles']}. {physics['reflection_quality']}."
            )
        
        return physics_template
    
    @staticmethod
    def get_material_physics(material: str) -> Dict[str, str]:
        """Get physics parameters for specific materials."""
        material_physics = {
            "skin": {
                "reflectance": "soft diffuse reflectance with subsurface scattering",
                "light_response": "light penetrating thin skin areas (ears, nostrils, lips)",
                "texture": "micro-scale texture detail visible at close focus",
                "color_response": "warm undertones with slight surface redness",
                "wetness": "subtle perspiration sheen without oil",
            },
            "fabric": {
                "texture": "woven texture catching directional light subtly",
                "reflectance": "diffuse reflectance creating soft shadows",
                "draping": "fabric fold geometry creating natural shadow variation",
                "material_color": "color showing depth through fabric weave",
                "motion_blur": "fabric movement visible in wind interaction",
            },
            "metal": {
                "reflectance": "sharp specular highlights showing surface quality",
                "surface_quality": "reflections revealing surface finish (brushed vs polished)",
                "color_response": "metallic sheen following light direction",
                "oxidation": "subtle oxidation or patina showing age/quality",
                "sharp_reflection": "crisp directional reflection of light sources",
            },
            "glass": {
                "refraction": "realistic light refraction through transparent material",
                "reflection": "Fresnel reflection increasing at shallow angles",
                "surface_detail": "dust particles visible on surface",
                "transmission": "light passing through with color accuracy",
                "distortion": "subtle distortion visible through glass",
            },
            "wood": {
                "grain_pattern": "visible wood grain following growth rings",
                "texture": "surface texture varying from polished to rough",
                "color_variation": "natural color variation in grain",
                "reflection": "matte reflection with slight sheen if varnished",
                "weathering": "authentic wear patterns showing age/quality",
            },
            "concrete": {
                "surface_roughness": "visible surface texture and slight imperfections",
                "aggregate": "visible stone aggregate catching light",
                "weathering": "natural staining and wear patterns",
                "moisture": "subtle moisture marks showing reality",
                "reflection": "minimal reflection, diffuse light absorption",
            },
        }
        
        return material_physics.get(material, {"description": f"Standard {material} physics"})
    
    @staticmethod
    def atmospheric_physics(
        time_of_day: str,
        weather: Optional[str] = None,
        air_quality: Optional[str] = None,
    ) -> str:
        """Generate atmospheric physics description."""
        
        atmosphere_templates = {
            "morning": "cool morning air (4000K color temp) with slight mist, soft diffuse light penetrating particles",
            "midday": "harsh noon light with high contrast shadows, minimal air particles",
            "afternoon": "warm afternoon light (3500K) with light atmospheric haze",
            "evening": "golden hour evening light with warm atmospheric glow, visible light diffusion",
            "night": "cold night air (7000K+) with visible particle interaction from light sources",
        }
        
        weather_additions = {
            "rain": "rain mist diffusing light, wet surfaces creating reflections",
            "fog": "dense fog reducing distant visibility, volumetric light visible",
            "dust": "dust particles catching directional light, visibility reduction",
            "clear": "crystal clear air with minimal particle diffusion",
        }
        
        description = atmosphere_templates.get(time_of_day, "")
        
        if weather and weather in weather_additions:
            description += f"; {weather_additions[weather]}"
        
        return description
