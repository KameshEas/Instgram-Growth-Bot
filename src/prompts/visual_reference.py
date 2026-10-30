"""Bridge between the visual_systems knowledge library and the LLM prompt generator.

Two deterministic uses, no extra LLM calls:

1. build_reference_block(): a short per-category "technical reference" (lighting, lens, film grade,
   composition, scene physics) that is appended to the <constraints> the generator (P01) receives.
   The model treats it as optional starting points, so the creator's idea always wins.
2. merge_negatives(): after generation, each variation's negative_prompt is merged with the
   library's category negatives (model's own terms first, de-duplicated, capped).

Text categories (reel_scripts, captions_templates, email_subjects) get neither.
"""

import logging
from typing import Dict, List, Optional

from src.prompts.visual_systems import (
    CameraLanguage,
    ColorGrading,
    CompositionIntelligence,
    LightingPhysics,
    NegativePrompts,
    ScenePhysics,
)

logger = logging.getLogger(__name__)

TEXT_CATEGORIES = {"reel_scripts", "captions_templates", "email_subjects"}
TRANSFORM_CATEGORIES = {"women_transform", "men_transform", "couples_transform"}

# Locations (from CustomScenarioParser) that are lit by daylight vs. a controlled setup
OUTDOOR_LOCATIONS = {"beach", "mountain", "garden", "urban", "wedding"}
INDOOR_SETUP_BY_LOCATION = {
    "studio": "butterfly",
    "office": "three_point_portrait",
    "home": "two_point_editorial",
    "cafe": "two_point_editorial",
    "creative": "rembrandt",
    "generic": "three_point_portrait",
}

# Per-category profile. Every key is optional; a missing key means "no line for this aspect".
#   lighting:    (setup_type, time_of_day, location) for LightingPhysics.get_physical_lighting_description
#   camera:      (focal_length_mm, aperture) for CameraLanguage.generate_camera_string
#   grading:     (film_emulation, grading_style, saturation) for ColorGrading.get_grading_string
#   composition: (strategy, emotional_tone, depth_method) for CompositionIntelligence.generate_composition_description
#   physics:     scenario_type for ScenePhysics.generate_scene_physics_description
CATEGORY_PROFILES: Dict[str, Dict] = {
    "general_photography": {
        "camera": (35, 2.8),
        "grading": ("kodak_portra_400", None, "neutral"),
        "composition": ("rule_of_thirds", None, "foreground_middle_background"),
    },
    "women_professional": {
        "lighting": ("three_point_portrait", None, "studio"),
        "camera": (85, 2.8),
        "grading": (None, None, "neutral"),
        "composition": ("rule_of_thirds", "intimate", None),
    },
    "men_professional": {
        "lighting": ("three_point_portrait", None, "studio"),
        "camera": (85, 2.8),
        "grading": (None, None, "neutral"),
        "composition": ("rule_of_thirds", "intimate", None),
    },
    "couples_general": {
        "lighting": ("two_point_editorial", "golden_hour_evening", "outdoor"),
        "camera": (50, 2.8),
        "grading": ("kodak_portra_400", None, "neutral"),
        "composition": ("rule_of_thirds", "intimate", "foreground_middle_background"),
    },
    "women_transform": {"camera": (85, 2.0), "grading": ("kodak_portra_400", None, "neutral")},
    "men_transform": {"camera": (85, 2.0), "grading": ("kodak_portra_400", None, "neutral")},
    "couples_transform": {"camera": (50, 2.8), "grading": ("kodak_portra_400", None, "neutral")},
    "photography_styles": {
        "camera": (50, 2.0),
        "grading": ("kodak_2383", "lifted_black", "desaturated"),
        "composition": ("negative_space_dominance", "isolated", None),
    },
    "product_3d": {
        "physics": "product",
        "camera": (85, 5.6),
        "grading": (None, "desaturated_luxury", "neutral"),
        "composition": ("centered_symmetry", None, None),
    },
    "design_posters": {"composition": ("centered_symmetry", None, None)},
    "print_design": {"composition": ("rule_of_thirds", None, None)},
    "design_gifts": {"composition": ("centered_symmetry", None, None)},
    "brand_identity": {"composition": ("negative_space_dominance", None, None)},
    "logo_create": {"composition": ("negative_space_dominance", None, None)},
    "illustration_art": {"composition": ("leading_lines", None, "foreground_middle_background")},
    "animation_motion": {"composition": ("leading_lines", "dynamic", None)},
    "ui_ux_design": {},
}

# Negative-prompt sets per category, built from the library's lists. The library's own
# get_category_negatives() uses generic keys and falls back to human-anatomy terms, which is wrong
# for products and designs, so the mapping lives here.
_N = NegativePrompts
NEGATIVES_BY_CATEGORY: Dict[str, List[str]] = {
    "general_photography": _N.UNIVERSAL_NEGATIVES,
    "photography_styles": _N.UNIVERSAL_NEGATIVES,
    # Category-specific terms come first so the MAX_NEGATIVE_TERMS cap never drops them
    "women_professional": _N.PORTRAIT_NEGATIVES.get("skin", []) + _N.UNIVERSAL_NEGATIVES,
    "men_professional": _N.PORTRAIT_NEGATIVES.get("skin", []) + _N.UNIVERSAL_NEGATIVES,
    "couples_general": ["faces different people", "wrong number of people"] + _N.UNIVERSAL_NEGATIVES,
    "women_transform": _N.TRANSFORMATION_NEGATIVES.get("identity", []) + _N.UNIVERSAL_NEGATIVES,
    "men_transform": _N.TRANSFORMATION_NEGATIVES.get("identity", []) + _N.UNIVERSAL_NEGATIVES,
    "couples_transform": _N.TRANSFORMATION_NEGATIVES.get("identity", []) + ["wrong number of people"]
    + _N.UNIVERSAL_NEGATIVES,
    "product_3d": _N.PRODUCT_NEGATIVES + _N.QUALITY_FAILURE_NEGATIVES,
    "design_posters": _N.QUALITY_FAILURE_NEGATIVES,
    "print_design": _N.QUALITY_FAILURE_NEGATIVES,
    "design_gifts": _N.QUALITY_FAILURE_NEGATIVES,
    "brand_identity": _N.QUALITY_FAILURE_NEGATIVES,
    "logo_create": _N.QUALITY_FAILURE_NEGATIVES,
    "illustration_art": _N.QUALITY_FAILURE_NEGATIVES,
    "animation_motion": _N.QUALITY_FAILURE_NEGATIVES,
    "ui_ux_design": _N.QUALITY_FAILURE_NEGATIVES,
}

MAX_REFERENCE_LINE = 260   # keep each reference line short for the 8B model
MAX_NEGATIVE_TERMS = 24


def _short(text: str, label: str = "", limit: int = MAX_REFERENCE_LINE) -> str:
    """Normalise a library string: drop a repeated label prefix, cap length at a sentence boundary."""
    text = " ".join((text or "").split()).strip(" .")
    for prefix in (f"{label}:", "Composition:", "Color grade:"):
        if prefix != ":" and text.lower().startswith(prefix.lower()):
            text = text[len(prefix):].strip()
    if len(text) <= limit:
        return text
    head = text[:limit]
    cut = head.rfind(". ")
    if cut >= limit // 2:
        return head[:cut]
    return head.rsplit(" ", 1)[0].rstrip(",;:")


class VisualReference:
    """Deterministic technical reference and negative-prompt guardrails from visual_systems."""

    @staticmethod
    def build_reference_block(category: str, location: Optional[str] = None) -> str:
        """Return a short technical-reference section for <constraints>, or "" if none applies.

        location: scene detected by CustomScenarioParser (transform categories), e.g. "beach".
        """
        if category in TEXT_CATEGORIES:
            return ""
        profile = dict(CATEGORY_PROFILES.get(category, {}))

        # Transform categories: lighting and scene physics follow the detected location
        if category in TRANSFORM_CATEGORIES:
            loc = (location or "generic").lower()
            if loc in OUTDOOR_LOCATIONS:
                profile["lighting"] = ("two_point_editorial", "golden_hour_evening", "outdoor")
                profile["physics"] = "golden_hour"
                profile["composition"] = ("rule_of_thirds", "intimate", "foreground_middle_background")
            else:
                profile["lighting"] = (INDOOR_SETUP_BY_LOCATION.get(loc, "three_point_portrait"), None, "studio")
                profile["composition"] = ("rule_of_thirds", "intimate", None)

        lines = []
        try:
            if "lighting" in profile:
                setup, time_of_day, where = profile["lighting"]
                lines.append(("Lighting", LightingPhysics.get_physical_lighting_description(setup, time_of_day, where)))
            if "physics" in profile:
                lines.append(("Scene physics", ScenePhysics.generate_scene_physics_description(profile["physics"])))
            if "camera" in profile:
                focal, aperture = profile["camera"]
                lines.append(("Camera", CameraLanguage.generate_camera_string(focal_length=focal, aperture=aperture)))
            if "grading" in profile:
                film, style, saturation = profile["grading"]
                lines.append(("Color grade", ColorGrading.get_grading_string(film, style, saturation)))
            if "composition" in profile:
                strategy, tone, depth = profile["composition"]
                lines.append(("Composition", CompositionIntelligence.generate_composition_description(strategy, tone, depth)))
        except Exception as e:  # the library is optional; never break generation over it
            logger.warning(f"[VISUAL REFERENCE] failed for {category}: {e}")
            return ""

        lines = [(label, _short(text, label)) for label, text in lines if text and text.strip()]
        if not lines:
            return ""
        body = "\n".join(f"- {label}: {text}" for label, text in lines)
        return (
            "Technical reference from the app's visual library (optional starting points; when the "
            "creator's idea or the guidance above says otherwise, follow those instead):\n" + body + "\n"
        )

    @staticmethod
    def merge_negatives(variations: List[Dict], category: str) -> List[Dict]:
        """Add the category's library negatives to each variation's negative_prompt (in place)."""
        library = NEGATIVES_BY_CATEGORY.get(category)
        if not library or category in TEXT_CATEGORIES:
            return variations
        library_terms = [t.strip() for item in library for t in item.split(",") if t.strip()]
        for var in variations:
            if not isinstance(var, dict):
                continue
            own = var.get("negative_prompt") or ""
            if isinstance(own, list):
                own = ", ".join(map(str, own))
            terms, seen = [], set()
            for term in [t.strip() for t in str(own).split(",")] + library_terms:
                key = term.lower()
                if term and key not in seen:
                    seen.add(key)
                    terms.append(term)
            var["negative_prompt"] = ", ".join(terms[:MAX_NEGATIVE_TERMS])
        return variations
