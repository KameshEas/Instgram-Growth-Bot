"""Context-aware component defaults based on niche, follower count, and region.

Replaces hardcoded fallback values in formulas.py with intelligent defaults that vary
by user context. This enables niche-specific prompt generation without requiring
every user to specify every component.
"""

from typing import Dict, Any, Optional
from enum import Enum


class FollowerTier(Enum):
    """Follower count tiers for context-aware defaults."""
    MICRO = "micro"  # < 10k
    MID = "mid"  # 10k-100k
    MACRO = "macro"  # > 100k


def get_follower_tier(follower_count: Optional[int]) -> FollowerTier:
    """Classify follower count into a tier."""
    if not follower_count or follower_count < 10000:
        return FollowerTier.MICRO
    elif follower_count < 100000:
        return FollowerTier.MID
    else:
        return FollowerTier.MACRO


# ============================================================================
# NICHE-SPECIFIC EMOTION DEFAULTS
# ============================================================================
EMOTION_DEFAULTS_BY_NICHE = {
    "fitness": {
        "micro": "determined, focused, powerful",
        "mid": "energetic, inspired, confident",
        "macro": "aspirational, commanding, magnetic",
    },
    "fashion": {
        "micro": "poised, fashionable, approachable",
        "mid": "elegant, sophisticated, trendy",
        "macro": "iconic, haute-couture, runway-ready",
    },
    "photography": {
        "micro": "artistic, contemplative, authentic",
        "mid": "professional, composed, expressive",
        "macro": "editorial, dramatic, captivating",
    },
    "lifestyle": {
        "micro": "genuine, relatable, warm",
        "mid": "aspirational, polished, curated",
        "macro": "luxurious, enviable, aspirational",
    },
    "beauty": {
        "micro": "fresh, natural, glowing",
        "mid": "radiant, flawless, glamorous",
        "macro": "luminous, editorial, red-carpet-ready",
    },
    "food": {
        "micro": "inviting, appetizing, homey",
        "mid": "professional, culinary, refined",
        "macro": "gourmet, restaurant-quality, Michelin-standard",
    },
    "travel": {
        "micro": "adventurous, curious, authentic",
        "mid": "worldly, sophisticated, well-traveled",
        "macro": "iconic, exploration, bucket-list-worthy",
    },
    "default": {
        "micro": "natural, genuine, approachable",
        "mid": "professional, polished, engaging",
        "macro": "commanding, influential, iconic",
    },
}

# ============================================================================
# NICHE-SPECIFIC LIGHTING DEFAULTS
# ============================================================================
LIGHTING_DEFAULTS_BY_NICHE = {
    "fitness": {
        "micro": "bright, energetic key light",
        "mid": "studio portrait lighting, dramatic shadows",
        "macro": "professional multi-key lighting, cinematic",
    },
    "fashion": {
        "micro": "soft key light with highlights",
        "mid": "high-key fashion lighting, editorial",
        "macro": "runway lighting, dramatic directional key",
    },
    "photography": {
        "micro": "natural window light",
        "mid": "carefully controlled studio lighting",
        "macro": "professional studio three-point setup",
    },
    "lifestyle": {
        "micro": "soft, diffused natural light",
        "mid": "warm studio lighting with fill light",
        "macro": "cinematic golden-hour professional lighting",
    },
    "beauty": {
        "micro": "bright, flat beauty lighting",
        "mid": "professional beauty light with fill",
        "macro": "high-end beauty studio lighting, diffused",
    },
    "default": {
        "micro": "soft, diffused light",
        "mid": "professional studio lighting",
        "macro": "cinematic professional lighting",
    },
}

# ============================================================================
# NICHE-SPECIFIC CAMERA ANGLE DEFAULTS
# ============================================================================
CAMERA_ANGLE_DEFAULTS_BY_NICHE = {
    "fitness": {
        "micro": "full-body side angle",
        "mid": "three-quarter front angle, powerful",
        "macro": "dynamic diagonal composition",
    },
    "fashion": {
        "micro": "full-length front angle",
        "mid": "three-quarter angled fashion pose",
        "macro": "high-fashion runway angle",
    },
    "photography": {
        "micro": "standard eye-level angle",
        "mid": "35mm portrait focal length feel",
        "macro": "85mm cinematic portrait angle",
    },
    "lifestyle": {
        "micro": "casual mid-shot angle",
        "mid": "effortless three-quarter angle",
        "macro": "editorial wide-angle lifestyle",
    },
    "beauty": {
        "micro": "straight-on beauty angle",
        "mid": "slightly elevated flattering angle",
        "macro": "professional beauty close-up angle",
    },
    "default": {
        "micro": "eye-level portrait angle",
        "mid": "three-quarter angled composition",
        "macro": "cinematic dramatic angle",
    },
}

# ============================================================================
# NICHE-SPECIFIC BACKGROUND DEFAULTS
# ============================================================================
BACKGROUND_DEFAULTS_BY_NICHE = {
    "fitness": {
        "micro": "gym or outdoor training setting",
        "mid": "professional fitness studio background",
        "macro": "high-end luxury fitness facility",
    },
    "fashion": {
        "micro": "minimal neutral backdrop",
        "mid": "editorial fashion background",
        "macro": "luxury high-fashion runway environment",
    },
    "photography": {
        "micro": "natural environment",
        "mid": "professionally curated backdrop",
        "macro": "iconic location or luxury setting",
    },
    "lifestyle": {
        "micro": "relatable home or casual setting",
        "mid": "curated lifestyle environment",
        "macro": "luxury home or exclusive location",
    },
    "beauty": {
        "micro": "clean neutral background",
        "mid": "professional beauty studio backdrop",
        "macro": "high-end luxury background",
    },
    "travel": {
        "micro": "authentic local landmark",
        "mid": "iconic travel destination",
        "macro": "exclusive luxury travel location",
    },
    "food": {
        "micro": "home kitchen or casual café",
        "mid": "restaurant-quality food photography setting",
        "macro": "Michelin-star restaurant environment",
    },
    "default": {
        "micro": "neutral complementary background",
        "mid": "professional curated background",
        "macro": "luxury high-end background",
    },
}

# ============================================================================
# REGION-SPECIFIC COLOR PALETTE DEFAULTS
# ============================================================================
COLOR_PALETTE_DEFAULTS_BY_REGION = {
    "north_america": "warm golden tones, muted pastels, earth tones",
    "europe": "sophisticated neutrals, muted jewel tones, creams",
    "asia": "vibrant saturated colors, rich jewel tones, bold contrasts",
    "south_america": "warm vivid colors, tropical saturation, passionate hues",
    "africa": "rich earthy tones, bold warm colors, natural pigments",
    "default": "warm balanced tones, sophisticated palette, complementary colors",
}

# ============================================================================
# CONTEXT-AWARE COMPONENT BUILDER
# ============================================================================


class ContextAwareComponentDefaults:
    """Provides context-aware default values for prompt components."""

    @staticmethod
    def get_emotion_adjectives(
        niche: Optional[str] = None,
        follower_count: Optional[int] = None,
    ) -> str:
        """Get emotion adjectives matching user niche and tier."""
        niche = (niche or "default").lower().strip()
        tier = get_follower_tier(follower_count).value

        niche_map = EMOTION_DEFAULTS_BY_NICHE.get(niche)
        if not niche_map:
            niche_map = EMOTION_DEFAULTS_BY_NICHE["default"]

        return niche_map.get(tier, niche_map.get("micro"))

    @staticmethod
    def get_lighting_style(
        niche: Optional[str] = None,
        follower_count: Optional[int] = None,
    ) -> str:
        """Get lighting style matching user niche and tier."""
        niche = (niche or "default").lower().strip()
        tier = get_follower_tier(follower_count).value

        niche_map = LIGHTING_DEFAULTS_BY_NICHE.get(niche)
        if not niche_map:
            niche_map = LIGHTING_DEFAULTS_BY_NICHE["default"]

        return niche_map.get(tier, niche_map.get("micro"))

    @staticmethod
    def get_camera_angle(
        niche: Optional[str] = None,
        follower_count: Optional[int] = None,
    ) -> str:
        """Get camera angle matching user niche and tier."""
        niche = (niche or "default").lower().strip()
        tier = get_follower_tier(follower_count).value

        niche_map = CAMERA_ANGLE_DEFAULTS_BY_NICHE.get(niche)
        if not niche_map:
            niche_map = CAMERA_ANGLE_DEFAULTS_BY_NICHE["default"]

        return niche_map.get(tier, niche_map.get("micro"))

    @staticmethod
    def get_background_color(
        niche: Optional[str] = None,
        follower_count: Optional[int] = None,
    ) -> str:
        """Get background color/style matching user niche and tier."""
        niche = (niche or "default").lower().strip()
        tier = get_follower_tier(follower_count).value

        niche_map = BACKGROUND_DEFAULTS_BY_NICHE.get(niche)
        if not niche_map:
            niche_map = BACKGROUND_DEFAULTS_BY_NICHE["default"]

        return niche_map.get(tier, niche_map.get("micro"))

    @staticmethod
    def get_color_palette(region: Optional[str] = None) -> str:
        """Get color palette matching user region."""
        region = (region or "default").lower().strip()
        return COLOR_PALETTE_DEFAULTS_BY_REGION.get(
            region, COLOR_PALETTE_DEFAULTS_BY_REGION["default"]
        )

    @staticmethod
    def build_context_aware_defaults(
        niche: Optional[str] = None,
        follower_count: Optional[int] = None,
        region: Optional[str] = None,
    ) -> Dict[str, str]:
        """Build a complete set of context-aware defaults."""
        return {
            "emotion_adjectives": ContextAwareComponentDefaults.get_emotion_adjectives(
                niche, follower_count
            ),
            "lighting_style": ContextAwareComponentDefaults.get_lighting_style(
                niche, follower_count
            ),
            "camera_angle": ContextAwareComponentDefaults.get_camera_angle(
                niche, follower_count
            ),
            "background_color": ContextAwareComponentDefaults.get_background_color(
                niche, follower_count
            ),
            "color_palette": ContextAwareComponentDefaults.get_color_palette(region),
        }
