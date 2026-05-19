"""Prompt formula registry and composer helpers.

This module provides a compact registry of prompt "formulas" (ordered component
lists with small templates) and a simple composer to turn a formula + inputs
into a single assembled prompt string.
"""
from typing import Dict, Any, Optional


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


def get_formula(category: str) -> Optional[Dict[str, Any]]:
    """Return the formula dict for a normalized category name, or None."""
    if not category:
        return None
    key = category.lower().strip().replace(" ", "_").replace("-", "_")
    return PROMPT_FORMULAS.get(key)


def compose_prompt_from_formula(formula_def: Dict[str, Any], components: Dict[str, Any], user_context: str = "") -> str:
    """Compose a prompt string from a formula definition.

    - `formula_def` is expected to have a `components` list with small template strings.
    - `components` supplies values used to fill placeholders like {SCENARIO}, {LIGHTING}, etc.
    - `user_context` is used as a fallback for {SCENARIO}.
    """
    if not formula_def or "components" not in formula_def:
        return ""

    parts = []
    for comp in formula_def["components"]:
        text = comp.get("template", "")
        if not text:
            continue

        replacements = {
            "SCENARIO": components.get("scenario") or user_context or "",
            "SCENARIO_SUBJECT": components.get("scenario_subject") or components.get("subject") or components.get("scenario") or user_context or "portrait subject",
            "QUALITY_LEVEL": components.get("quality_level", "high quality"),
            "PHOTOGRAPHY_STYLE": components.get("photography_style") or components.get("style") or "photorealistic editorial photography",
            "CAMERA_ANGLE": components.get("camera_angle", "eye-level portrait angle"),
            "FACIAL_STRUCTURE": components.get("facial_structure", "facial structure"),
            "EYES": components.get("eyes", "eyes"),
            "NOSE": components.get("nose", "nose"),
            "SMILE": components.get("smile", "smile"),
            "SKIN_TONE": components.get("skin_tone", "skin tone"),
            "FACIAL_PROPORTIONS": components.get("facial_proportions", "facial proportions"),
            "EMOTION_ADJECTIVES": components.get("emotion_adjectives") or components.get("mood") or "calm, confident",
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
            "LIGHTING_STYLE": components.get("lighting_style") or components.get("lighting") or "cinematic portrait lighting",
            "LIGHT_DIRECTION": components.get("light_direction", "45-degree key light"),
            "LIGHT_TEMPERATURE": components.get("light_temperature", "neutral-warm"),
            "HIGHLIGHT_BEHAVIOR": components.get("highlight_behavior", "controlled, natural highlights"),
            "SHADOW_SOFTNESS": components.get("shadow_softness", "soft"),
            "SKIN_INTERACTION": components.get("skin_interaction", "natural subsurface glow"),
            "BACKGROUND_COLOR": components.get("background_color", "complementary neutral tones"),
            "ENVIRONMENT_TYPE": components.get("environment_type", "contextual portrait environment"),
            "DECORATIVE_DESIGN": components.get("decorative_design", "minimal and elegant"),
            "COMPOSITION_STYLE": components.get("composition_style") or components.get("composition") or "clean, balanced composition",
            "LENS_STYLE": components.get("lens_style", "85mm portrait lens feel"),
            "DEPTH_OF_FIELD": components.get("depth_of_field", "shallow"),
            "FOCUS_QUALITY": components.get("focus_quality", "sharp facial focus"),
            "PORTRAIT_REALISM": components.get("portrait_realism", "high photorealism"),
            "EDITORIAL_FRAMING": components.get("editorial_framing", "professional editorial crop"),
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
            "COLOR_PALETTE": components.get("color_palette", ""),
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
