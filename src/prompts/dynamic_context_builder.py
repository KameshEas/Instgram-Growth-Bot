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
        "general_photography": """Category guidance: general photography
- Goal: a photorealistic image that looks like it was taken by a skilled photographer. The subject can be people, places, objects, food, or nature, whatever the idea describes.
- Composition: one clear subject, deliberate framing (rule of thirds, leading lines, or symmetry).
- Lighting: motivated, natural-looking light that suits the scene and time of day.
- Avoid: stock-photo clichés and stiff, posed looks.""",

        "women_professional": """Category guidance: professional portrait
- Goal: a portrait that reads as competent, confident, and approachable, suitable for LinkedIn, a company website, or a speaker profile.
- Composition: head-and-shoulders or waist-up, eyes in the upper third, subject in a relevant work setting or a clean backdrop.
- Lighting: soft, even key light with gentle fill; flattering and natural.
- Styling: polished business or business-casual attire that fits the subject's field.
- Avoid: distracting backgrounds, heavy retouching, harsh shadows.""",

        "men_professional": """Category guidance: professional portrait
- Goal: a portrait that reads as competent, confident, and approachable, suitable for LinkedIn, a company website, or a speaker profile.
- Composition: head-and-shoulders or waist-up, eyes in the upper third, subject in a relevant work setting or a clean backdrop.
- Lighting: soft, even key light with gentle fill; flattering and natural.
- Styling: polished business or business-casual attire that fits the subject's field.
- Avoid: distracting backgrounds, heavy retouching, harsh shadows.""",

        # Transform categories normally get scenario + styling sections; these entries cover the
        # no-custom-text path (category buttons), which previously got only a generic line.
        "women_transform": """Category guidance: transformation of the creator's own photo
- Goal: place the person from the creator's reference photo into a new, flattering scene or look.
- Identity: every prompt starts with "Using the reference photo," and states that the face, skin tone, hair, and body proportions stay identical. The person must remain recognisably the same individual; never morph, swap, or alter their identity.
- Variety: change the setting, outfit, pose, and lighting between variations, not the person.
- Avoid: different faces, idealised or changed body shapes, plastic or over-retouched skin.""",

        "men_transform": """Category guidance: transformation of the creator's own photo
- Goal: place the person from the creator's reference photo into a new, flattering scene or look.
- Identity: every prompt starts with "Using the reference photo," and states that the face, skin tone, hair, and body proportions stay identical. The person must remain recognisably the same individual; never morph, swap, or alter their identity.
- Variety: change the setting, outfit, pose, and lighting between variations, not the person.
- Avoid: different faces, idealised or changed body shapes, plastic or over-retouched skin.""",

        "couples_transform": """Category guidance: transformation of a couple's own photo
- Goal: place both people from the couple's reference photo into a new, romantic or fun scene.
- Identity: every prompt starts with "Using the reference photo," and states that both people keep their exact faces, skin tones, hair, and body proportions. Exactly two people; never morph, swap, merge, or alter either identity.
- Composition: both people clearly visible and interacting naturally; neither dominates the frame.
- Variety: change the setting, outfits, pose, and lighting between variations, not the people.
- Avoid: extra people, swapped or merged faces, changed body shapes.""",

        "couples_general": """Category guidance: couple photography
- Goal: genuine connection and emotion between two people.
- Composition: both people clearly visible and engaged with each other or the camera; neither dominates the frame.
- Lighting: flattering for both faces; warm and intimate rather than dramatic.
- Background: complements the couple without competing for attention.
- Avoid: awkward body language, one person cut off or out of focus.""",

        "design_posters": """Category guidance: poster design
- Goal: a bold poster with a clear visual hierarchy: headline, key image, supporting details.
- Composition: one strong focal point and a clear reading order; space reserved for the headline.
- Typography: legible from a distance; describe font style (for example bold condensed sans-serif).
- Color: high contrast between text and background.
- Avoid: cluttered layouts, illegible or misspelled text, competing focal points.""",

        "design_gifts": """Category guidance: gift and merchandise design
- Goal: an artwork that prints well on the named product (t-shirt, mug, pillow, and so on).
- Composition: centered or wrap-friendly as the product requires; artwork on a plain or transparent background, not a photo of the product, unless the idea asks for a mockup.
- Colors: a limited, saturated palette that survives printing.
- Detail: bold shapes and lines; text large enough to read on the product.
- Avoid: hairline details, tiny text, photographic gradients that print poorly.""",

        "print_design": """Category guidance: print collateral (flyers, brochures, cards)
- Goal: a print-ready layout with clear hierarchy.
- Composition: balanced grid with safe margins and room for bleed.
- Typography: readable body text sizes, high contrast.
- Colors: a palette that reproduces well in CMYK printing.
- Avoid: screen-only effects such as neon glow, thin lines, low-contrast text.""",

        "ui_ux_design": """Category guidance: UI/UX showcase
- Goal: a clean, modern interface mockup that shows a believable product screen.
- Composition: clear information hierarchy, consistent spacing, logically grouped components.
- Detail: readable labels, recognisable buttons and icons, realistic content rather than lorem ipsum.
- Presentation: flat screen view or device mockup, as the idea suggests.
- Avoid: cluttered screens, low contrast, unreadable text.""",

        "brand_identity": """Category guidance: brand identity and logo branding
- Goal: a memorable, scalable mark that works in one color.
- Composition: balanced proportions, purposeful negative space, presented on a plain background.
- Concept: a simple, distinctive idea tied to the brand; not a copy of a well-known logo.
- Detail: legible at small sizes.
- Avoid: photorealistic elements, gradients that break in one color, excessive detail.""",

        "illustration_art": """Category guidance: digital illustration
- Goal: an illustration with a distinctive, consistent style and a clear emotional tone.
- Composition: deliberate visual flow toward one focal point.
- Style: name the technique (for example flat vector, gouache, ink and watercolor, cel-shaded).
- Avoid: photorealism, mixed inconsistent styles.""",

        "animation_motion": """Category guidance: animation and motion concept art
- Goal: a single frame that implies movement and energy.
- Composition: dynamic angles, motion lines or blur, a pose caught mid-action.
- Style: name the animation style (for example 2D anime, 3D Pixar-like, motion-graphics flat).
- Avoid: static, stiff poses and unclear direction of motion.""",

        "photography_styles": """Category guidance: fine-art and style-led photography
- Goal: a photograph with a distinctive artistic style and a clear concept.
- Composition: creative use of light, shadow, geometry, or color.
- Style: name the look (for example film noir, double exposure, 1970s film, minimalist).
- Avoid: generic, conventional snapshots.""",

        "product_3d": """Category guidance: 3D product render
- Goal: a professional product hero shot with realistic materials.
- Lighting: studio lighting setup that shows form and material (for example three-point softbox with rim light).
- Angle: hero three-quarter view unless the idea asks for another.
- Materials: describe physically based surfaces (brushed aluminum, matte plastic, frosted glass).
- Background: clean seamless backdrop or a simple styled surface.
- Avoid: blurry details, unrealistic reflections, clutter.""",

        "logo_create": """Category guidance: logo design
- Goal: a simple, distinctive logo that works in full color and in one color, from favicon size to billboard.
- Composition: the logo alone, centered on a plain or transparent background, with clear space around it.
- Concept: the brand's essence reduced to a simple form; follow every value in <reference> exactly, including brand name spelling, colors, and logo type.
- Avoid: photorealistic elements, fine detail that disappears at small sizes, mockups unless requested.""",

        "reel_scripts": """Category guidance: Instagram Reel scripts
- Hook in the first 1 to 2 seconds, then the value, then a clear CTA.
- Length 15 to 45 seconds, written as timed beats with on-screen text cues.
- Tone: energetic, natural, and spoken, not written-essay style.""",

        "captions_templates": """Category guidance: Instagram captions
- Hook in the first line, then value or story, then a CTA (save, comment, share, or DM).
- 125 to 300 characters, line breaks for scannability, up to 3 emojis.
- Tone: conversational and true to the creator's niche.""",

        "email_subjects": """Category guidance: email subject lines
- 50 characters or fewer, clear benefit or honest curiosity.
- No all-caps words, no spam-trigger phrases, no misleading claims.""",
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
        """Build per-request guidance for a category (inserted into <constraints>)."""
        try:
            base_guidance = DynamicContextBuilder.CATEGORY_GUIDANCE.get(
                category,
                f"Category guidance: {category.replace('_', ' ')}\n- Goal: high-quality output that matches the creator's idea.",
            )

            niche_instruction = ""
            if niche:
                niche_instruction = (
                    f"\n- Niche: {niche.strip()}. Make the subject, setting, and details clearly "
                    f"belong to this niche; do not substitute a different niche."
                )

            custom_instruction = ""
            if user_idea:
                # The idea itself is already in <user_idea>; point to it rather than copying it here.
                custom_instruction = "\n- The creator's idea in <user_idea> defines the subject. Apply this guidance to that idea."

            guardrails = DynamicContextBuilder.TECHNICAL_GUARDRAILS.get(category, {})
            guardrail_text = ""
            if guardrails.get("negative_keywords"):
                negative_list = ", ".join(guardrails["negative_keywords"])
                guardrail_text = f"\n- Also avoid: {negative_list}. Include the relevant ones in negative_prompt."

            return f"{base_guidance}{niche_instruction}{custom_instruction}{guardrail_text}\n"

        except Exception as e:
            logger.error(f"Error building category guidance for {category}: {e}")
            return f"Category guidance: {category.replace('_', ' ')}\n"
