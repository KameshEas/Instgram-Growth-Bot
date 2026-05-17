"""Prompt formula registry and composer helpers.

This module provides a compact registry of prompt "formulas" (ordered component
lists with small templates) and a simple composer to turn a formula + inputs
into a single assembled prompt string.
"""
from typing import Dict, Any, Optional


PROMPT_FORMULAS: Dict[str, Dict[str, Any]] = {
    "women_transform": {
        "components": [
            {"key": "reference_anchor", "template": "Using reference image, transform the subject into {SCENARIO}."},
            {"key": "identity_closure", "template": "Keep natural skin texture and appearance matching the reference."},
            {"key": "composition_framing", "template": "Composition: medium close-up (waist-up), face focal and sharp; hands visible if relevant."},
            {"key": "styling_clothing", "template": "Styling: {STYLING}. Outfit: {OUTFIT}."},
            {"key": "lighting_mood", "template": "Lighting: {LIGHTING}."},
            {"key": "details", "template": "Details: {ACCESSORIES}. Intricate hand details if present."},
            {"key": "negative_constraints", "template": "Constraints: No face distortion; no extra fingers; no stylized/cartoon rendering; avoid facial beautification."},
            {"key": "quality", "template": "Quality: photorealistic, high detail, natural tones, 85mm portrait feel."},
        ]
    },
    "men_transform": {
        "components": [
            {"key": "reference_anchor", "template": "Using reference image, transform the subject into {SCENARIO}."},
            {"key": "identity_closure", "template": "Keep natural skin texture and appearance matching the reference; preserve facial hair style if present."},
            {"key": "composition_framing", "template": "Composition: medium close-up (waist-up), face focal and sharp; hands visible if relevant."},
            {"key": "styling_clothing", "template": "Styling: {STYLING}. Outfit: {OUTFIT}."},
            {"key": "lighting_mood", "template": "Lighting: {LIGHTING}."},
            {"key": "details", "template": "Details: {ACCESSORIES}. Keep facial hair and texture authentic."},
            {"key": "negative_constraints", "template": "Constraints: No face distortion; no extra fingers; no stylized/cartoon rendering; avoid facial beautification."},
            {"key": "quality", "template": "Quality: photorealistic, high detail, natural tones, 85mm portrait feel."},
        ]
    },
    "couples_transform": {
        "components": [
            {"key": "reference_anchor", "template": "Using reference images, transform the couple into {SCENARIO}."},
            {"key": "identity_closure", "template": "Preserve both subjects' natural skin texture and appearance matching their references."},
            {"key": "composition_framing", "template": "Composition: two-subject framing, faces sharp and connected; maintain emotional connection."},
            {"key": "styling_clothing", "template": "Styling: {STYLING}. Outfits: {OUTFIT}."},
            {"key": "lighting_mood", "template": "Lighting: {LIGHTING}."},
            {"key": "details", "template": "Details: {ACCESSORIES}. Emphasize realistic interaction and hands if visible."},
            {"key": "negative_constraints", "template": "Constraints: No face distortion; no extra fingers; no stylized/cartoon rendering; avoid facial beautification."},
            {"key": "quality", "template": "Quality: photorealistic, high detail, natural tones, couple editorial feel."},
        ]
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
        "components": [
            {"key": "reference_anchor", "template": "Using reference image, apply a portrait transformation: {SCENARIO}."},
            {"key": "identity_closure", "template": "Preserve facial identity and natural skin texture matching the reference."},
            {"key": "composition", "template": "Composition: {COMPOSITION} (face focal and sharp)."},
            {"key": "lighting", "template": "Lighting: {LIGHTING}."},
            {"key": "styling", "template": "Styling: {STYLING}. Outfit: {OUTFIT}."},
            {"key": "negative_constraints", "template": "Constraints: No face distortion, no identity change, no extra fingers, no cartoonish rendering."},
            {"key": "quality", "template": "Quality: photorealistic, high detail, editorial portrait feel."},
        ]
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
