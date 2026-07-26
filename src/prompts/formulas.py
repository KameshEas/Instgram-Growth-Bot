"""Prompt formula registry and composer helpers.

This module provides a compact registry of prompt "formulas" (ordered component
lists with small templates) and a simple composer to turn a formula + inputs
into a single assembled prompt string.

Enhanced with context-aware defaults that vary by user niche and follower tier,
replacing generic hardcoded fallbacks.
"""
from typing import Dict, Any, Optional
from src.prompts.context_aware_components import ContextAwareComponentDefaults


TRANSFORMATION_FORMULA_COMPONENTS = [
    {
        "key": "image_type_style_foundation",
        "template": "Image type/style foundation: {QUALITY_LEVEL}, {PHOTOGRAPHY_STYLE}, {CAMERA_ANGLE}, subject: {SCENARIO_SUBJECT}.",
    },
    {
        "key": "reference_identity_preservation",
        "template": "Reference and identity preservation: using reference image(s), preserve {FACIAL_STRUCTURE}, {EYES}, {NOSE}, {SMILE}, {SKIN_TONE}, {FACIAL_PROPORTIONS}, and overall identity without altering recognizable features.",
    },
    {
        "key": "expression_emotional_mood",
        "template": "Expression and emotional mood: {EMOTION_ADJECTIVES}; smile behavior: {SMILE_BEHAVIOR}; authenticity cues: {AUTHENTICITY_CUES}.",
    },
    {
        "key": "pose_body_language",
        "template": "Pose and body language: {BODY_ORIENTATION}, head angle: {HEAD_ANGLE}, shoulder posture: {SHOULDER_POSTURE}, neck posture: {NECK_POSTURE}, gaze direction: {GAZE_DIRECTION}, realism: {BODY_LANGUAGE_REALISM}.",
    },
    {
        "key": "hair_details",
        "template": "Hair details: texture {HAIR_TEXTURE}, color {HAIR_COLOR}, hairstyle {HAIRSTYLE}, decorative elements: {HAIR_DECORATIVE_ELEMENTS}, preserving natural texture.",
    },
    {
        "key": "clothing_fabric_detailing",
        "template": "Clothing and fabric detailing: {OUTFIT_TYPE}, material {FABRIC_MATERIAL}, palette {COLOR_PALETTE}, patterns {PATTERNS}, fabric realism: {FABRIC_REALISM}, natural folds.",
    },
    {
        "key": "accessories_jewelry",
        "template": "Accessories and jewelry: {JEWELRY_MATERIAL}, {JEWELRY_TYPE}, cultural detailing: {CULTURAL_DETAILING}, ornament realism: {ORNAMENT_REALISM}.",
    },
    {
        "key": "lighting_design",
        "template": "Lighting design: {LIGHTING_STYLE}, direction: {LIGHT_DIRECTION}, temperature: {LIGHT_TEMPERATURE}, highlight behavior: {HIGHLIGHT_BEHAVIOR}, shadow softness: {SHADOW_SOFTNESS}, skin interaction: {SKIN_INTERACTION}.",
    },
    {
        "key": "background_environment",
        "template": "Background and environment: {BACKGROUND_COLOR}, {ENVIRONMENT_TYPE}, decorative design: {DECORATIVE_DESIGN}, composition style: {COMPOSITION_STYLE}.",
    },
    {
        "key": "camera_cinematic_depth",
        "template": "Camera and cinematic depth: {LENS_STYLE}, depth of field: {DEPTH_OF_FIELD}, focus quality: {FOCUS_QUALITY}, portrait realism: {PORTRAIT_REALISM}, editorial framing: {EDITORIAL_FRAMING}.",
    },
    {
        "key": "rendering_quality_enhancers",
        "template": "Rendering and quality enhancers: 4K, RAW realism, skin microtexture, hair detailing, professional color grading, cinematic realism.",
    },
    {
        "key": "negative_constraints",
        "template": "Do not beautify excessively, do not change facial proportions, do not modify identity, do not oversoften skin, do not stylize unnaturally, and do not alter skin tone.",
    },
]


LOGO_PROMPT_FORMULA_COMPONENTS = [
    {
        "key": "brand_foundation",
        "template": "Brand foundation: brand name {BRAND_NAME}, tagline: {TAGLINE}, industry: {INDUSTRY}, brand tone: {BRAND_TONE}, target audience: {TARGET_AUDIENCE}.",
    },
    {
        "key": "purpose_deliverables",
        "template": "Purpose & deliverables: primary usage {PRIMARY_USAGE}; deliverables: include High-Resolution PNG (transparent background), design system package with color tokens, typography, spacing, usage guidelines; variant_count: {VARIANT_COUNT}.",
    },
    {
        "key": "logo_type_concept",
        "template": "Logo type & concept: {LOGO_TYPE} (wordmark/lettermark/emblem/combination); concept notes: {CONCEPT_NOTES}.",
    },
    {
        "key": "visual_identity_constraints",
        "template": "Visual identity constraints: preferred colors {PREFERRED_COLORS}; forbidden colors {FORBIDDEN_COLORS}; color harmony guidance: {COLOR_HARMONY}.",
    },
    {
        "key": "typography_lettering",
        "template": "Typography & lettering: font style {FONT_STYLE}; typography constraints: {TYPOGRAPHY_CONSTRAINTS}.",
    },
    {
        "key": "icon_mark_details",
        "template": "Icon/mark details: shape language {SHAPE_LANGUAGE}; negative space guidance: {NEGATIVE_SPACE}; symbol specifics: {SYMBOL_SPECIFICS}.",
    },
    {
        "key": "layout_variants",
        "template": "Layout & variants: layout options {LAYOUT_OPTIONS}; clear space rules: {CLEAR_SPACE}; minimum size px: {MIN_SIZE_PX}.",
    },
    {
        "key": "color_variants",
        "template": "Color variants required: full-color {FULL_COLOR}, monochrome {MONOCHROME}, single-color {SINGLE_COLOR}, reversed {REVERSED}.",
    },
    {
        "key": "export_specs",
        "template": "Export & production specs: PNG resolution {PNG_RESOLUTION}, DPI {DPI}, background {BACKGROUND}, additional PNG sizes {ADDITIONAL_PNG_SIZES}.",
    },
    {
        "key": "accessibility_contrast",
        "template": "Accessibility & contrast: contrast target {CONTRAST_TARGET}; color-blind-friendly variants: {COLOR_BLIND_FRIENDLY}.",
    },
    {
        "key": "mockups_contexts",
        "template": "Background & mockups: mockup contexts {MOCKUP_CONTEXTS}; cropping/canvas guidance: {CROPPING_GUIDANCE}.",
    },
    {
        "key": "negative_constraints",
        "template": "Constraints & IP safety: do not imitate trademarked logos or copyrighted artwork; avoid photographic textures; require original, vector-friendly shapes; no text/trademark copying.",
    },
]

PROMPT_FORMULAS: Dict[str, Dict[str, Any]] = {
    "women_transform": {
        "components": TRANSFORMATION_FORMULA_COMPONENTS,
    },
    "men_transform": {
        "components": TRANSFORMATION_FORMULA_COMPONENTS,
    },
    "couples_transform": {
        "components": TRANSFORMATION_FORMULA_COMPONENTS,
    },
    "general_photography": {
        "components": [
            {"key": "intent", "template": "Create a scene: {SCENARIO}."},
            {"key": "composition", "template": "Composition: {COMPOSITION}."},
            {"key": "lighting", "template": "Lighting: {LIGHTING}."},
            {"key": "mood", "template": "Mood: {MOOD}."},
            {"key": "quality", "template": "Quality: {QUALITY}."},
        ]
    },
    "design_gifts": {
        "components": [
            {"key": "product_anchor", "template": "Product: {PRODUCT_TYPE} (print area: {PRINTABLE_AREA})."},
            {"key": "brief_intent", "template": "Design concept: {CONCEPT}. Tone: {TONE}."},
            {"key": "visual", "template": "Visuals: color palette {COLOR_PALETTE}; typography suggestions: {TYPOGRAPHY}."},
            {"key": "constraints", "template": "Constraints: {PRODUCT_CONSTRAINTS}."},
            {"key": "quality", "template": "Quality: deliverable-ready, product-aware, high-detail."},
        ]
    },
    "portrait_transformation": {
        "components": TRANSFORMATION_FORMULA_COMPONENTS,
    },
    "design_posters": {
        "components": [
            {"key": "intent", "template": "Create a premium poster: {SCENARIO}."},
            {"key": "composition", "template": "Composition: {COMPOSITION}."},
            {"key": "visual", "template": "Color palette: {COLOR_PALETTE}. Typography: {TYPOGRAPHY}."},
            {"key": "constraints", "template": "Constraints: {PRODUCT_CONSTRAINTS}."},
            {"key": "quality", "template": "Quality: high-resolution poster-ready, editorial design."},
        ]
    },
    "print_design": {
        "components": [
            {"key": "intent", "template": "Design print collateral for: {SCENARIO}."},
            {"key": "composition", "template": "Composition: {COMPOSITION} with print-safe margins."},
            {"key": "visual", "template": "Color palette: {COLOR_PALETTE}. Typography: {TYPOGRAPHY}."},
            {"key": "constraints", "template": "Print constraints: {PRODUCT_CONSTRAINTS}."},
            {"key": "quality", "template": "Quality: print-ready, CMYK-aware, high DPI."},
        ]
    },
    "ui_ux_design": {
        "components": [
            {"key": "intent", "template": "Design a UI/UX interface for: {SCENARIO}."},
            {"key": "focus", "template": "Focus: {FOCUS} with accessibility considerations: {ACCESSIBILITY}."},
            {"key": "visual", "template": "Color palette: {COLOR_PALETTE}. Typography: {TYPOGRAPHY}."},
            {"key": "quality", "template": "Quality: production-ready UX, responsive guidelines included."},
        ]
    },
    "illustration_art": {
        "components": [
            {"key": "intent", "template": "Create an illustration: {SCENARIO}."},
            {"key": "style", "template": "Style: {STYLE} with mood: {MOOD}."},
            {"key": "color", "template": "Color palette: {COLOR_PALETTE}."},
            {"key": "quality", "template": "Quality: high-detail digital illustration, concept art quality."},
        ]
    },
    "product_3d": {
        "components": [
            {"key": "intent", "template": "Render a 3D product: {SCENARIO}."},
            {"key": "composition", "template": "Composition: {COMPOSITION}, optimal product angle."},
            {"key": "lighting", "template": "Lighting: {LIGHTING} for realistic materials."},
            {"key": "quality", "template": "Quality: ray-traced photorealistic render, high-res."},
        ]
    },
}

# Register logo_create formula (High-Resolution PNG + design system)
PROMPT_FORMULAS['logo_create'] = {"components": LOGO_PROMPT_FORMULA_COMPONENTS}


def get_formula(category: str) -> Optional[Dict[str, Any]]:
    """Return the formula dict for a normalized category name, or None."""
    if not category:
        return None
    key = category.lower().strip().replace(" ", "_").replace("-", "_")
    return PROMPT_FORMULAS.get(key)


def compose_prompt_from_formula(
    formula_def: Dict[str, Any],
    components: Dict[str, Any],
    user_context: str = "",
    niche: Optional[str] = None,
    follower_count: Optional[int] = None,
    region: Optional[str] = None,
) -> str:
    """Compose a prompt string from a formula definition with context-aware defaults.

    Args:
        formula_def: Formula dict with 'components' list containing templates
        components: Values to fill placeholders like {SCENARIO}, {LIGHTING}, etc.
        user_context: Fallback for {SCENARIO}
        niche: User's content niche (e.g., 'fitness', 'fashion') for aware defaults
        follower_count: User's follower count for tier-aware defaults
        region: User's region for color palette selection

    Returns:
        Composed prompt string with filled placeholders and context-aware defaults
    """
    if not formula_def or "components" not in formula_def:
        return ""

    # Build context-aware defaults that vary by niche, tier, and region
    context_defaults = ContextAwareComponentDefaults.build_context_aware_defaults(
        niche=niche,
        follower_count=follower_count,
        region=region,
    )

    parts = []
    for comp in formula_def["components"]:
        text = comp.get("template", "")
        if not text:
            continue

        # Use context-aware defaults instead of hardcoded generic values
        replacements = {
            "SCENARIO": components.get("scenario") or user_context or "",
            "SCENARIO_SUBJECT": components.get("scenario_subject") or components.get("subject") or components.get("scenario") or user_context or "portrait subject",
            "QUALITY_LEVEL": components.get("quality_level", "high quality"),
            "PHOTOGRAPHY_STYLE": components.get("photography_style") or components.get("style") or "photorealistic editorial photography",
            "CAMERA_ANGLE": components.get("camera_angle", context_defaults["camera_angle"]),
            "FACIAL_STRUCTURE": components.get("facial_structure", "facial structure"),
            "EYES": components.get("eyes", "eyes"),
            "NOSE": components.get("nose", "nose"),
            "SMILE": components.get("smile", "smile"),
            "SKIN_TONE": components.get("skin_tone", "skin tone"),
            "FACIAL_PROPORTIONS": components.get("facial_proportions", "facial proportions"),
            "EMOTION_ADJECTIVES": components.get("emotion_adjectives") or components.get("mood") or context_defaults["emotion_adjectives"],
            "SMILE_BEHAVIOR": components.get("smile_behavior", "natural and subtle"),
            "AUTHENTICITY_CUES": components.get("authenticity_cues", "micro-expressions and relaxed facial muscles"),
            "BODY_ORIENTATION": components.get("body_orientation", "natural three-quarter orientation"),
            "HEAD_ANGLE": components.get("head_angle", "slight natural tilt"),
            "SHOULDER_POSTURE": components.get("shoulder_posture", "relaxed and balanced"),
            "NECK_POSTURE": components.get("neck_posture", "elongated, neutral"),
            "GAZE_DIRECTION": components.get("gaze_direction", "toward camera"),
            "BODY_LANGUAGE_REALISM": components.get("body_language_realism", "anatomically natural and unforced"),
            "HAIR_TEXTURE": components.get("hair_texture", "natural texture"),
            "HAIR_COLOR": components.get("hair_color", "reference-matched color"),
            "HAIRSTYLE": components.get("hairstyle", "reference-consistent hairstyle"),
            "HAIR_DECORATIVE_ELEMENTS": components.get("hair_decorative_elements", "minimal"),
            "OUTFIT_TYPE": components.get("outfit_type") or components.get("outfit") or "scenario-appropriate outfit",
            "FABRIC_MATERIAL": components.get("fabric_material", "realistic fabric"),
            "PATTERNS": components.get("patterns", "subtle patterns"),
            "FABRIC_REALISM": components.get("fabric_realism", "high"),
            "JEWELRY_MATERIAL": components.get("jewelry_material", "metal or gemstone as appropriate"),
            "JEWELRY_TYPE": components.get("jewelry_type") or components.get("accessories") or "minimal accessories",
            "CULTURAL_DETAILING": components.get("cultural_detailing", "authentic and context-aware"),
            "ORNAMENT_REALISM": components.get("ornament_realism", "high"),
            "LIGHTING_STYLE": components.get("lighting_style") or components.get("lighting") or context_defaults["lighting_style"],
            "LIGHT_DIRECTION": components.get("light_direction", "45-degree key light"),
            "LIGHT_TEMPERATURE": components.get("light_temperature", "neutral-warm"),
            "HIGHLIGHT_BEHAVIOR": components.get("highlight_behavior", "controlled, natural highlights"),
            "SHADOW_SOFTNESS": components.get("shadow_softness", "soft"),
            "SKIN_INTERACTION": components.get("skin_interaction", "natural subsurface glow"),
            "BACKGROUND_COLOR": components.get("background_color", context_defaults["background_color"]),
            "ENVIRONMENT_TYPE": components.get("environment_type", "contextual portrait environment"),
            "DECORATIVE_DESIGN": components.get("decorative_design", "minimal and elegant"),
            "COMPOSITION_STYLE": components.get("composition_style") or components.get("composition") or "clean, balanced composition",
            "LENS_STYLE": components.get("lens_style", "85mm portrait lens feel"),
            "DEPTH_OF_FIELD": components.get("depth_of_field", "shallow"),
            "FOCUS_QUALITY": components.get("focus_quality", "sharp facial focus"),
            "PORTRAIT_REALISM": components.get("portrait_realism", "high photorealism"),
            "EDITORIAL_FRAMING": components.get("editorial_framing", "professional editorial crop"),
            "BRAND_NAME": components.get("brand_name", ""),
            "TAGLINE": components.get("tagline", ""),
            "INDUSTRY": components.get("industry", ""),
            "BRAND_TONE": components.get("brand_tone", ""),
            "TARGET_AUDIENCE": components.get("target_audience", ""),
            "PRIMARY_USAGE": components.get("primary_usage", ""),
            "VARIANT_COUNT": components.get("variant_count", 3),
            "LOGO_TYPE": components.get("logo_type", ""),
            "CONCEPT_NOTES": components.get("concept_notes", ""),
            "PREFERRED_COLORS": components.get("preferred_colors", ""),
            "FORBIDDEN_COLORS": components.get("forbidden_colors", ""),
            "COLOR_HARMONY": components.get("color_harmony", ""),
            "FONT_STYLE": components.get("font_style", ""),
            "TYPOGRAPHY_CONSTRAINTS": components.get("typography_constraints", ""),
            "SHAPE_LANGUAGE": components.get("shape_language", ""),
            "NEGATIVE_SPACE": components.get("negative_space", ""),
            "SYMBOL_SPECIFICS": components.get("symbol_specifics", ""),
            "LAYOUT_OPTIONS": components.get("layout_options", ""),
            "CLEAR_SPACE": components.get("clear_space", ""),
            "MIN_SIZE_PX": components.get("min_size_px", ""),
            "FULL_COLOR": components.get("full_color", "yes"),
            "MONOCHROME": components.get("monochrome", "yes"),
            "SINGLE_COLOR": components.get("single_color", "yes"),
            "REVERSED": components.get("reversed", "yes"),
            "PNG_RESOLUTION": components.get("png_resolution", "4000x4000"),
            "DPI": components.get("dpi", 300),
            "BACKGROUND": components.get("background", "transparent"),
            "ADDITIONAL_PNG_SIZES": components.get("additional_png_sizes", "2000x2000,1024x1024,32x32"),
            "CONTRAST_TARGET": components.get("contrast_target", "WCAG AA"),
            "COLOR_BLIND_FRIENDLY": components.get("color_blind_friendly", "false"),
            "MOCKUP_CONTEXTS": components.get("mockup_contexts", "app icon, social avatar, signage, packaging"),
            "CROPPING_GUIDANCE": components.get("cropping_guidance", "center-crop for icon; safe margins for signage"),
            "NEGATIVE_CONSTRAINTS": components.get("negative_constraints", ""),
            "LIGHTING": components.get("lighting", ""),
            "STYLING": components.get("styling") or components.get("style") or "",
            "OUTFIT": components.get("outfit", ""),
            "ACCESSORIES": components.get("accessories", ""),
            "COMPOSITION": components.get("composition", ""),
            "MOOD": components.get("mood", ""),
            "QUALITY": components.get("quality", "photorealistic"),
            "PRODUCT_TYPE": components.get("product_type", ""),
            "PRINTABLE_AREA": components.get("printable_area", ""),
            "CONCEPT": components.get("concept", ""),
            "TONE": components.get("tone", ""),
            "COLOR_PALETTE": components.get("color_palette", context_defaults["color_palette"]),
            "TYPOGRAPHY": components.get("typography", ""),
            "PRODUCT_CONSTRAINTS": components.get("product_constraints", ""),
            "FOCUS": components.get("focus", ""),
            "ACCESSIBILITY": components.get("accessibility", ""),
            "STYLE": components.get("style", ""),
        }

        for k, v in replacements.items():
            text = text.replace("{" + k + "}", str(v))

        text = text.strip()
        if text:
            parts.append(text)

    return " ".join(parts).strip()


__all__ = ["PROMPT_FORMULAS", "get_formula", "compose_prompt_from_formula"]
