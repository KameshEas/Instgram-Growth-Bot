"""Dynamic context builder for non-transform categories.

Injects category-specific structural guidance + user's niche/topic into LLM prompts,
ensuring every /generate call reflects both the fixed category's domain conventions
AND the user's actual free-text niche/topic input (never a static menu of preset topics).

This is NOT a preset picker. It composes guidance per-request based on:
- Category (fixed, from CATEGORY_META)
- User's actual free-text niche/topic (dynamic, varies per request)
- User's custom idea/requirement (dynamic)

Reuses visual_systems knowledge only as deterministic technical guardrails
(negative-prompt safety nets, camera vocabulary), never as creative preset selection.
"""

from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DynamicContextBuilder:
    """Build dynamic, per-request context guidance for non-transform categories."""

    # Category-specific structural guidance (NOT creative presets, NOT topic-specific)
    # These describe what good output looks like for each category
    CATEGORY_GUIDANCE = {
        "general_photography": """
🎯 STRUCTURAL GUIDANCE: General Photography
- Focus: Authentic, expressive human photography
- Quality: Photorealistic, professional-grade
- Emphasis: Lighting, composition, natural beauty
- Avoid: Stock photo clichés, artificial poses
        """,

        "women_professional": """
🎯 STRUCTURAL GUIDANCE: Professional Portraits (Women)
- Focus: Professional confidence, competence, approachability
- Composition: Head/shoulders or full-body in work context
- Lighting: Even, flattering, emphasizes features not shadows
- Background: Minimal distraction, context-appropriate (office, etc.)
- Avoid: Overly glamorous styling, inappropriate office attire
        """,

        "men_professional": """
🎯 STRUCTURAL GUIDANCE: Professional Portraits (Men)
- Focus: Professional authority, trustworthiness, competence
- Composition: Head/shoulders or full-body in work context
- Lighting: Even, mature, emphasizes strength and reliability
- Background: Minimal distraction, context-appropriate
- Avoid: Casual styling, unprofessional attire, overly trendy
        """,

        "couples_general": """
🎯 STRUCTURAL GUIDANCE: Couple Photography
- Focus: Genuine connection, emotion, chemistry between subjects
- Composition: Both subjects equally visible and engaged
- Lighting: Flattering to both, creates intimacy not drama
- Background: Complements the couple, doesn't compete
- Avoid: One person dominating frame, awkward body language
        """,

        "design_posters": """
🎯 STRUCTURAL GUIDANCE: Poster Design
- Focus: Bold, attention-grabbing visual hierarchy
- Composition: Strong focal point, clear information flow
- Typography: Readable at distance, complements imagery
- Color: High contrast, vibrant if appropriate to topic
- Avoid: Cluttered layouts, illegible text, competing elements
        """,

        "design_gifts": """
🎯 STRUCTURAL GUIDANCE: Gift/Merchandise Design
- Focus: Print-ready design for merchandise (apparel, mugs, etc.)
- Composition: Balanced for product wrap (consider dimensions)
- Colors: Vibrant, durable under printing process
- Resolution: High DPI suitable for merchandise production
- Avoid: Complex details that don't print well, thin lines
        """,

        "print_design": """
🎯 STRUCTURAL GUIDANCE: Print Design Collateral
- Focus: Professional, print-optimized layout
- Composition: Balanced, respects margins and bleed areas
- Typography: Print-safe fonts, high contrast for readability
- Colors: CMYK-compatible, print-optimized palette
- Avoid: Screen-only design, thin lines, insufficient contrast
        """,

        "ui_ux_design": """
🎯 STRUCTURAL GUIDANCE: UI/UX Design
- Focus: Clean interface, intuitive user experience, modern aesthetic
- Composition: Information hierarchy, logical component grouping
- Style: Contemporary, accessibility-conscious, device-appropriate
- Detail: Buttons, icons, spacing, states all visible and polished
- Avoid: Cluttered interfaces, poor contrast, unclear interactions
        """,

        "brand_identity": """
🎯 STRUCTURAL GUIDANCE: Brand Identity / Logo Branding
- Focus: Memorable, scalable, works in single-color
- Composition: Negative space, balanced proportions
- Concept: Timeless, distinct, legally defensible (no copycat)
- Detail: Legible at thumbnail size, versatile across mediums
- Avoid: Trendy designs, overly complex, photorealistic elements
        """,

        "illustration_art": """
🎯 STRUCTURAL GUIDANCE: Digital Illustration
- Focus: Artistic expression, unique style, emotional impact
- Composition: Deliberate visual flow, focal point hierarchy
- Style: Consistent illustrative approach (painterly, graphic, mixed)
- Mood: Cohesive emotional tone throughout composition
- Avoid: Photorealistic (for illustration category), lack of style
        """,

        "animation_motion": """
🎯 STRUCTURAL GUIDANCE: Animation / Motion Graphics Concept
- Focus: Dynamic movement, visual rhythm, clear action
- Composition: Anticipates motion, suggests velocity/impact
- Style: Consistent animation style (2D, 3D, mixed)
- Keyframes: Key poses/frames visible, progression clear
- Avoid: Static poses, unclear motion direction
        """,

        "photography_styles": """
🎯 STRUCTURAL GUIDANCE: Fine Art / Style-Focused Photography
- Focus: Artistic vision, distinctive visual style
- Composition: Creative use of light, shadow, geometry
- Style: Signature aesthetic (vintage, surreal, minimalist, etc.)
- Mood: Strong emotional or conceptual underpinning
- Avoid: Conventional photography, generic subject matter
        """,

        "product_3d": """
🎯 STRUCTURAL GUIDANCE: 3D Product Render
- Focus: Professional product showcase, material realism
- Lighting: Studio lighting rig, emphasizes materials and form
- Angle: Hero angle (3/4 view typical), sometimes turntable
- Materials: Photorealistic PBR properties, surface details
- Background: Clean, non-distracting, highlights product
- Avoid: Blurry details, unrealistic material behavior
        """,

        "logo_create": """
🎯 STRUCTURAL GUIDANCE: Logo Design
- Focus: Memorable, scalable, works in single-color and color
- Concept: Brand essence distilled to simple, distinctive form
- Spacing: Proper negative space, balanced proportions
- Versatility: Functions at small sizes, across all mediums
- Avoid: Photorealistic elements, trendy styles, complexity
        """,

        # Text-content categories
        "reel_scripts": """
🎯 STRUCTURAL GUIDANCE: Instagram Reel Scripts
- Focus: Hook within first 0.5 seconds, maintain engagement
- Structure: Opening hook → Body content → Clear CTA
- Length: 15-60 seconds typical (use pacing cues if available)
- Tone: Platform-appropriate, energetic, authentic
- Elements: Visual cues, music timing, text overlays as needed
        """,

        "captions_templates": """
🎯 STRUCTURAL GUIDANCE: Instagram Caption Copy
- Focus: Compelling hook that stops the scroll
- Structure: Opening hook → Story/value → CTA (save/comment/DM)
- Length: 125-300 characters for mobile-first reading
- Tone: Brand voice, conversational, authentic
- Elements: Emojis for visual interest, line breaks for scannability
        """,

        "email_subjects": """
🎯 STRUCTURAL GUIDANCE: Email Subject Lines
- Focus: High open rate, curiosity + clarity balance
- Length: 50 characters ideal (preview line cutoff consideration)
- Tone: Urgent/curious/benefit-driven without clickbait
- Personalization: Optional but effective (name, segment cues)
- Avoid: ALL CAPS, spam trigger words, misleading claims
        """,
    }

    # Technical guardrails from visual_systems (deterministic, never creative presets)
    TECHNICAL_GUARDRAILS = {
        "general_photography": {
            "negative_keywords": ["stock photo", "cliché pose", "plastic look", "cartoon"],
            "camera_hint": "professional DSLR or mirrorless",
        },
        "women_professional": {
            "negative_keywords": ["overly glamorous", "unflattering shadows", "inappropriate attire"],
            "camera_hint": "professional portrait lens (50mm-85mm equivalent)",
        },
        "men_professional": {
            "negative_keywords": ["casual appearance", "poor lighting", "distracting background"],
            "camera_hint": "professional portrait lens (50mm-85mm equivalent)",
        },
        "couples_general": {
            "negative_keywords": ["awkward body language", "unbalanced composition", "stiff poses"],
            "camera_hint": "professional portrait setup",
        },
        "design_posters": {
            "negative_keywords": ["illegible text", "cluttered layout", "muddy colors"],
            "camera_hint": "N/A (design category)",
        },
        "design_gifts": {
            "negative_keywords": ["thin lines that won't print", "complex fine details", "screen-only effects"],
            "camera_hint": "N/A (design category)",
        },
        "print_design": {
            "negative_keywords": ["thin lines", "low contrast text", "CMYK-incompatible colors"],
            "camera_hint": "N/A (design category)",
        },
        "ui_ux_design": {
            "negative_keywords": ["cluttered interface", "poor contrast", "unclear interactions"],
            "camera_hint": "N/A (UI category)",
        },
        "brand_identity": {
            "negative_keywords": ["photorealistic elements", "trendy design", "overly complex"],
            "camera_hint": "N/A (design category)",
        },
        "illustration_art": {
            "negative_keywords": ["photorealistic", "inconsistent style", "lack of coherence"],
            "camera_hint": "N/A (illustration category)",
        },
        "animation_motion": {
            "negative_keywords": ["static pose", "unclear movement", "inconsistent style"],
            "camera_hint": "N/A (animation category)",
        },
        "photography_styles": {
            "negative_keywords": ["generic photography", "conventional subject", "lack of artistic vision"],
            "camera_hint": "professional fine-art photography",
        },
        "product_3d": {
            "negative_keywords": ["blurry details", "unrealistic materials", "poor lighting"],
            "camera_hint": "3D render with photorealistic settings",
        },
        "logo_create": {
            "negative_keywords": ["photorealistic", "trendy design", "too complex", "hard to scale"],
            "camera_hint": "N/A (design category)",
        },
    }

    @staticmethod
    def build_category_guidance(
        category: str,
        niche: str = "",
        user_idea: str = "",
    ) -> str:
        """Build dynamic context guidance for a category.

        Args:
            category: Fixed category name (from CATEGORY_META)
            niche: Free-text user-provided niche/topic (e.g., "underwater welding", "luxury travel")
            user_idea: Additional free-text user requirement/idea

        Returns:
            Formatted guidance string to inject into LLM prompt.
            Never a preset; always composed fresh per request incorporating the user's actual niche.
        """
        try:
            # Get base structural guidance for this category
            base_guidance = DynamicContextBuilder.CATEGORY_GUIDANCE.get(
                category,
                f"Generate high-quality content for the '{category}' category."
            )

            # Build niche-specific instruction (the dynamic part)
            niche_instruction = ""
            if niche:
                niche_instruction = f"""
NICHE/TOPIC SPECIFICATION (Apply exactly as stated, do not substitute):
- Niche: {niche.strip()}
"""

            # Add user's custom idea if provided
            custom_instruction = ""
            if user_idea:
                custom_instruction = f"- User's specific requirement: {user_idea.strip()}\n"

            # Add technical guardrails (deterministic per category)
            guardrails = DynamicContextBuilder.TECHNICAL_GUARDRAILS.get(category, {})
            guardrail_text = ""
            if guardrails.get("negative_keywords"):
                negative_list = ", ".join(guardrails["negative_keywords"])
                guardrail_text += f"""
QUALITY GUARDRAILS:
- Avoid: {negative_list}
"""

            # Compose final guidance section
            guidance_section = f"""{base_guidance}{niche_instruction}{custom_instruction}{guardrail_text}
"""

            return guidance_section

        except Exception as e:
            logger.error(f"Error building category guidance for {category}: {e}")
            # Fallback: minimal but safe guidance
            return f"Generate content for the '{category}' category.\n"
