"""Scene-aware styling system that matches costumes and hairstyles to locations.

Ensures attire, hairstyles, and accessories are cohesive with the scene/occasion.
"""

import logging
from typing import Dict, List, Tuple, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class SceneStylingCohesion:
    """Match costumes, hairstyles, and accessories to create coherent scenes."""

    # Scene-specific costume recommendations
    SCENE_ATTIRE_MAP = {
        "beach": {
            "formal": [],
            "semi_formal": ["Light linen dress", "Beach cover-up", "Lightweight kaftan"],
            "casual": ["Swim wear with cover-up", "Light beach dress", "Shorts and beach top", "Casual linen pants"],
            "vibe_keywords": ["light", "breathable", "sun-protection", "breezy"],
        },
        "mountain": {
            "formal": [],
            "semi_formal": ["Hiking dress", "Outdoor adventure outfit"],
            "casual": ["Hiking boots with casual wear", "Adventure jacket", "Trekking pants", "Outdoor casual top"],
            "vibe_keywords": ["rugged", "weather-resistant", "comfortable", "adventurous"],
        },
        "urban": {
            "formal": ["Tailored blazer", "Professional dress", "Business casual outfit"],
            "semi_formal": ["Smart casual dress", "Chic jeans and top", "Urban editorial wear"],
            "casual": ["Street style jeans", "Casual t-shirt", "Urban sneaker outfit", "Casual urban wear"],
            "vibe_keywords": ["trendy", "fashionable", "contemporary", "stylish"],
        },
        "office": {
            "formal": ["Business suit", "Professional dress", "Executive outfit"],
            "semi_formal": ["Business casual", "Professional blouse"],
            "casual": ["Smart casual", "Business casual"],
            "vibe_keywords": ["professional", "polished", "corporate", "formal"],
        },
        "cafe": {
            "formal": [],
            "semi_formal": ["Casual dress", "Nice jeans and blouse"],
            "casual": ["Comfortable casual", "Coffee shop casual", "Relaxed jeans", "Cozy sweater"],
            "vibe_keywords": ["cozy", "relaxed", "intimate", "warm"],
        },
        "garden": {
            "formal": ["Garden party dress", "Elegant gown"],
            "semi_formal": ["Flowy dress", "Garden dress"],
            "casual": ["Sundress", "Casual flowy wear", "Garden casual", "Light dress"],
            "vibe_keywords": ["natural", "flowy", "organic", "elegant"],
        },
        "creative": {
            "formal": ["Artistic statement piece"],
            "semi_formal": ["Creative editorial wear"],
            "casual": ["Artistic casual", "Bohemian wear", "Creative casual", "Artistic expression"],
            "vibe_keywords": ["artistic", "unique", "creative", "experimental"],
        },
        "wedding": {
            "formal": ["Wedding dress", "Formal gown", "Bridal wear"],
            "semi_formal": ["Formal dress", "Evening wear"],
            "casual": ["Wedding guest dress", "Formal casual"],
            "vibe_keywords": ["elegant", "romantic", "formal", "festive"],
        },
        "home": {
            "formal": [],
            "semi_formal": [],
            "casual": ["Comfortable home wear", "Casual loungewear", "Relaxed home outfit", "Cozy indoor wear"],
            "vibe_keywords": ["comfortable", "intimate", "relaxed", "personal"],
        },
        "studio": {
            "formal": ["Editorial studio wear", "High fashion"],
            "semi_formal": ["Studio fashion wear"],
            "casual": ["Studio casual", "Minimal studio outfit", "Statement studio wear"],
            "vibe_keywords": ["minimal", "editorial", "bold", "controlled"],
        },
    }

    # Hairstyle recommendations per scene and costume type
    SCENE_HAIRSTYLE_MAP = {
        "beach": {
            "light": ["Loose waves", "Beach waves", "Half-up bun", "Braided style", "Tousled waves"],
            "jewelry_modern": ["Sleek ponytail", "High bun", "Beachy half-up"],
            "jewelry_traditional": ["Long waves", "Braided crown", "Side braid"],
            "jewelry_statement": ["High ponytail", "Statement updo", "Side-swept waves"],
        },
        "mountain": {
            "practical": ["Tight bun", "Secure braid", "Ponytail", "Practical updo"],
            "adventurous": ["Side braid", "Loose ponytail", "Natural waves"],
            "active": ["Tight ponytail", "Braided bun", "Secured updo"],
        },
        "urban": {
            "trendy": ["Modern textured bob", "Sleek straight", "Styled waves", "Fashion-forward updo"],
            "casual": ["Casual ponytail", "Messy bun", "Natural texture"],
            "editorial": ["High fashion style", "Avant-garde", "Statement hair"],
            "fashion_aware": ["Sleek high pony", "Chic bun", "Styled waves"],
        },
        "office": {
            "professional": ["Sleek bun", "Polished waves", "Professional updo"],
            "business": ["Neat ponytail", "Professional bun", "Polished style"],
            "corporate": ["Executive updo", "Polished waves", "Professional style"],
        },
        "cafe": {
            "relaxed": ["Loose waves", "Soft bun", "Half-up style", "Natural texture"],
            "cozy": ["Messy bun", "Loose waves", "Casual style"],
            "intimate": ["Soft waves", "Half-up bun", "Relaxed style"],
        },
        "garden": {
            "natural": ["Long flowing waves", "Loose braids", "Natural texture"],
            "flowy": ["Half-up flower crown", "Loose waves", "Braided style"],
            "organic": ["Loose braids", "Natural waves", "Garden crown"],
        },
        "creative": {
            "artistic": ["Avant-garde style", "Experimental updo", "Artistic arrangement"],
            "bohemian": ["Bohemian braid", "Flower crown", "Free-flowing"],
            "unique": ["Unique styling", "Creative arrangement", "Statement hair"],
        },
        "wedding": {
            "formal": ["Formal updo", "Bridal bun", "Elegant updos"],
            "romantic": ["Soft curls", "Romance bun", "Bride hairstyle"],
            "festive": ["Formal updo", "Ornate style", "Celebration hair"],
        },
        "home": {
            "comfortable": ["Natural texture", "Casual bun", "Relaxed waves"],
            "intimate": ["Soft waves", "Loose hair", "Natural style"],
            "relaxed": ["Natural texture", "Casual updo", "Comfortable style"],
        },
        "studio": {
            "minimal": ["Sleek style", "Minimal updo", "Clean lines"],
            "editorial": ["Fashion editorial", "Bold style", "Controlled look"],
            "bold": ["Statement style", "Strong presence", "Bold arrangement"],
        },
    }

    # Accessories that complement each scene
    SCENE_ACCESSORIES_MAP = {
        "beach": {
            "suggested": ["sunglasses", "beach hat", "minimal jewelry", "shell accessories"],
            "avoid": ["heavy jewelry", "formal accessories", "bulky bags"],
        },
        "mountain": {
            "suggested": ["practical backpack", "trekking watch", "hiking accessories"],
            "avoid": ["delicate jewelry", "formal accessories", "high heels"],
        },
        "urban": {
            "suggested": ["stylish bag", "sunglasses", "statement jewelry", "urban accessories"],
            "avoid": ["overly casual", "mismatched", "outdoor gear"],
        },
        "office": {
            "suggested": ["professional bag", "subtle jewelry", "formal watch"],
            "avoid": ["casual bags", "statement jewelry", "outdoor gear"],
        },
        "cafe": {
            "suggested": ["casual bag", "subtle jewelry", "simple accessories"],
            "avoid": ["formal accessories", "bulky bags", "statement pieces"],
        },
        "garden": {
            "suggested": ["flower crown", "delicate jewelry", "garden accessories"],
            "avoid": ["heavy jewelry", "formal bags", "industrial accessories"],
        },
        "creative": {
            "suggested": ["artistic pieces", "unique jewelry", "creative accessories"],
            "avoid": ["mainstream", "conventional", "formal pieces"],
        },
        "wedding": {
            "suggested": ["bridal jewelry", "formal accessories", "elegant pieces"],
            "avoid": ["casual items", "mismatched", "outdoor gear"],
        },
        "home": {
            "suggested": ["minimal jewelry", "comfortable accessories"],
            "avoid": ["formal pieces", "outdoor gear", "heavy accessories"],
        },
        "studio": {
            "suggested": ["curated pieces", "editorial jewelry", "controlled accessories"],
            "avoid": ["casual items", "clashing accessories", "outdoor wear"],
        },
    }

    @staticmethod
    def get_scene_category(location: str) -> str:
        """Categorize location into one of our scene types."""
        location_lower = location.lower()

        location_map = {
            "beach": ["beach", "sea", "shore", "coast", "ocean", "seaside"],
            "mountain": ["mountain", "hill", "peak", "alpine", "hiking", "trail"],
            "urban": ["city", "urban", "street", "downtown", "metro", "building"],
            "office": ["office", "corporate", "business", "work", "workplace"],
            "cafe": ["cafe", "coffee", "restaurant", "bistro", "bar", "lounge"],
            "garden": ["garden", "park", "nature", "outdoor", "natural", "green"],
            "creative": ["creative", "artistic", "gallery", "studio", "art"],
            "wedding": ["wedding", "ceremony", "bride", "groom", "marriage"],
            "home": ["home", "indoor", "room", "house", "domestic"],
            "studio": ["studio", "backdrop", "blank", "controlled"],
        }

        for scene, keywords in location_map.items():
            if any(keyword in location_lower for keyword in keywords):
                return scene

        return "studio"  # Default fallback

    @staticmethod
    def get_formal_level(user_context: str, mood: str) -> str:
        """Determine formality level based on context and mood."""
        context_lower = (user_context or "").lower()
        mood_lower = (mood or "").lower()

        formal_keywords = ["formal", "wedding", "ceremony", "professional", "corporate", "business", "executive"]
        casual_keywords = ["casual", "relaxed", "chill", "fun", "playful", "beach", "park"]

        if any(keyword in context_lower or keyword in mood_lower for keyword in formal_keywords):
            return "formal"
        elif any(keyword in context_lower or keyword in mood_lower for keyword in casual_keywords):
            return "casual"
        else:
            return "semi_formal"

    @staticmethod
    def get_cohesive_styling(
        location: str,
        mood: str,
        user_context: str,
        blend_level: str = "50/50",
        jewelry_style: str = "fusion",
    ) -> Dict[str, any]:
        """Get cohesive costume, hairstyle, and accessories for a scene.

        Args:
            location: Primary location (beach, mountain, urban, etc.)
            mood: Mood/vibe (relaxed, energetic, professional, etc.)
            user_context: User's full requirement text
            blend_level: Aesthetic blend preference
            jewelry_style: Jewelry style preference

        Returns:
            Dictionary with costume, hairstyle, accessories, and styling notes
        """
        scene = SceneStylingCohesion.get_scene_category(location)
        formal_level = SceneStylingCohesion.get_formal_level(user_context, mood)

        # Get attire recommendations
        scene_attire = SceneStylingCohesion.SCENE_ATTIRE_MAP.get(scene, {})
        attire_options = scene_attire.get(formal_level, scene_attire.get("casual", []))

        # Select hairstyle based on scene and mood
        hairstyle_key = mood.lower() if mood else "relaxed"
        scene_hairstyles = SceneStylingCohesion.SCENE_HAIRSTYLE_MAP.get(scene, {})
        hairstyle_options = scene_hairstyles.get(hairstyle_key, [])

        # If no hairstyles for mood, use jewelry style as fallback
        if not hairstyle_options and jewelry_style:
            jewelry_key = f"jewelry_{jewelry_style.lower()}"
            hairstyle_options = scene_hairstyles.get(jewelry_key, [])

        # Default fallback
        if not hairstyle_options:
            hairstyle_options = list(scene_hairstyles.values())[0] if scene_hairstyles else ["Styled appropriately"]

        # Get accessories
        accessories = SceneStylingCohesion.SCENE_ACCESSORIES_MAP.get(scene, {})
        suggested_accessories = accessories.get("suggested", [])
        avoid_accessories = accessories.get("avoid", [])

        # Get vibe keywords
        vibe_keywords = scene_attire.get("vibe_keywords", [])

        return {
            "scene": scene,
            "formal_level": formal_level,
            "attire_options": attire_options[:3],  # Top 3 options
            "hairstyle_options": hairstyle_options[:5],  # Top 5 options
            "suggested_accessories": suggested_accessories,
            "avoid_accessories": avoid_accessories,
            "vibe_keywords": vibe_keywords,
            "styling_notes": SceneStylingCohesion._generate_styling_notes(
                scene, formal_level, mood, blend_level, jewelry_style
            )
        }

    @staticmethod
    def _generate_styling_notes(
        scene: str,
        formal_level: str,
        mood: str,
        blend_level: str,
        jewelry_style: str,
    ) -> str:
        """Generate coherent styling notes for the prompt."""

        notes = []

        # Formality note
        if formal_level == "formal":
            notes.append("Formal, polished presentation with refined styling")
        elif formal_level == "casual":
            notes.append("Casual, relaxed styling with comfortable aesthetic")
        else:
            notes.append("Semi-formal presentation balancing elegance and comfort")

        # Mood note
        mood_lower = mood.lower() if mood else ""
        if "professional" in mood_lower or "business" in mood_lower:
            notes.append("Professional demeanor with corporate polish")
        elif "artistic" in mood_lower or "creative" in mood_lower:
            notes.append("Artistic expression with creative flair")
        elif "nature" in mood_lower or "natural" in mood_lower:
            notes.append("Natural, organic aesthetic reflecting harmony with environment")
        elif "relaxed" in mood_lower:
            notes.append("Relaxed comfort with approachable style")

        # Blend note
        if "traditional" in blend_level.lower():
            notes.append("Respectful of cultural elements with traditional touches")
        elif "modern" in blend_level.lower():
            notes.append("Contemporary styling with modern aesthetics")
        else:
            notes.append("Balanced fusion blending traditional and modern elements")

        # Scene coordination
        scene_notes = {
            "beach": "All styling should appear lightweight and sun-appropriate, avoiding heat-heavy fabrics",
            "mountain": "Attire should be practical and weather-resistant while maintaining style",
            "urban": "Styling should reflect current fashion trends and urban sophistication",
            "office": "Professional coordination with business-appropriate styling throughout",
            "garden": "Natural flow and elegance in keeping with organic surroundings",
            "wedding": "Formal elegance and refinement appropriate for celebration",
            "studio": "Controlled, editorial presentation with intentional styling choices",
        }

        if scene in scene_notes:
            notes.append(scene_notes[scene])

        return " | ".join(notes)

    @staticmethod
    def build_styling_prompt_section(
        location: str,
        mood: str,
        user_context: str,
        blend_level: str = "50/50",
        jewelry_style: str = "fusion",
    ) -> str:
        """Build a comprehensive styling section for image generation prompts.

        Returns formatted markdown section with costume, hairstyle, and accessories guidance.
        """
        styling = SceneStylingCohesion.get_cohesive_styling(
            location, mood, user_context, blend_level, jewelry_style
        )

        section = f"""
👗 COHESIVE STYLING & COSTUME COORDINATION:

📋 Scene Analysis:
Location: {styling['scene'].upper()}
Formality Level: {styling['formal_level'].title()}
Mood/Vibe: {mood}

🎽 ATTIRE RECOMMENDATIONS (Choose from context):
"""
        for i, attire in enumerate(styling['attire_options'], 1):
            section += f"   {i}. {attire}\n"

        section += f"""
💇 HAIRSTYLE COORDINATION (Select one that complements attire):
"""
        for i, hair in enumerate(styling['hairstyle_options'], 1):
            section += f"   {i}. {hair}\n"

        section += f"""
✨ ACCESSORIES & JEWELRY:
Suggested: {', '.join(styling['suggested_accessories'])}
Avoid: {', '.join(styling['avoid_accessories'])}

🎨 STYLING VIBE KEYWORDS:
{', '.join(styling['vibe_keywords'])}

📝 OVERALL STYLING NOTES:
{styling['styling_notes']}

⚠️ CRITICAL STYLING REQUIREMENTS:
✓ Attire, hairstyle, and accessories MUST coordinate as a cohesive unit
✓ All styling choices MUST match the {styling['scene'].upper()} location context
✓ Formality level of ALL elements MUST be {styling['formal_level']}
✓ NO mismatched styles or contradictory fashion choices
✓ Styling should enhance the {mood} mood naturally
✓ GARMENT FIT: Every outfit MUST be realistically tailored/fitted to the subject's actual body type, size, and build exactly as shown in the reference photo — NOT draped on a generic, idealized, or different body shape
✓ NO substituting a different/idealized body silhouette to "fit" the costume better — the costume must be described as fitting the real person's proportions (shoulders, waist, hips, height) as-is
"""

        return section
