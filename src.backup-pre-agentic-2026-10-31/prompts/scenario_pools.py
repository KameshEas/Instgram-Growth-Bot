"""Scenario pools - dynamic, occasion-based scene variations.

Instead of fixed scenarios, provide pools of scenarios that vary based on:
- Occasion (professional, casual, festive, wedding, creative)
- User preferences (blend level, culture influences)
- Category (portrait, fashion, lifestyle, etc.)

This enables infinite scenario variation without being pigeon-holed.
"""

from typing import Dict, List, Optional
from enum import Enum


class Occasion(Enum):
    """Occasion types."""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    FESTIVE = "festive"
    WEDDING = "wedding"
    EVENING = "evening"
    CREATIVE = "creative"
    LIFESTYLE = "lifestyle"
    FASHION = "fashion"


# ============================================================================
# PROFESSIONAL SCENARIOS (Work, Business, Career-focused)
# ============================================================================

PROFESSIONAL_SCENARIOS = {
    "corporate_boardroom": {
        "setting": "Corporate boardroom or executive office",
        "pose": "Power pose - standing confident, commanding presence",
        "body_position": "Upright, formal, professional posture",
        "face_angle": "Direct eye contact or authoritative angle",
        "expression": "Confident, commanding, professional authority",
        "lighting": "Corporate professional lighting, bright neutral",
        "background": "Office elements, professional backdrop",
        "vibe": "Power, authority, leadership, confidence",
    },

    "creative_professional": {
        "setting": "Creative agency or design studio",
        "pose": "Relaxed confident - leaning on desk, creative stance",
        "body_position": "Comfortable confidence, creative energy",
        "face_angle": "Approachable with professional polish",
        "expression": "Creative, passionate, professional warmth",
        "lighting": "Soft contemporary studio lighting",
        "background": "Creative space, artistic elements softly blurred",
        "vibe": "Creativity, innovation, professional passion",
    },

    "startup_casual": {
        "setting": "Modern startup office or tech environment",
        "pose": "Relaxed authentic - natural stance, comfortable professional",
        "body_position": "Approachable yet confident, modern professional",
        "face_angle": "Genuine, approachable, friendly professional",
        "expression": "Warm, friendly, collaborative, genuine",
        "lighting": "Soft contemporary natural or office lighting",
        "background": "Modern minimalist office, startup aesthetic",
        "vibe": "Innovation, collaboration, modern professionalism",
    },

    "entrepreneur": {
        "setting": "Personal workspace or luxury environment",
        "pose": "Commanding but approachable - self-assured stance",
        "body_position": "Confident, purposeful, independent energy",
        "face_angle": "Direct and intentional gaze",
        "expression": "Determined, ambitious, self-assured, visionary",
        "lighting": "Professional dramatic or golden hour lighting",
        "background": "Luxury setting or inspired backdrop",
        "vibe": "Ambition, leadership, vision, success",
    },

    "expert_professional": {
        "setting": "Professional environment specific to expertise (lab, clinic, studio)",
        "pose": "Authoritative yet approachable, expert stance",
        "body_position": "Confident in expertise, professional mastery",
        "face_angle": "Trustworthy and knowledgeable angle",
        "expression": "Expert confidence, professional wisdom, knowledgeable",
        "lighting": "Professional specialized lighting",
        "background": "Professional environment reflecting expertise",
        "vibe": "Expertise, trust, professional mastery",
    },
}


# ============================================================================
# CASUAL SCENARIOS (Relaxed, Everyday, Comfortable)
# ============================================================================

CASUAL_SCENARIOS = {
    "cafe_relaxed": {
        "setting": "Coffee cafe or casual cafe ambiance",
        "pose": "Relaxed seated or leaning - comfortable and at-ease",
        "body_position": "Relaxed posture, comfortable and approachable",
        "face_angle": "Natural over-shoulder look or soft angle",
        "expression": "Warm, friendly, genuine smile, relaxed contentment",
        "lighting": "Soft cafe lighting or warm natural light",
        "background": "Cafe interior elements, intimate relaxed setting",
        "vibe": "Relaxed, approachable, genuine, comfortable",
    },

    "street_style": {
        "setting": "Urban street or market setting",
        "pose": "Natural confident walk or street pose",
        "body_position": "Comfortable urban energy, street confident",
        "face_angle": "Natural street angle, authentic",
        "expression": "Confident, authentic, fashion-aware",
        "lighting": "Natural daylight, authentic street lighting",
        "background": "Urban street, market, city elements",
        "vibe": "Fashion, urban, authentic, confident style",
    },

    "artsy_casual": {
        "setting": "Creative space, gallery, or artistic environment",
        "pose": "Free-spirited authentic pose, creative ease",
        "body_position": "Relaxed creative energy, artistic comfort",
        "face_angle": "Thoughtful, creative, expressive angle",
        "expression": "Creative, thoughtful, artistic, genuine",
        "lighting": "Soft artistic lighting, moody or inspiring",
        "background": "Artistic elements, creative space backdrop",
        "vibe": "Creativity, artistic expression, genuine authenticity",
    },

    "global_traveler": {
        "setting": "Travel destination or cultural location",
        "pose": "Relaxed exploration pose, travel comfort",
        "body_position": "Comfortable wanderer energy, approachable traveler",
        "face_angle": "Open, curious, engaged angle",
        "expression": "Curious, joyful, adventurous, open-minded",
        "lighting": "Natural destination lighting, authentic travel light",
        "background": "Travel destination, cultural landmark, authentic setting",
        "vibe": "Adventure, openness, exploration, curiosity",
    },

    "minimalist_zen": {
        "setting": "Minimalist contemporary space or serene location",
        "pose": "Calm centered pose, peaceful stance",
        "body_position": "Peaceful confidence, balanced energy",
        "face_angle": "Serene, peaceful, balanced angle",
        "expression": "Calm, peaceful, centered, mindful",
        "lighting": "Clean minimalist lighting, soft and balanced",
        "background": "Minimalist backdrop, clean serene setting",
        "vibe": "Calm, balance, mindfulness, contemporary peace",
    },
}


# ============================================================================
# FESTIVE SCENARIOS (Celebrations, Festivals, Joyful)
# ============================================================================

FESTIVE_SCENARIOS = {
    "traditional_festival": {
        "setting": "Traditional festival venue or cultural celebration",
        "pose": "Joyful celebratory pose, festive energy",
        "body_position": "Festive confidence, celebratory posture",
        "face_angle": "Radiant joyful angle, celebration-ready",
        "expression": "Joyful, celebratory, radiant, festive",
        "lighting": "Warm festive lighting, celebration glow",
        "background": "Festival decorations, traditional celebration elements",
        "vibe": "Tradition, celebration, joy, cultural festivity",
    },

    "modern_celebration": {
        "setting": "Contemporary party or modern celebration space",
        "pose": "Energetic dynamic pose, party confident",
        "body_position": "Energetic celebratory posture, party ready",
        "face_angle": "Dynamic joyful angle, celebration excitement",
        "expression": "Excited, energetic, joyful, celebratory",
        "lighting": "Contemporary party lighting, celebratory atmosphere",
        "background": "Modern celebration setting, contemporary party elements",
        "vibe": "Modern celebration, energy, joy, contemporary festivity",
    },

    "fusion_festival": {
        "setting": "Blended cultural celebration or fusion festival",
        "pose": "Confident joyful pose, culturally aware",
        "body_position": "Celebration confidence, cultural fusion energy",
        "face_angle": "Radiant inclusive angle, celebration blend",
        "expression": "Joyful, culturally embracing, celebratory warmth",
        "lighting": "Blended festive lighting, fusion celebration glow",
        "background": "Fusion celebration elements, blended cultural backdrop",
        "vibe": "Celebration, fusion, cultural appreciation, joy",
    },

    "night_celebration": {
        "setting": "Evening celebration venue with festive lights",
        "pose": "Glamorous celebratory pose, night ready",
        "body_position": "Elegant celebration confidence, festive glamour",
        "face_angle": "Glamorous radiant angle, celebration glow",
        "expression": "Glamorous, celebratory, radiant evening joy",
        "lighting": "Festive evening lights, celebration glamour",
        "background": "Celebration lighting, festive evening elements",
        "vibe": "Glamour, celebration, evening joy, festive elegance",
    },
}


# ============================================================================
# WEDDING SCENARIOS (Weddings, Formal Ceremonies)
# ============================================================================

WEDDING_SCENARIOS = {
    "traditional_bridal": {
        "setting": "Traditional wedding venue, mandap, or celebration space",
        "pose": "Radiant bridal confidence, ceremonial poise",
        "body_position": "Elegant formal posture, bridal grace",
        "face_angle": "Radiant joyful bridal angle, celebration ready",
        "expression": "Radiant, joyful, confident, romantic bridal",
        "lighting": "Warm romantic bridal lighting, celebration glow",
        "background": "Decorated wedding venue, traditional celebration backdrop",
        "vibe": "Tradition, romance, celebration, bridal radiance",
    },

    "modern_bridal": {
        "setting": "Contemporary wedding space or modern celebration venue",
        "pose": "Contemporary confident bridal pose, modern elegance",
        "body_position": "Modern formal confidence, contemporary bridal grace",
        "face_angle": "Elegant modern bridal angle, sophisticated celebration",
        "expression": "Radiant, sophisticated, modern bridal confidence",
        "lighting": "Contemporary professional bridal lighting, modern glow",
        "background": "Modern wedding venue, contemporary celebration backdrop",
        "vibe": "Modern romance, contemporary elegance, celebration",
    },

    "fusion_wedding": {
        "setting": "Blended cultural wedding celebration",
        "pose": "Elegant blended confidence, cultural aware",
        "body_position": "Fusion formal confidence, culturally graceful",
        "face_angle": "Radiant fusion angle, blended celebration",
        "expression": "Radiant, culturally embracing, joyful fusion",
        "lighting": "Fusion celebration lighting, blended cultural glow",
        "background": "Fusion wedding elements, blended cultural backdrop",
        "vibe": "Fusion, celebration, cultural appreciation, romance",
    },

    "pre_wedding": {
        "setting": "Pre-wedding celebration or engagement setting",
        "pose": "Joyful confident pose, celebration glow",
        "body_position": "Celebration confidence, joyful posture",
        "face_angle": "Joyful excited angle, celebration ready",
        "expression": "Excited, joyful, confident, celebrating love",
        "lighting": "Warm celebratory lighting, joyful glow",
        "background": "Celebration setting, joyful backdrop",
        "vibe": "Joy, love, celebration, excitement",
    },
}


# ============================================================================
# CREATIVE SCENARIOS (Art, Fashion, Editorial, Artistic)
# ============================================================================

CREATIVE_SCENARIOS = {
    "fashion_editorial": {
        "setting": "Fashion shoot set or editorial studio",
        "pose": "Bold fashion pose, runway ready",
        "body_position": "Fashion confident, editorial posture",
        "face_angle": "Fashion forward angle, editorial intense",
        "expression": "Confident, fashion-aware, editorial attitude",
        "lighting": "Professional fashion lighting, editorial dramatic",
        "background": "Fashion backdrop, editorial professional setting",
        "vibe": "Fashion, attitude, editorial confidence, runway",
    },

    "artistic_conceptual": {
        "setting": "Artistic set or conceptual space",
        "pose": "Artistic expressive pose, concept aware",
        "body_position": "Artistic confidence, conceptual energy",
        "face_angle": "Artistic interpretive angle, expressive",
        "expression": "Artistic, expressive, thoughtful, conceptual",
        "lighting": "Artistic atmospheric lighting, mood driven",
        "background": "Artistic elements, conceptual backdrop",
        "vibe": "Artistry, expression, conceptual, creativity",
    },

    "cultural_narrative": {
        "setting": "Cultural setting reflecting narrative",
        "pose": "Storytelling pose, narrative aware",
        "body_position": "Cultural confidence, narrative posture",
        "face_angle": "Expressive narrative angle, story telling",
        "expression": "Expressive, culturally grounded, narrative depth",
        "lighting": "Atmospheric narrative lighting, story glow",
        "background": "Cultural narrative backdrop, story setting",
        "vibe": "Culture, narrative, storytelling, artistic depth",
    },

    "high_fashion": {
        "setting": "High fashion set or luxury backdrop",
        "pose": "High fashion statement pose, luxury ready",
        "body_position": "Luxury confidence, high fashion posture",
        "face_angle": "High fashion editorial angle, luxury intense",
        "expression": "Sophisticated, fashion intense, luxury attitude",
        "lighting": "Professional high fashion lighting, luxurious",
        "background": "Luxury backdrop, high fashion professional",
        "vibe": "Luxury, high fashion, sophisticated attitude",
    },
}


# ============================================================================
# LIFESTYLE SCENARIOS (Daily life, lifestyle content)
# ============================================================================

LIFESTYLE_SCENARIOS = {
    "home_comfort": {
        "setting": "Home interior or comfortable home space",
        "pose": "Comfortable home pose, at-home ease",
        "body_position": "Relaxed home comfort, comfortable posture",
        "face_angle": "Warm comfortable angle, home contentment",
        "expression": "Warm, comfortable, genuine, home peace",
        "lighting": "Soft warm home lighting, comfortable glow",
        "background": "Home interior, comfortable home backdrop",
        "vibe": "Comfort, home warmth, genuine relaxation",
    },

    "active_lifestyle": {
        "setting": "Active lifestyle location or gym setting",
        "pose": "Active confident pose, fitness ready",
        "body_position": "Active confident posture, energetic",
        "face_angle": "Determined active angle, fitness focus",
        "expression": "Determined, energetic, motivated, active",
        "lighting": "Bright energetic lighting, active glow",
        "background": "Fitness environment, active backdrop",
        "vibe": "Fitness, motivation, energy, active lifestyle",
    },

    "family_moments": {
        "setting": "Family gathering or family space",
        "pose": "Warm family moment pose, relational",
        "body_position": "Warm relational posture, family comfort",
        "face_angle": "Warm loving angle, family connection",
        "expression": "Warm, loving, genuine family connection",
        "lighting": "Warm natural family lighting, intimate glow",
        "background": "Family space, intimate family backdrop",
        "vibe": "Family, love, connection, warmth",
    },

    "nature_outdoor": {
        "setting": "Nature or outdoor location",
        "pose": "Natural outdoor pose, nature ease",
        "body_position": "Relaxed outdoor posture, nature comfort",
        "face_angle": "Natural outdoor angle, peaceful",
        "expression": "Peaceful, connected to nature, outdoor joy",
        "lighting": "Natural outdoor lighting, golden hour feel",
        "background": "Nature backdrop, outdoor scenery",
        "vibe": "Nature, peace, outdoor joy, connection",
    },
}


# ============================================================================
# SCENARIO SELECTION FUNCTIONS
# ============================================================================

SCENARIO_POOLS = {
    Occasion.PROFESSIONAL: PROFESSIONAL_SCENARIOS,
    Occasion.CASUAL: CASUAL_SCENARIOS,
    Occasion.FESTIVE: FESTIVE_SCENARIOS,
    Occasion.WEDDING: WEDDING_SCENARIOS,
    Occasion.CREATIVE: CREATIVE_SCENARIOS,
    Occasion.LIFESTYLE: LIFESTYLE_SCENARIOS,
}


def get_scenarios_for_occasion(occasion: str) -> Dict[str, Dict]:
    """Get all available scenarios for an occasion.

    Args:
        occasion: Occasion type (professional, casual, etc.)

    Returns:
        Dictionary of scenarios for this occasion
    """
    try:
        occ = Occasion(occasion.lower())
        return SCENARIO_POOLS.get(occ, SCENARIO_POOLS[Occasion.CASUAL])
    except ValueError:
        # Default to casual if occasion not recognized
        return SCENARIO_POOLS[Occasion.CASUAL]


def get_scenario_list_for_occasion(occasion: str) -> List[str]:
    """Get list of scenario names for an occasion.

    Args:
        occasion: Occasion type

    Returns:
        List of scenario names
    """
    scenarios = get_scenarios_for_occasion(occasion)
    return list(scenarios.keys())


def get_scenario_details(occasion: str, scenario_name: str) -> Optional[Dict]:
    """Get details for a specific scenario.

    Args:
        occasion: Occasion type
        scenario_name: Scenario name

    Returns:
        Scenario details dictionary or None if not found
    """
    scenarios = get_scenarios_for_occasion(occasion)
    return scenarios.get(scenario_name)


def select_diverse_scenarios(
    occasion: str,
    count: int = 3,
    exclude: Optional[List[str]] = None,
) -> List[str]:
    """Select diverse scenarios for an occasion.

    Args:
        occasion: Occasion type
        count: Number of scenarios to select
        exclude: Scenario names to exclude

    Returns:
        List of selected scenario names
    """
    all_scenarios = get_scenario_list_for_occasion(occasion)
    exclude = exclude or []

    # Filter out excluded scenarios
    available = [s for s in all_scenarios if s not in exclude]

    # If we have enough, return first `count` diverse ones
    if len(available) >= count:
        return available[:count]

    # If not enough, return all available
    return available
