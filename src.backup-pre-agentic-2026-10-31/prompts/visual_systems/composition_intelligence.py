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
        "foreground_middle_background": {
            "layers": "three distinct layers creating visual depth",
            "effect": "foreground (blurred), midground (sharp subject), background (blurred)",
            "depth_perception": "extreme depth apparent from layering",
        },
        "atmospheric_perspective": {
            "technique": "distant elements increasingly desaturated and hazy",
            "effect": "atmospheric particle interaction reducing contrast with distance",
            "depth_perception": "distance perception through atmospheric quality",
        },
        "overlapping_objects": {
            "technique": "foreground objects partially obscuring background",
            "effect": "depth from occlusion relationships",
            "depth_perception": "layered spatial relationships clear",
        },
    }
    
    # Emotional composition profiles
    EMOTIONAL_COMPOSITION = {
        "intimate": {
            "framing": "tight composition with minimal breathing room",
            "distance": "close to subject, foreground elements framing",
            "hierarchy": "subject dominant, environment secondary",
            "emotional": "vulnerability, connection, immediacy",
        },
        "grand": {
            "framing": "wide environmental context with subject small",
            "distance": "far from subject showing scale",
            "hierarchy": "environment dominant, subject contextual",
            "emotional": "awe, scale, majesty",
        },
        "isolated": {
            "framing": "subject surrounded by negative space",
            "distance": "breathing room maximized",
            "hierarchy": "subject absolutely dominant",
            "emotional": "loneliness, focus, emphasis",
        },
        "dynamic": {
            "framing": "off-center with diagonal composition",
            "distance": "varied layering creating tension",
            "hierarchy": "multiple competing focal points",
            "emotional": "energy, movement, tension",
        },
    }
    
    # Composition by subject positioning
    SUBJECT_POSITIONING = {
        "left_third": "subject positioned at left third with right negative space",
        "center": "centered subject with balanced environment",
        "right_third": "subject positioned at right third with left negative space",
        "upper_third": "subject in upper portion with lower environment",
        "lower_third": "subject in lower portion with upper environment",
    }
    
    @staticmethod
    def generate_composition_description(
        strategy: str,
        emotional_tone: Optional[str] = None,
        depth_method: Optional[str] = None,
    ) -> str:
        """Generate strategic composition description."""
        
        description_parts = []
        
        if strategy in CompositionIntelligence.FRAMING_STRATEGIES:
            frame_info = CompositionIntelligence.FRAMING_STRATEGIES[strategy]
            part = f"Composition: {frame_info.get('description', strategy.replace('_', ' '))}"
            if frame_info.get('focal_point'):  # not every strategy defines a focal point
                part += f". Focal point: {frame_info['focal_point']}"
            description_parts.append(part)
        
        if emotional_tone and emotional_tone in CompositionIntelligence.EMOTIONAL_COMPOSITION:
            emotion_info = CompositionIntelligence.EMOTIONAL_COMPOSITION[emotional_tone]
            description_parts.append(
                f"Emotional composition: {emotion_info.get('framing', '')}. "
                f"Distance and hierarchy: {emotion_info.get('hierarchy', '')}"
            )
        
        if depth_method and depth_method in CompositionIntelligence.DEPTH_TECHNIQUES:
            depth_info = CompositionIntelligence.DEPTH_TECHNIQUES[depth_method]
            # "foreground_middle_background" stores its technique under "layers"
            technique = depth_info.get('technique') or depth_info.get('layers', '')
            description_parts.append(
                f"Depth technique: {technique}. "
                f"Effect: {depth_info.get('effect', '')}"
            )
        
        return ". ".join(description_parts)
    
    @staticmethod
    def focal_hierarchy_string(primary: str, secondary: Optional[str] = None) -> str:
        """Describe focal hierarchy for composition."""
        
        result = f"Primary focal point: {primary} receiving maximum emphasis, sharpest focus, highest contrast"
        
        if secondary:
            result += f". Secondary element: {secondary} with reduced emphasis and softer focus"
        
        result += ". Background atmospheric and supporting without distraction."
        
        return result
    
    @staticmethod
    def negative_space_ratio(percentage: int) -> str:
        """Describe negative space in composition."""
        
        if percentage > 60:
            return "dominant negative space creating minimalist luxury aesthetic"
        elif percentage > 40:
            return "substantial negative space with balanced subject emphasis"
        elif percentage > 20:
            return "moderate negative space supporting subject composition"
        else:
            return "minimal negative space with densely packed composition"
