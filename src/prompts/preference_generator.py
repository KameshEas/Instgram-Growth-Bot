"""Preference generator - extract, validate, and generate aesthetic preferences.

Converts user input into aesthetic preference objects that guide prompt generation.
"""

import logging
from typing import Dict, Any, Optional, List
from src.prompts.aesthetic_preferences import (
    AestheticPreferences,
    BlendLevel,
    JewelryStyle,
    MakeupVibe,
    ColorPalette,
)

logger = logging.getLogger(__name__)


class PreferenceGenerator:
    """Generate aesthetic preferences from user input."""

    # Mappings for user-friendly input
    BLEND_MAPPINGS = {
        "traditional": BlendLevel.FULLY_TRADITIONAL,
        "mostly traditional": BlendLevel.MOSTLY_TRADITIONAL,
        "80% traditional": BlendLevel.MOSTLY_TRADITIONAL,
        "blend": BlendLevel.BLEND_TRADITIONAL,
        "60% traditional": BlendLevel.BLEND_TRADITIONAL,
        "50/50": BlendLevel.HALF_BLEND,
        "half": BlendLevel.HALF_BLEND,
        "modern": BlendLevel.FULLY_MODERN,
        "100% modern": BlendLevel.FULLY_MODERN,
        "60% modern": BlendLevel.MOSTLY_MODERN,
        "mostly modern": BlendLevel.MOSTLY_MODERN,
        "fusion": BlendLevel.FUSION_FOCUS,
        "fusion focus": BlendLevel.FUSION_FOCUS,
    }

    JEWELRY_MAPPINGS = {
        "minimal": JewelryStyle.MINIMAL,
        "none": JewelryStyle.MINIMAL,
        "simple": JewelryStyle.MINIMAL,
        "moderate": JewelryStyle.MODERATE,
        "balanced": JewelryStyle.MODERATE,
        "statement": JewelryStyle.STATEMENT,
        "bold": JewelryStyle.STATEMENT,
        "layered": JewelryStyle.LAYERED,
        "multiple": JewelryStyle.LAYERED,
        "traditional": JewelryStyle.TRADITIONAL,
        "cultural": JewelryStyle.TRADITIONAL,
        "modern": JewelryStyle.MODERN,
        "minimalist": JewelryStyle.MODERN,
        "fusion": JewelryStyle.FUSION,
        "mixed": JewelryStyle.FUSION,
    }

    MAKEUP_MAPPINGS = {
        "natural": MakeupVibe.NATURAL,
        "fresh": MakeupVibe.NATURAL,
        "minimal": MakeupVibe.NATURAL,
        "bold": MakeupVibe.BOLD,
        "dramatic": MakeupVibe.BOLD,
        "artistic": MakeupVibe.BOLD,
        "minimalist": MakeupVibe.MINIMALIST,
        "subtle": MakeupVibe.MINIMALIST,
        "clean": MakeupVibe.MINIMALIST,
        "traditional": MakeupVibe.TRADITIONAL,
        "cultural": MakeupVibe.TRADITIONAL,
        "modern": MakeupVibe.MODERN,
        "contemporary": MakeupVibe.MODERN,
        "editorial": MakeupVibe.EDITORIAL,
        "fashion": MakeupVibe.EDITORIAL,
        "fusion": MakeupVibe.FUSION,
    }

    COLOR_MAPPINGS = {
        "vibrant": ColorPalette.VIBRANT_WARM,
        "warm": ColorPalette.VIBRANT_WARM,
        "energetic": ColorPalette.VIBRANT_WARM,
        "jewel": ColorPalette.JEWEL_TONES,
        "jewel tones": ColorPalette.JEWEL_TONES,
        "elegant": ColorPalette.JEWEL_TONES,
        "luxury": ColorPalette.JEWEL_TONES,
        "earth": ColorPalette.EARTH_TONES,
        "natural": ColorPalette.EARTH_TONES,
        "organic": ColorPalette.EARTH_TONES,
        "pastel": ColorPalette.COOL_PASTELS,
        "soft": ColorPalette.COOL_PASTELS,
        "dreamy": ColorPalette.COOL_PASTELS,
        "bold": ColorPalette.BOLD_MONOCHROME,
        "monochrome": ColorPalette.BOLD_MONOCHROME,
        "black and white": ColorPalette.BOLD_MONOCHROME,
        "rainbow": ColorPalette.RAINBOW_FUSION,
        "colorful": ColorPalette.RAINBOW_FUSION,
        "artistic": ColorPalette.RAINBOW_FUSION,
        "neutral": ColorPalette.NEUTRAL,
        "professional": ColorPalette.NEUTRAL,
        "minimal": ColorPalette.NEUTRAL,
    }

    @staticmethod
    def parse_blend_level(user_input: Optional[str]) -> BlendLevel:
        """Parse user input to blend level preference.

        Args:
            user_input: User's blend preference text

        Returns:
            BlendLevel enum value
        """
        if not user_input:
            return BlendLevel.HALF_BLEND  # Default

        user_input_lower = user_input.lower().strip()

        # Check direct mappings
        if user_input_lower in PreferenceGenerator.BLEND_MAPPINGS:
            return PreferenceGenerator.BLEND_MAPPINGS[user_input_lower]

        # Check partial matches: prioritize patterns with % or / (more specific) over simple words
        # Sort: (1) has % or /, (2) by length descending, (3) alphabetically
        def sort_key(key):
            has_special = -1 if '%' in key or '/' in key else 0
            return (has_special, -len(key), key)

        for key in sorted(PreferenceGenerator.BLEND_MAPPINGS.keys(), key=sort_key):
            if key in user_input_lower:
                return PreferenceGenerator.BLEND_MAPPINGS[key]

        # Default if no match
        return BlendLevel.HALF_BLEND

    @staticmethod
    def parse_jewelry_style(user_input: Optional[str]) -> JewelryStyle:
        """Parse user input to jewelry style preference."""
        if not user_input:
            return JewelryStyle.FUSION  # Default

        user_input_lower = user_input.lower().strip()

        if user_input_lower in PreferenceGenerator.JEWELRY_MAPPINGS:
            return PreferenceGenerator.JEWELRY_MAPPINGS[user_input_lower]

        for key in sorted(PreferenceGenerator.JEWELRY_MAPPINGS.keys(), key=len, reverse=True):
            if key in user_input_lower:
                return PreferenceGenerator.JEWELRY_MAPPINGS[key]

        return JewelryStyle.FUSION

    @staticmethod
    def parse_makeup_vibe(user_input: Optional[str]) -> MakeupVibe:
        """Parse user input to makeup vibe preference."""
        if not user_input:
            return MakeupVibe.MODERN  # Default

        user_input_lower = user_input.lower().strip()

        if user_input_lower in PreferenceGenerator.MAKEUP_MAPPINGS:
            return PreferenceGenerator.MAKEUP_MAPPINGS[user_input_lower]

        for key in sorted(PreferenceGenerator.MAKEUP_MAPPINGS.keys(), key=len, reverse=True):
            if key in user_input_lower:
                return PreferenceGenerator.MAKEUP_MAPPINGS[key]

        return MakeupVibe.MODERN

    @staticmethod
    def parse_color_palette(user_input: Optional[str]) -> ColorPalette:
        """Parse user input to color palette preference."""
        if not user_input:
            return ColorPalette.JEWEL_TONES  # Default

        user_input_lower = user_input.lower().strip()

        if user_input_lower in PreferenceGenerator.COLOR_MAPPINGS:
            return PreferenceGenerator.COLOR_MAPPINGS[user_input_lower]

        for key in sorted(PreferenceGenerator.COLOR_MAPPINGS.keys(), key=len, reverse=True):
            if key in user_input_lower:
                return PreferenceGenerator.COLOR_MAPPINGS[key]

        return ColorPalette.JEWEL_TONES

    @staticmethod
    def extract_from_dict(data: Dict[str, Any]) -> AestheticPreferences:
        """Extract aesthetic preferences from data dictionary.

        Args:
            data: Dictionary with preference keys

        Returns:
            AestheticPreferences object
        """
        # Get preferences from dict
        blend_input = data.get("blend_preference") or data.get("attire_blend")
        jewelry_input = data.get("jewelry_preference") or data.get("jewelry_style")
        makeup_input = data.get("makeup_preference") or data.get("makeup_vibe")
        color_input = data.get("color_preference") or data.get("color_palette")
        occasion = data.get("occasion", "casual")
        cultures = data.get("culture_influences") or data.get("cultures")

        # Parse inputs
        blend = PreferenceGenerator.parse_blend_level(blend_input)
        jewelry = PreferenceGenerator.parse_jewelry_style(jewelry_input)
        makeup = PreferenceGenerator.parse_makeup_vibe(makeup_input)
        color = PreferenceGenerator.parse_color_palette(color_input)

        # Create preferences object
        return AestheticPreferences(
            blend_level=blend,
            jewelry_style=jewelry,
            makeup_vibe=makeup,
            color_palette=color,
            occasion=occasion,
            culture_influences=cultures if isinstance(cultures, list) else None,
        )

    @staticmethod
    def extract_from_niche_and_tier(
        niche: Optional[str] = None,
        follower_count: Optional[int] = None,
    ) -> AestheticPreferences:
        """Generate aesthetic preferences based on niche and follower tier.

        Args:
            niche: User's niche (fashion, fitness, lifestyle, etc.)
            follower_count: User's follower count

        Returns:
            AestheticPreferences with niche-appropriate defaults
        """
        niche = (niche or "").lower().strip()

        # Determine tier
        if not follower_count or follower_count < 10000:
            tier = "micro"
        elif follower_count < 100000:
            tier = "mid"
        else:
            tier = "macro"

        # Niche-specific preference defaults
        niche_preferences = {
            "fashion": {
                "micro": AestheticPreferences(
                    blend_level=BlendLevel.HALF_BLEND,
                    jewelry_style=JewelryStyle.STATEMENT,
                    makeup_vibe=MakeupVibe.MODERN,
                    color_palette=ColorPalette.VIBRANT_WARM,
                    occasion="fashion",
                ),
                "mid": AestheticPreferences(
                    blend_level=BlendLevel.FUSION_FOCUS,
                    jewelry_style=JewelryStyle.FUSION,
                    makeup_vibe=MakeupVibe.EDITORIAL,
                    color_palette=ColorPalette.JEWEL_TONES,
                    occasion="fashion",
                ),
                "macro": AestheticPreferences(
                    blend_level=BlendLevel.FUSION_FOCUS,
                    jewelry_style=JewelryStyle.STATEMENT,
                    makeup_vibe=MakeupVibe.EDITORIAL,
                    color_palette=ColorPalette.BOLD_MONOCHROME,
                    occasion="fashion",
                ),
            },

            "fitness": {
                "micro": AestheticPreferences(
                    blend_level=BlendLevel.HALF_BLEND,
                    jewelry_style=JewelryStyle.MINIMAL,
                    makeup_vibe=MakeupVibe.NATURAL,
                    color_palette=ColorPalette.VIBRANT_WARM,
                    occasion="lifestyle",
                ),
                "mid": AestheticPreferences(
                    blend_level=BlendLevel.MOSTLY_MODERN,
                    jewelry_style=JewelryStyle.MINIMAL,
                    makeup_vibe=MakeupVibe.MODERN,
                    color_palette=ColorPalette.VIBRANT_WARM,
                    occasion="lifestyle",
                ),
                "macro": AestheticPreferences(
                    blend_level=BlendLevel.FULLY_MODERN,
                    jewelry_style=JewelryStyle.MINIMAL,
                    makeup_vibe=MakeupVibe.BOLD,
                    color_palette=ColorPalette.BOLD_MONOCHROME,
                    occasion="lifestyle",
                ),
            },

            "lifestyle": {
                "micro": AestheticPreferences(
                    blend_level=BlendLevel.HALF_BLEND,
                    jewelry_style=JewelryStyle.MODERATE,
                    makeup_vibe=MakeupVibe.NATURAL,
                    color_palette=ColorPalette.EARTH_TONES,
                    occasion="lifestyle",
                ),
                "mid": AestheticPreferences(
                    blend_level=BlendLevel.FUSION_FOCUS,
                    jewelry_style=JewelryStyle.FUSION,
                    makeup_vibe=MakeupVibe.MODERN,
                    color_palette=ColorPalette.JEWEL_TONES,
                    occasion="lifestyle",
                ),
                "macro": AestheticPreferences(
                    blend_level=BlendLevel.FUSION_FOCUS,
                    jewelry_style=JewelryStyle.STATEMENT,
                    makeup_vibe=MakeupVibe.EDITORIAL,
                    color_palette=ColorPalette.JEWEL_TONES,
                    occasion="lifestyle",
                ),
            },

            "professional": {
                "micro": AestheticPreferences(
                    blend_level=BlendLevel.BLEND_TRADITIONAL,
                    jewelry_style=JewelryStyle.MINIMAL,
                    makeup_vibe=MakeupVibe.MINIMALIST,
                    color_palette=ColorPalette.NEUTRAL,
                    occasion="professional",
                ),
                "mid": AestheticPreferences(
                    blend_level=BlendLevel.HALF_BLEND,
                    jewelry_style=JewelryStyle.MODERATE,
                    makeup_vibe=MakeupVibe.MODERN,
                    color_palette=ColorPalette.JEWEL_TONES,
                    occasion="professional",
                ),
                "macro": AestheticPreferences(
                    blend_level=BlendLevel.MOSTLY_MODERN,
                    jewelry_style=JewelryStyle.STATEMENT,
                    makeup_vibe=MakeupVibe.EDITORIAL,
                    color_palette=ColorPalette.BOLD_MONOCHROME,
                    occasion="professional",
                ),
            },
        }

        # Get default for this niche/tier combination
        if niche in niche_preferences:
            return niche_preferences[niche].get(tier, niche_preferences[niche]["micro"])

        # Default for unknown niche
        return AestheticPreferences()

    @staticmethod
    def log_preferences(prefs: AestheticPreferences) -> None:
        """Log preference selection for analytics."""
        logger.info(
            f"[PREFERENCES] Selected: "
            f"Blend={prefs.blend_level.value}, "
            f"Jewelry={prefs.jewelry_style.value}, "
            f"Makeup={prefs.makeup_vibe.value}, "
            f"Colors={prefs.color_palette.value}, "
            f"Occasion={prefs.occasion}"
        )
