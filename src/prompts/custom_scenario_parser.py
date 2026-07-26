"""Parse custom user requirements and extract scenario/location/mood."""

import re
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class CustomScenarioParser:
    """Extract location, mood, and context from user's custom requirement."""

    # Location keywords and their variations
    LOCATION_KEYWORDS = {
        "beach": ["beach", "seaside", "shore", "coast", "ocean", "sea", "sandy"],
        "mountain": ["mountain", "hill", "peak", "alpine", "forest", "woods"],
        "urban": ["city", "urban", "street", "downtown", "metro", "building"],
        "cafe": ["cafe", "coffee", "restaurant", "bistro", "bar", "lounge"],
        "garden": ["garden", "park", "nature", "outdoor", "outdoor", "natural"],
        "home": ["home", "indoor", "room", "living", "bedroom", "house"],
        "studio": ["studio", "blank", "minimalist", "studio", "backdrop"],
        "wedding": ["wedding", "ceremony", "bride", "groom", "altar"],
        "office": ["office", "corporate", "business", "professional", "work"],
        "creative": ["creative", "artistic", "gallery", "art", "studio"],
    }

    # Mood/Vibe keywords
    MOOD_KEYWORDS = {
        "relaxed": ["relaxed", "chill", "calm", "peaceful", "serene", "mellow"],
        "energetic": ["energetic", "vibrant", "dynamic", "active", "lively"],
        "mysterious": ["mysterious", "moody", "dark", "dramatic", "edgy"],
        "romantic": ["romantic", "intimate", "sensual", "passionate", "love"],
        "professional": ["professional", "corporate", "business", "formal", "serious"],
        "playful": ["playful", "fun", "happy", "cheerful", "joyful"],
        "artistic": ["artistic", "creative", "conceptual", "experimental", "unique"],
        "nature": ["nature", "natural", "organic", "earthy", "wild"],
    }

    @staticmethod
    def extract_location(text: str) -> Tuple[str, str]:
        """Extract primary location and mood from custom requirement.

        Args:
            text: User's custom requirement text

        Returns:
            Tuple of (location, mood) or ("generic", "neutral") if not found
        """
        text_lower = text.lower()

        # Find location
        location = "generic"
        location_found = None
        for loc, keywords in CustomScenarioParser.LOCATION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    location = loc
                    location_found = keyword
                    break
            if location_found:
                break

        # Find mood
        mood = "neutral"
        for m, keywords in CustomScenarioParser.MOOD_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    mood = m
                    break

        logger.info(f"[PARSER] Extracted location={location}, mood={mood} from '{text}'")
        return location, mood

    @staticmethod
    def generate_pose_variations(location: str, mood: str, count: int = 3) -> List[Dict[str, str]]:
        """Generate pose variations for the same location.

        Args:
            location: Primary location extracted
            mood: Primary mood/vibe extracted
            count: Number of variations (default 3)

        Returns:
            List of pose variation dictionaries
        """

        pose_variations = {
            "beach": [
                {
                    "pose": "sitting on the sand",
                    "body_position": "seated with legs extended",
                    "expression": "contemplative gaze toward horizon",
                    "activity": "enjoying the ocean breeze"
                },
                {
                    "pose": "standing in shallow water",
                    "body_position": "standing confidently, slightly turned",
                    "expression": "serene, looking at the waves",
                    "activity": "wading in the shallow waves"
                },
                {
                    "pose": "walking along the shore",
                    "body_position": "natural walking stride",
                    "expression": "peaceful, looking down at sand",
                    "activity": "strolling barefoot on the beach"
                },
                {
                    "pose": "reclining on beach",
                    "body_position": "relaxed laying position",
                    "expression": "carefree, smiling at camera",
                    "activity": "sunbathing with relaxed attitude"
                },
                {
                    "pose": "leaning on rocks",
                    "body_position": "leaning against natural rocks",
                    "expression": "confident, gazing into distance",
                    "activity": "admiring the coastal scenery"
                },
            ],
            "mountain": [
                {
                    "pose": "standing on peak",
                    "body_position": "standing tall, arms at sides",
                    "expression": "triumphant, looking at vista",
                    "activity": "enjoying mountain view"
                },
                {
                    "pose": "sitting on mountain edge",
                    "body_position": "seated with scenic backdrop",
                    "expression": "contemplative, peaceful",
                    "activity": "taking in the landscape"
                },
                {
                    "pose": "hiking pose",
                    "body_position": "mid-stride walking",
                    "expression": "determined, focused",
                    "activity": "trekking the mountain path"
                },
            ],
            "urban": [
                {
                    "pose": "walking street",
                    "body_position": "natural walking stride",
                    "expression": "confident, street style",
                    "activity": "urban wandering"
                },
                {
                    "pose": "leaning on building",
                    "body_position": "casual lean",
                    "expression": "cool, collected",
                    "activity": "against urban backdrop"
                },
                {
                    "pose": "standing at intersection",
                    "body_position": "standing confidently",
                    "expression": "fashionable, poised",
                    "activity": "urban exploration"
                },
            ],
            "garden": [
                {
                    "pose": "among flowers",
                    "body_position": "standing gracefully",
                    "expression": "serene, surrounded by nature",
                    "activity": "enjoying garden beauty"
                },
                {
                    "pose": "sitting on bench",
                    "body_position": "seated on garden bench",
                    "expression": "peaceful, contemplative",
                    "activity": "quiet garden moment"
                },
                {
                    "pose": "walking paths",
                    "body_position": "walking through garden",
                    "expression": "joyful, exploring",
                    "activity": "garden stroll"
                },
            ],
            "generic": [
                {
                    "pose": "standing pose",
                    "body_position": "standing confidently",
                    "expression": "direct, engaging",
                    "activity": "primary focus"
                },
                {
                    "pose": "seated pose",
                    "body_position": "seated comfortably",
                    "expression": "relaxed, approachable",
                    "activity": "seated interaction"
                },
                {
                    "pose": "walking pose",
                    "body_position": "natural movement",
                    "expression": "dynamic, alive",
                    "activity": "movement and energy"
                },
            ]
        }

        # Get variations for location, fallback to generic
        variations = pose_variations.get(location, pose_variations["generic"])

        # Return requested count
        return variations[:count]

    @staticmethod
    def build_custom_scenario_section(
        location: str,
        mood: str,
        original_requirement: str,
        count: int = 3
    ) -> str:
        """Build scenario guidance based on user's custom requirement.

        Args:
            location: Extracted location
            mood: Extracted mood
            original_requirement: Original user text
            count: Number of prompts

        Returns:
            Formatted scenario section for Groq prompt
        """

        pose_variations = CustomScenarioParser.generate_pose_variations(location, mood, count)

        scenario_section = f"""
🎬 CUSTOM SCENARIO EXTRACTION:
User's primary location: {location.upper()}
User's mood/vibe: {mood}
User's full requirement: "{original_requirement}"

CRITICAL: ALL {count} PROMPTS MUST USE THE SAME LOCATION: {location.upper()}
- Vary ONLY: pose, body position, expression, activity
- DO NOT change: location, scenery, environment context
- Each prompt shows a DIFFERENT POSE but SAME LOCATION

POSE VARIATION MANDATE:
"""

        for i, var in enumerate(pose_variations, 1):
            scenario_section += f"""
{i}️⃣ Pose Option {i}:
   - Position: {var['pose']}
   - Body: {var['body_position']}
   - Expression: {var['expression']}
   - Activity: {var['activity']}
"""

        scenario_section += f"""

LOCATION DETAILS:
- Setting: {location} environment with natural {mood} mood
- Background: Appropriate {location} scenery
- Lighting: Soft, natural lighting suited to {location}
- Atmosphere: Conveys {mood} feeling as requested

STRICT REQUIREMENT:
All {count} prompts MUST:
✅ Use {location} as the location
✅ Respect "{original_requirement}" requirement
✅ Vary pose and expression ONLY
✅ Keep same scenery/environment
✅ Preserve identity absolutely
"""

        return scenario_section
