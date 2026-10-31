"""Flexible aesthetic preference system - blend-based, not category-locked.

Supports infinite blend of traditional, modern, and fusion aesthetics without
forcing users into rigid Indian/Western categories.
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum


class BlendLevel(Enum):
    """Attire blend preference from traditional to modern."""
    FULLY_TRADITIONAL = "100% Traditional"  # Pure traditional aesthetics
    MOSTLY_TRADITIONAL = "80% Traditional"  # Mostly traditional, slight modern
    BLEND_TRADITIONAL = "60% Traditional"   # Balanced with traditional leaning
    HALF_BLEND = "50/50 Blend"             # Perfect half-half blend
    MOSTLY_MODERN = "60% Modern"           # Mostly modern with traditional touches
    FULLY_MODERN = "100% Modern"           # Pure contemporary
    FUSION_FOCUS = "Fusion Focus"          # Deliberately blended global styles


class JewelryStyle(Enum):
    """Jewelry preference spectrum."""
    MINIMAL = "minimal"              # Single delicate piece or none
    MODERATE = "moderate"            # Coordinated jewelry set
    STATEMENT = "statement"          # Bold statement pieces
    LAYERED = "layered"             # Multiple layered pieces
    TRADITIONAL = "traditional"      # Cultural/traditional jewelry
    MODERN = "modern"               # Contemporary minimalist
    FUSION = "fusion"               # Mix of traditional and modern


class MakeupVibe(Enum):
    """Makeup style preference."""
    NATURAL = "natural"              # Minimal makeup, fresh face
    BOLD = "bold"                   # Dramatic colors, artistic
    MINIMALIST = "minimalist"        # Clean lines, subtle
    TRADITIONAL = "traditional"      # Cultural makeup (kohl, bindi, etc.)
    MODERN = "modern"               # Contemporary makeup trends
    EDITORIAL = "editorial"          # High fashion, avant-garde
    FUSION = "fusion"               # Mix traditional and modern elements


class ColorPalette(Enum):
    """Color preference spectrum."""
    VIBRANT_WARM = "vibrant_warm"           # Red, orange, gold, warm tones
    JEWEL_TONES = "jewel_tones"            # Deep purple, emerald, sapphire
    EARTH_TONES = "earth_tones"            # Beige, olive, terracotta, cream
    COOL_PASTELS = "cool_pastels"          # Soft blues, lavender, blush
    BOLD_MONOCHROME = "bold_monochrome"    # Pure black, pure white, solid bold
    RAINBOW_FUSION = "rainbow_fusion"      # Multi-color, playful, artistic
    NEUTRAL = "neutral"                    # Grays, blacks, whites, neutrals


class AestheticPreferences:
    """User aesthetic preferences for prompt generation."""

    def __init__(
        self,
        blend_level: BlendLevel = BlendLevel.HALF_BLEND,
        jewelry_style: JewelryStyle = JewelryStyle.FUSION,
        makeup_vibe: MakeupVibe = MakeupVibe.MODERN,
        color_palette: ColorPalette = ColorPalette.JEWEL_TONES,
        occasion: str = "casual",
        culture_influences: Optional[List[str]] = None,
        custom_preferences: Optional[Dict[str, str]] = None,
    ):
        """Initialize aesthetic preferences.

        Args:
            blend_level: Traditional to modern spectrum
            jewelry_style: Jewelry preference
            makeup_vibe: Makeup style
            color_palette: Color preference
            occasion: Context (professional, casual, festive, wedding, creative)
            culture_influences: List of cultural influences (indian, western, asian, etc.)
            custom_preferences: Additional custom preferences
        """
        self.blend_level = blend_level
        self.jewelry_style = jewelry_style
        self.makeup_vibe = makeup_vibe
        self.color_palette = color_palette
        self.occasion = occasion.lower()
        self.culture_influences = culture_influences or ["global"]
        self.custom_preferences = custom_preferences or {}

    def to_dict(self) -> Dict[str, str]:
        """Convert preferences to dictionary."""
        return {
            "blend_level": self.blend_level.value,
            "jewelry_style": self.jewelry_style.value,
            "makeup_vibe": self.makeup_vibe.value,
            "color_palette": self.color_palette.value,
            "occasion": self.occasion,
            "culture_influences": self.culture_influences,
            **self.custom_preferences,
        }


# ============================================================================
# ATTIRE LIBRARY - Global, Blended, Fusion-Focused
# ============================================================================

ATTIRE_POOL = {
    # Traditional Indian
    "indian_traditional": {
        "formal": [
            "Silk saree with traditional blouse",
            "Embroidered lehenga",
            "Anarkali with dupatta",
            "Formal Salwar Kameez with dupatta",
        ],
        "casual": [
            "Cotton saree",
            "Simple lehenga",
            "Casual kurti",
            "Everyday Salwar Kameez",
        ],
        "festive": [
            "Silk bridal saree",
            "Embroidered festive lehenga",
            "Festival kurta",
            "Gold-adorned festive saree",
        ],
    },

    # Modern Indian (Contemporary with traditional roots)
    "indian_modern": {
        "formal": [
            "Saree with contemporary blouse design",
            "Modern lehenga with current fabric",
            "Fusion dress with Indian embroidery",
            "Modern kurta dress",
            "Saree with minimalist blouse",
        ],
        "casual": [
            "Casual kurti with jeans",
            "Saree-inspired wrap",
            "Embroidered modern shirt",
            "Printed contemporary kurti",
        ],
        "streetwear": [
            "Indian street fashion mix",
            "Kurta with sneakers",
            "Saree with modern accessories",
        ],
    },

    # Western Classic
    "western_classic": {
        "formal": [
            "Blazer and formal trousers",
            "Formal evening dress",
            "Gown",
            "Sophisticated business suit",
        ],
        "casual": [
            "Jeans and stylish top",
            "T-shirt and denim",
            "Casual dress",
            "Comfortable loungewear style",
        ],
        "professional": [
            "Business suit",
            "Business casual dress",
            "Professional blazer outfit",
        ],
    },

    # Modern Western (Contemporary)
    "western_modern": {
        "fashion_forward": [
            "Trendy contemporary outfit",
            "Designer modern wear",
            "Fashion-forward streetwear",
            "Current trending style",
        ],
        "minimalist": [
            "Neutral monochrome outfit",
            "Minimalist clean lines",
            "Simple elegant modern",
            "Understated contemporary",
        ],
        "bold": [
            "Statement piece outfit",
            "Contrasting color combination",
            "Artistic bold wear",
            "Fashion statement look",
        ],
    },

    # Global Fusion (Deliberately blended)
    "global_fusion": {
        "east_meets_west": [
            "Saree with crop top modern style",
            "Lehenga with contemporary silhouette",
            "Kurta with Western trousers",
            "Indian fabric with modern cut design",
            "Saree-inspired dress with Western construction",
        ],
        "asian_fusion": [
            "Chinese-inspired with Indian elements",
            "Japanese minimal with Indian jewelry",
            "Korean contemporary with Indian accessories",
            "Southeast Asian fusion",
        ],
        "bohemian": [
            "Boho dress with cultural jewelry",
            "Mix of patterns and cultural elements",
            "Free-spirited global fusion",
            "Artistic cultural blend",
        ],
        "african_fusion": [
            "African print with Indian jewelry",
            "African wrap with modern styling",
            "African fabric with contemporary cut",
        ],
    },
}


def get_attire_for_blend(
    blend_level: BlendLevel,
    occasion: str,
) -> List[str]:
    """Get attire options for user's blend preference.

    Args:
        blend_level: User's tradition-to-modern spectrum
        occasion: Context (formal, casual, festive, etc.)

    Returns:
        List of attire options appropriate for blend level
    """
    attire_options = []

    # Map blend level to attire pools
    blend_mapping = {
        BlendLevel.FULLY_TRADITIONAL: ["indian_traditional"],
        BlendLevel.MOSTLY_TRADITIONAL: ["indian_traditional", "indian_modern"],
        BlendLevel.BLEND_TRADITIONAL: ["indian_traditional", "indian_modern", "global_fusion"],
        BlendLevel.HALF_BLEND: ["indian_modern", "global_fusion", "western_modern"],
        BlendLevel.MOSTLY_MODERN: ["indian_modern", "western_modern", "global_fusion"],
        BlendLevel.FULLY_MODERN: ["western_modern", "western_classic"],
        BlendLevel.FUSION_FOCUS: ["global_fusion", "indian_modern", "western_modern"],
    }

    # Get pools for this blend level
    pools = blend_mapping.get(blend_level, ["global_fusion"])

    # Collect attire options from each pool
    for pool_name in pools:
        pool = ATTIRE_POOL.get(pool_name, {})
        # Get relevant category from pool
        for category in ["formal", "casual", "festive", "streetwear", "professional",
                        "fashion_forward", "minimalist", "bold", "east_meets_west",
                        "asian_fusion", "bohemian", "african_fusion"]:
            if category in pool:
                attire_options.extend(pool[category])

    return list(set(attire_options))  # Remove duplicates


# ============================================================================
# JEWELRY & ACCESSORIES LIBRARY
# ============================================================================

JEWELRY_POOL = {
    "metals": {
        "gold": ["Gold tone", "Rose gold", "Yellow gold", "Antique gold"],
        "silver": ["Silver tone", "Platinum", "White gold", "Oxidized silver"],
        "mixed": ["Gold and silver combination", "Mixed metal blend"],
        "alternative": ["Copper", "Bronze", "Beaded", "Wooden"],
    },

    "traditional_indian": [
        "Mangalsutra",
        "Temple jewelry",
        "Kundan jewelry",
        "Polki jewelry",
        "Intricate filigree",
        "Stone-studded jewelry",
    ],

    "modern_minimal": [
        "Delicate gold studs",
        "Simple necklace",
        "Minimal bracelet",
        "Single elegant piece",
        "Thin bands",
    ],

    "statement": [
        "Statement necklace",
        "Chunky bracelets",
        "Bold earrings",
        "Dramatic pieces",
        "Eye-catching jewelry",
    ],

    "fusion": [
        "Layered necklaces",
        "Mixed metal jewelry",
        "Traditional meets modern",
        "Beaded with metal",
        "Contemporary traditional",
    ],

    "bindi_options": {
        "traditional": [
            "Red vermillion bindi",
            "Gold traditional bindi",
            "Black bindi",
            "Maroon bindi",
        ],
        "modern": [
            "Minimalist dot bindi",
            "Decorative sticker bindi",
            "Jeweled bindi",
            "Colored contemporary bindi",
        ],
        "statement": [
            "Elaborate stone-studded bindi",
            "Artistic design bindi",
            "Large decorative bindi",
            "Ornate traditional bindi",
        ],
    },
}


def get_jewelry_for_style(
    jewelry_style: JewelryStyle,
    attire_description: str,
) -> Dict[str, List[str]]:
    """Get jewelry recommendation for style preference.

    Args:
        jewelry_style: User's jewelry preference
        attire_description: Description of attire for coordination

    Returns:
        Dictionary with jewelry recommendations
    """
    recommendations = {
        "pieces": [],
        "metals": [],
        "bindi": None,
        "coordination_notes": "",
    }

    if jewelry_style == JewelryStyle.MINIMAL:
        recommendations["pieces"] = JEWELRY_POOL["modern_minimal"]
        recommendations["metals"] = JEWELRY_POOL["metals"]["gold"]
        recommendations["bindi"] = "Optional, minimal if worn"
        recommendations["coordination_notes"] = "Single delicate piece, understated elegance"

    elif jewelry_style == JewelryStyle.MODERATE:
        recommendations["pieces"] = JEWELRY_POOL["modern_minimal"] + JEWELRY_POOL["fusion"]
        recommendations["metals"] = JEWELRY_POOL["metals"]["gold"]
        recommendations["bindi"] = JEWELRY_POOL["bindi_options"]["modern"]
        recommendations["coordination_notes"] = "Coordinated set, balanced aesthetic"

    elif jewelry_style == JewelryStyle.STATEMENT:
        recommendations["pieces"] = JEWELRY_POOL["statement"]
        recommendations["metals"] = JEWELRY_POOL["metals"]["gold"]
        recommendations["bindi"] = JEWELRY_POOL["bindi_options"]["statement"]
        recommendations["coordination_notes"] = "Bold eye-catching pieces"

    elif jewelry_style == JewelryStyle.LAYERED:
        recommendations["pieces"] = JEWELRY_POOL["fusion"]
        recommendations["metals"] = JEWELRY_POOL["metals"]["mixed"]
        recommendations["bindi"] = JEWELRY_POOL["bindi_options"]["modern"]
        recommendations["coordination_notes"] = "Layered with mixed metals"

    elif jewelry_style == JewelryStyle.TRADITIONAL:
        recommendations["pieces"] = JEWELRY_POOL["traditional_indian"]
        recommendations["metals"] = JEWELRY_POOL["metals"]["gold"]
        recommendations["bindi"] = JEWELRY_POOL["bindi_options"]["traditional"]
        recommendations["coordination_notes"] = "Authentic cultural jewelry"

    elif jewelry_style == JewelryStyle.MODERN:
        recommendations["pieces"] = JEWELRY_POOL["modern_minimal"]
        recommendations["metals"] = JEWELRY_POOL["metals"]["silver"]
        recommendations["bindi"] = "No bindi or minimal contemporary"
        recommendations["coordination_notes"] = "Contemporary minimalist"

    elif jewelry_style == JewelryStyle.FUSION:
        recommendations["pieces"] = (
            JEWELRY_POOL["traditional_indian"]
            + JEWELRY_POOL["modern_minimal"]
            + JEWELRY_POOL["fusion"]
        )
        recommendations["metals"] = JEWELRY_POOL["metals"]["gold"]
        recommendations["bindi"] = JEWELRY_POOL["bindi_options"]["modern"]
        recommendations["coordination_notes"] = "Blend traditional and modern"

    return recommendations


# ============================================================================
# MAKEUP & HAIR STYLES
# ============================================================================

MAKEUP_STYLES = {
    "natural": "Minimal makeup, fresh face, natural tones, effortless look",
    "bold": "Dramatic colors, defined eyes, artistic expression, smoky effect",
    "minimalist": "Clean lines, subtle colors, understated professional elegance",
    "traditional": "Kajal (kohl), cultural makeup elements, traditional approach",
    "modern": "Contemporary makeup trends, defined brows, modern techniques",
    "editorial": "High fashion artistic, avant-garde, experimental makeup",
    "fusion": "Light kohl + modern eye makeup + optional subtle bindi",
}

HAIR_STYLES = {
    "loose_waves": "Loose waves, cascading, flowing, soft",
    "structured": "Sleek bun, ponytail, half-up, neat braids",
    "braided": "Traditional braids, possibly with flowers or jewelry",
    "half_up": "Half-up style, romantic, balanced",
    "artistic": "Undercut, colored, textured, experimental",
    "casual": "Casual waves, undone elegance, relaxed",
    "formal": "Updo, sleek styling, polished professional",
}


def get_makeup_for_vibe(makeup_vibe: MakeupVibe) -> str:
    """Get makeup description for user's vibe preference."""
    return MAKEUP_STYLES.get(makeup_vibe.value, MAKEUP_STYLES["modern"])


def get_hair_for_occasion(occasion: str, blend_level: BlendLevel) -> str:
    """Get hair style recommendation for occasion and blend preference."""
    if blend_level in [BlendLevel.FULLY_TRADITIONAL, BlendLevel.MOSTLY_TRADITIONAL]:
        return "Traditional braids with flowers and jewelry"
    elif blend_level == BlendLevel.HALF_BLEND:
        return "Balanced hairstyle - braids or loose waves with modern twist"
    elif blend_level in [BlendLevel.MOSTLY_MODERN, BlendLevel.FULLY_MODERN]:
        return "Contemporary styled hair - waves, bun, or artistic styling"
    else:
        return "Fusion hairstyle - modern cut with traditional elements"


# ============================================================================
# COLOR PALETTES
# ============================================================================

COLOR_PALETTES = {
    ColorPalette.VIBRANT_WARM: {
        "colors": ["Red", "Orange", "Gold", "Warm pink", "Warm brown"],
        "mood": "Energetic, warm, celebratory, vibrant",
        "best_for": ["Festive", "Wedding", "Creative"],
    },
    ColorPalette.JEWEL_TONES: {
        "colors": ["Deep purple", "Emerald", "Sapphire", "Burgundy", "Teal"],
        "mood": "Elegant, luxurious, sophisticated, rich",
        "best_for": ["Professional", "Formal", "Evening"],
    },
    ColorPalette.EARTH_TONES: {
        "colors": ["Beige", "Taupe", "Olive", "Terracotta", "Cream"],
        "mood": "Natural, grounded, understated, organic",
        "best_for": ["Casual", "Bohemian", "Natural"],
    },
    ColorPalette.COOL_PASTELS: {
        "colors": ["Soft blue", "Lavender", "Pale green", "Blush", "Powder pink"],
        "mood": "Soft, dreamy, contemporary, delicate",
        "best_for": ["Modern", "Minimalist", "Contemporary"],
    },
    ColorPalette.BOLD_MONOCHROME: {
        "colors": ["Pure black", "Pure white", "Solid color statement"],
        "mood": "Bold, dramatic, powerful, artistic",
        "best_for": ["Fashion", "Editorial", "Statement"],
    },
    ColorPalette.RAINBOW_FUSION: {
        "colors": ["Multi-color blend", "Contrasting colors", "Colorful mix"],
        "mood": "Playful, artistic, expressive, joyful",
        "best_for": ["Creative", "Festival", "Artistic"],
    },
    ColorPalette.NEUTRAL: {
        "colors": ["Gray", "Black", "White", "Neutral tones"],
        "mood": "Professional, minimal, timeless, clean",
        "best_for": ["Professional", "Minimal", "Corporate"],
    },
}


def get_color_palette_for_occasion(
    color_palette: ColorPalette,
    occasion: str,
) -> Dict[str, any]:
    """Get color palette details."""
    return COLOR_PALETTES.get(
        color_palette,
        COLOR_PALETTES[ColorPalette.NEUTRAL],
    )
