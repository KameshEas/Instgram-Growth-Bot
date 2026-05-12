"""Composition Intelligence - Issue #8 Solution
Strategic composition design instead of independent component descriptions.

Composition includes:
- Focal hierarchy
- Eye path through image
- Balance and weight
- Foreground/midground/background relationships
- Framing mechanics
- Rule of thirds
- Leading lines
- Negative space
"""

from typing import Dict, List, Optional


class CompositionIntelligence:
    """Strategic composition design for visual hierarchy."""
    
    # Compositional rules and framing
    FRAMING_STRATEGIES = {
        "rule_of_thirds": {
            "description": "subject positioned at intersection of thirds, dynamic balance",
            "focal_point": "off-center positioning creating dynamic tension",
            "breathing_room": "space in front of subject's gaze direction",
        },
        "centered_symmetry": {
            "description": "centered subject with balanced environment",
            "focal_point": "direct center emphasis",
            "breathing_room": "equal space on all sides",
            "emotional": "formal, powerful, assertive",
        },
        "foreground_anchor": {
            "description": "foreground element framing subject",
            "technique": "blurred foreground framing subject, creating depth",
            "emotional": "intimate, layered, three-dimensional",
        },
        "leading_lines": {
            "description": "environmental lines guiding eye to subject",
            "technique": "paths, lines, architecture leading to focal point",
            "emotional": "narrative direction, viewer engagement",
        },
        "negative_space_dominance": {
            "description": "strategic empty space as compositional element",
            "technique": "minimal subject with maximum breathing room",
            "emotional": "minimalist, sophisticated, luxury restraint",
        },
    }
    
    # Focal hierarchy levels
    FOCAL_HIERARCHY = {
        "primary": {
            "emphasis": "primary focal point (usually subject)",
            "size": "dominant in frame",
            "focus": "sharpest focus area",
            "contrast": "highest contrast",
        },
        "secondary": {
            "emphasis": "supporting elements with reduced emphasis",
            "size": "smaller than primary",
            "focus": "slightly soft focus from primary",
            "contrast": "reduced contrast from primary",
        },
        "tertiary": {
            "emphasis": "background/environmental context",
            "size": "significantly smaller",
            "focus": "soft focus blur",
            "contrast": "minimal, atmospheric",
        },
    }
    
    # Depth composition techniques
    DEPTH_TECHNIQUES = {
        "foreground_middle_background": {\n            "layers": "three distinct layers creating visual depth",\n            "effect": "foreground (blurred), midground (sharp subject), background (blurred)",\n            "depth_perception": "extreme depth apparent from layering",\n        },\n        "atmospheric_perspective": {\n            "technique": "distant elements increasingly desaturated and hazy",\n            "effect": "atmospheric particle interaction reducing contrast with distance",\n            "depth_perception": "distance perception through atmospheric quality",\n        },\n        "overlapping_objects": {\n            "technique": "foreground objects partially obscuring background",\n            "effect": "depth from occlusion relationships",\n            "depth_perception": "layered spatial relationships clear",\n        },\n    }\n    \n    # Emotional composition profiles\n    EMOTIONAL_COMPOSITION = {\n        "intimate": {\n            "framing": "tight composition with minimal breathing room",\n            "distance": "close to subject, foreground elements framing",\n            "hierarchy": "subject dominant, environment secondary",\n            "emotional": "vulnerability, connection, immediacy",\n        },\n        "grand": {\n            "framing": "wide environmental context with subject small",\n            "distance": "far from subject showing scale",\n            "hierarchy": "environment dominant, subject contextual",\n            "emotional": "awe, scale, majesty",\n        },\n        "isolated": {\n            "framing": "subject surrounded by negative space",\n            "distance": "breathing room maximized",\n            "hierarchy": "subject absolutely dominant",\n            "emotional": "loneliness, focus, emphasis",\n        },\n        "dynamic": {\n            "framing": "off-center with diagonal composition",\n            "distance": "varied layering creating tension",\n            "hierarchy": "multiple competing focal points",\n            "emotional": "energy, movement, tension",\n        },\n    }\n    \n    # Composition by subject positioning\n    SUBJECT_POSITIONING = {\n        \"left_third\": \"subject positioned at left third with right negative space\",\n        \"center\": \"centered subject with balanced environment\",\n        \"right_third\": \"subject positioned at right third with left negative space\",\n        \"upper_third\": \"subject in upper portion with lower environment\",\n        \"lower_third\": \"subject in lower portion with upper environment\",\n    }\n    \n    @staticmethod\n    def generate_composition_description(\n        strategy: str,\n        emotional_tone: Optional[str] = None,\n        depth_method: Optional[str] = None,\n    ) -> str:\n        \"\"\"Generate strategic composition description.\"\"\"\n        \n        description_parts = []\n        \n        if strategy in CompositionIntelligence.FRAMING_STRATEGIES:\n            frame_info = CompositionIntelligence.FRAMING_STRATEGIES[strategy]\n            description_parts.append(\n                f\"Composition: {frame_info.get('description', '')}. \"\n                f\"Focal point: {frame_info.get('focal_point', '')}\"\n            )\n        \n        if emotional_tone and emotional_tone in CompositionIntelligence.EMOTIONAL_COMPOSITION:\n            emotion_info = CompositionIntelligence.EMOTIONAL_COMPOSITION[emotional_tone]\n            description_parts.append(\n                f\"Emotional composition: {emotion_info.get('framing', '')}. \"\n                f\"Distance and hierarchy: {emotion_info.get('hierarchy', '')}\"\n            )\n        \n        if depth_method and depth_method in CompositionIntelligence.DEPTH_TECHNIQUES:\n            depth_info = CompositionIntelligence.DEPTH_TECHNIQUES[depth_method]\n            description_parts.append(\n                f\"Depth technique: {depth_info.get('technique', '')}. \"\n                f\"Effect: {depth_info.get('effect', '')}\"\n            )\n        \n        return \". \".join(description_parts)\n    \n    @staticmethod\n    def focal_hierarchy_string(primary: str, secondary: Optional[str] = None) -> str:\n        \"\"\"Describe focal hierarchy for composition.\"\"\"\n        \n        result = f\"Primary focal point: {primary} receiving maximum emphasis, sharpest focus, highest contrast\"\n        \n        if secondary:\n            result += f\". Secondary element: {secondary} with reduced emphasis and softer focus\"\n        \n        result += \". Background atmospheric and supporting without distraction.\"\n        \n        return result\n    \n    @staticmethod\n    def negative_space_ratio(percentage: int) -> str:\n        \"\"\"Describe negative space in composition.\"\"\"\n        \n        if percentage > 60:\n            return \"dominant negative space creating minimalist luxury aesthetic\"\n        elif percentage > 40:\n            return \"substantial negative space with balanced subject emphasis\"\n        elif percentage > 20:\n            return \"moderate negative space supporting subject composition\"\n        else:\n            return \"minimal negative space with densely packed composition\"\n