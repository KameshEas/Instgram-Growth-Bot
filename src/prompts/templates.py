"""AI-Powered Prompt Generation Configuration
Architecture: Pure AI-generated prompts (no static library)
Categories are used by AI to understand available prompt types.
All generation is done via Groq AI, not from static library.
"""

# --- UNIVERSAL AI PROMPT SYSTEM PROMPT --------------------------------------------------
UNIVERSAL_PROMPT_SYSTEM_PROMPT = """You are an expert Prompt Engineer.

Your task is to transform the user's idea into three highly detailed AI prompts.

Generate prompts that work with:
• GPT Images
• Midjourney
• Flux
• Ideogram
• Stable Diffusion

Rules:

- Preserve every literal detail the user provides — exact headlines, names, titles,
  wording, and any explicit preservation constraints (e.g. "keep this exact face",
  "same location") must appear unchanged. Never invent replacement content or
  "creative alternatives" to what the user explicitly specified.
- Expand the scene with cinematic details: lighting, camera angle, composition,
  textures, atmosphere, colors, quality keywords, style-specific enhancements.
- Never generate design briefs, deliverables lists, or software recommendations.
- Never explain the prompt.
- Output only valid JSON.

Return:

{
  "variations": [
    {
      "title": "",
      "style": "",
      "prompt": "",
      "negative_prompt": "",
      "aspect_ratio": "",
      "keywords": []
    }
  ]
}
"""

# --- TEXT CONTENT SYSTEM PROMPT ---------------------------------------------------
# For reel_scripts, captions_templates, email_subjects (not image generation)
UNIVERSAL_TEXT_CONTENT_SYSTEM_PROMPT = """You are an expert Content Creator and Copywriter.

Your task is to generate high-performing social media and marketing content.

Rules:

- Preserve every literal detail the user provides — exact wording, names, topics,
  and any specific requirements must appear unchanged.
- Create content optimized for engagement, virality, and conversions.
- Content should be platform-appropriate and culturally sensitive.
- Never explain the content.
- Output only valid JSON.

Return:

{
  "variations": [
    {
      "title": "",
      "type": "",
      "content": "",
      "hook": "",
      "cta": "",
      "tone": "",
      "keywords": []
    }
  ]
}
"""

# --- CATEGORY METADATA (LIGHTWEIGHT) --------------------------------------------------
# Lightweight metadata: emoji + style hint only. All generation via universal prompt.
CATEGORY_META = {
    "general_photography":  {"emoji": "📷", "style": "photorealistic photography"},
    "women_professional":   {"emoji": "👩‍💼", "style": "professional portrait"},
    "women_transform":      {"emoji": "✨", "style": "portrait transformation with identity lock"},
    "men_professional":     {"emoji": "👨‍💼", "style": "professional portrait"},
    "men_transform":        {"emoji": "💪", "style": "portrait transformation with identity lock"},
    "couples_general":      {"emoji": "💑", "style": "couple lifestyle photography"},
    "couples_transform":    {"emoji": "💕", "style": "couple transformation with dual identity lock"},
    "design_posters":       {"emoji": "🎨", "style": "cinematic poster"},
    "design_gifts":         {"emoji": "🎁", "style": "product-aware merchandise design"},
    "reel_scripts":         {"emoji": "🎬", "style": "Instagram Reel video scripts"},
    "captions_templates":   {"emoji": "✍️", "style": "Instagram caption copy"},
    "email_subjects":       {"emoji": "📧", "style": "email subject lines"},
    "ui_ux_design":         {"emoji": "🖥️", "style": "modern UI showcase"},
    "brand_identity":       {"emoji": "🏷️", "style": "minimal logo branding"},
    "illustration_art":     {"emoji": "🖌️", "style": "digital illustration"},
    "animation_motion":     {"emoji": "🎞️", "style": "dynamic concept art"},
    "photography_styles":   {"emoji": "📸", "style": "fine-art photography"},
    "print_design":         {"emoji": "🖨️", "style": "print-ready collateral"},
    "product_3d":           {"emoji": "📦", "style": "3D product render"},
    "logo_create":          {"emoji": "🏛️", "style": "logo design with branding system"},
}

# Categories that use text-content system prompt (not image generation)
TEXT_CONTENT_CATEGORIES = {"reel_scripts", "captions_templates", "email_subjects"}

DIFFICULTY_EMOJI = {"beginner": "🟢", "professional": "🔵", "expert": "🔴"}

# --- GIFT PRODUCT METADATA -------------------------------------------------------
GIFT_PRODUCTS = {
    "t_shirt": {
        "emoji": "👕",
        "display_name": "T-Shirt",
        "printable_area": "1000x1200px front",
        "constraints": "Front design, consider seam positions, avoid placing text on shoulder seams",
        "best_for": "Personal, casual, graphic designs",
        "tools": ["DALL-E 3", "Midjourney", "Stable Diffusion"],
    },
    "mug": {
        "emoji": "☕",
        "display_name": "Mug",
        "printable_area": "900x350px wrap-around",
        "constraints": "Cylindrical wrap design, recommend vertical focus or repeating pattern",
        "best_for": "Coffee lovers, office gifts, daily use items",
        "tools": ["DALL-E 3", "Midjourney"],
    },
    "hoodie": {
        "emoji": "🧥",
        "display_name": "Hoodie",
        "printable_area": "1200x1500px front/back",
        "constraints": "Large canvas, sleeves and hood available for design extension",
        "best_for": "Bold graphics, logos, statement designs",
        "tools": ["DALL-E 3", "Midjourney", "Stable Diffusion"],
    },
    "pillow": {
        "emoji": "🛏️",
        "display_name": "Pillow",
        "printable_area": "1500x1500px square",
        "constraints": "Centered main focus, consider both sides if double-sided printing",
        "best_for": "Personal, decorative, photo/art prints",
        "tools": ["DALL-E 3", "Midjourney"],
    },
    "poster": {
        "emoji": "🖼️",
        "display_name": "Poster",
        "printable_area": "18x24 inches / 4320x5760px",
        "constraints": "Full canvas utilization, text readable from distance, high contrast",
        "best_for": "Wall art, motivational, photography, typography",
        "tools": ["DALL-E 3", "Midjourney", "Stable Diffusion"],
    },
    "hat": {
        "emoji": "🧢",
        "display_name": "Cap/Hat",
        "printable_area": "400x300px front",
        "constraints": "Limited front area, recommend simple logo or text, avoid complex details",
        "best_for": "Logos, brand marks, simple text",
        "tools": ["DALL-E 3", "Midjourney"],
    },
    "notebook": {
        "emoji": "📔",
        "display_name": "Notebook",
        "printable_area": "700x1000px cover",
        "constraints": "Book cover format, consider spine width (50px), front-focused design",
        "best_for": "Artistic covers, motivational quotes, brand identity",
        "tools": ["DALL-E 3", "Midjourney"],
    },
    "water_bottle": {
        "emoji": "💧",
        "display_name": "Water Bottle",
        "printable_area": "800x400px wrap",
        "constraints": "Cylindrical wrap, vertical focus recommended, repeating pattern works well",
        "best_for": "Active lifestyle, sports, minimalist designs",
        "tools": ["DALL-E 3", "Midjourney"],
    },
    "phone_case": {
        "emoji": "📱",
        "display_name": "Phone Case",
        "printable_area": "1080x2160px portrait",
        "constraints": "Consider curved phone edges, test design on curved surface, avoid critical elements on edges",
        "best_for": "Minimalist, high-contrast designs, personal style",
        "tools": ["DALL-E 3", "Midjourney"],
    },
    "sweater": {
        "emoji": "🧶",
        "display_name": "Sweater",
        "printable_area": "1100x1400px front",
        "constraints": "Cozy aesthetic, center-focused for chest placement, avoid tight cuffs",
        "best_for": "Seasonal, family groups, cozy designs",
        "tools": ["DALL-E 3", "Midjourney"],
    },
}

# --- DESIGN TONE PRESETS --------------------------------------------------------
GIFT_DESIGN_TONES = {
    "minimalist": "Clean, simple, modern, whitespace, sans-serif fonts, subtle colors",
    "playful": "Fun, colorful, whimsical, rounded elements, bright colors, approachable",
    "elegant": "Sophisticated, refined, premium feel, serif fonts, gold/silver accents, luxury",
    "sporty": "Dynamic, energetic, bold, angular shapes, vibrant colors, motion-implied",
    "vintage": "Retro, nostalgic, classic style, muted colors, decorative fonts, historical references",
    "artistic": "Creative, expressive, hand-drawn, mixed media, abstract, unique perspective",
    "professional": "Corporate, business-focused, formal, structured, dark colors, clean typography",
    "nature": "Organic, earthy, natural elements, botanical, outdoor-inspired, greens/browns",
    "tech": "Modern, futuristic, digital, geometric, neon accents, cutting-edge aesthetic",
    "romantic": "Love-focused, dreamy, soft colors, flowing shapes, hearts/decorative elements",
}

# --- PROFESSIONAL ROLES TAXONOMY ------------------------------------------------
PROFESSIONAL_ROLES = {
    "ui_ux_designer": {
        "emoji": "🎨",
        "display_name": "UI/UX Designer",
        "expertise": ["user experience", "interface design", "accessibility", "wireframing", "prototyping"],
        "guidance": "Focus on user-centered design principles, accessibility compliance, and intuitive interactions. Consider usability patterns and information architecture.",
        "tools": ["Figma", "Adobe XD", "Sketch", "DALL-E 3", "Midjourney"],
        "design_focus": "Interface-ready, pixel-perfect, accessibility-compliant"
    },
    "graphic_designer": {
        "emoji": "✏️",
        "display_name": "Graphic Designer",
        "expertise": ["visual design", "typography", "color theory", "composition", "branding"],
        "guidance": "Emphasize typography, color harmony, composition rules, and visual hierarchy. Consider print-ready specifications and design principles.",
        "tools": ["Adobe Creative Suite", "Illustrator", "Photoshop", "DALL-E 3", "Midjourney"],
        "design_focus": "Print-ready, color-harmonious, typographically-rich"
    },
    "developer": {
        "emoji": "💻",
        "display_name": "Developer",
        "expertise": ["code", "frontend development", "responsive design", "web standards", "performance"],
        "guidance": "Include technical specifications, responsive breakpoints, and implementation considerations. Focus on clean, implementable designs.",
        "tools": ["Figma", "CSS", "SVG", "DALL-E 3", "Midjourney"],
        "design_focus": "Web-optimized, responsive, CSS-friendly"
    },
    "content_creator": {
        "emoji": "📹",
        "display_name": "Content Creator",
        "expertise": ["social media", "video content", "storytelling", "engagement", "trending topics"],
        "guidance": "Focus on viral-worthy visuals, trending aesthetics, emotional resonance, and platform-specific optimization (Instagram, TikTok, YouTube).",
        "tools": ["Canva", "Adobe Premiere", "DALL-E 3", "Midjourney", "CapCut"],
        "design_focus": "Trend-aware, platform-optimized, engagement-focused"
    },
    "marketer": {
        "emoji": "📊",
        "display_name": "Marketer",
        "expertise": ["brand messaging", "campaign strategy", "target audience", "conversion optimization", "analytics"],
        "guidance": "Prioritize message clarity, audience targeting, call-to-action effectiveness, and brand consistency. Include conversion-optimized layouts.",
        "tools": ["Canva", "Adobe Creative Suite", "DALL-E 3", "Midjourney"],
        "design_focus": "Message-driven, conversion-optimized, audience-targeted"
    },
    "social_media_manager": {
        "emoji": "📱",
        "display_name": "Social Media Manager",
        "expertise": ["social platforms", "engagement metrics", "audience growth", "scheduling", "community management"],
        "guidance": "Design for specific platform dimensions, trending sounds/hashtags, optimal posting times. Focus on engagement and shareability.",
        "tools": ["Buffer", "Later", "Hootsuite", "Canva", "DALL-E 3", "Midjourney"],
        "design_focus": "Platform-native, engagement-optimized, on-trend"
    },
    "photographer": {
        "emoji": "📸",
        "display_name": "Photographer",
        "expertise": ["composition", "lighting", "color grading", "visual narrative", "post-processing"],
        "guidance": "Emphasize composition techniques, lighting setups, color grading possibilities, and visual storytelling. Consider depth of field and framing.",
        "tools": ["Lightroom", "Adobe Photoshop", "Capture One", "DALL-E 3", "Midjourney"],
        "design_focus": "Photographic, compositionally-strong, lighting-aware"
    },
    "brand_strategist": {
        "emoji": "🎯",
        "display_name": "Brand Strategist",
        "expertise": ["brand identity", "positioning", "messaging", "visual language", "market differentiation"],
        "guidance": "Focus on brand consistency, competitive differentiation, target market positioning, and long-term brand building. Include brand values in design.",
        "tools": ["Brand guidelines", "Adobe Creative Suite", "DALL-E 3", "Midjourney"],
        "design_focus": "Brand-aligned, market-differentiated, strategically-positioned"
    },
    "product_manager": {
        "emoji": "🛍️",
        "display_name": "Product Manager",
        "expertise": ["product strategy", "user needs", "feature prioritization", "roadmap", "metrics"],
        "guidance": "Include user value proposition, feature highlights, benefit-driven messaging, and measurable outcomes. Focus on product differentiation.",
        "tools": ["Figma", "ProductBoard", "DALL-E 3", "Midjourney"],
        "design_focus": "Value-driven, feature-highlighting, user-benefit-focused"
    },
    "illustrator": {
        "emoji": "🖼️",
        "display_name": "Illustrator",
        "expertise": ["illustration", "character design", "artistic style", "storytelling", "custom artwork"],
        "guidance": "Emphasize artistic style, character consistency, narrative elements, and illustrative techniques. Focus on custom artwork and unique perspectives.",
        "tools": ["Procreate", "Adobe Illustrator", "Clip Studio Paint", "DALL-E 3", "Midjourney"],
        "design_focus": "Artistically-driven, character-rich, illustratively-unique"
    },
    "motion_designer": {
        "emoji": "🎬",
        "display_name": "Motion Designer",
        "expertise": ["animation", "motion graphics", "transitions", "timing", "visual effects"],
        "guidance": "Include animation possibilities, timing cues, motion paths, and dynamic elements. Focus on movement and temporal aspects of design.",
        "tools": ["After Effects", "Cinema 4D", "Blender", "DALL-E 3", "Midjourney"],
        "design_focus": "Animation-capable, motion-aware, dynamic-element-rich"
    },
}

# --- HELPER FUNCTIONS -----------------------------------------------------------
def list_categories() -> list:
    """Return all available content categories for AI generation.
    
    Used by AI to understand what types of content can be generated.
    All generation is done by AI, not from static library.
    """
    return list(CATEGORY_META.keys())


def get_category_meta(category: str) -> dict:
    """Return metadata (emoji, style) for a category.

    Args:
        category: Category name (e.g., 'women_professional', 'design_posters')

    Returns:
        Dictionary with emoji and style hint
    """
    return CATEGORY_META.get(category, {"emoji": "🎯", "style": "general use"})


# --- GIFT DESIGN HELPER FUNCTIONS -----------------------------------------------
def list_gift_products() -> list:
    """Return all available gift product types for design generation.
    
    Returns:
        List of product type keys (e.g., ['t_shirt', 'mug', 'hoodie', ...])
    """
    return list(GIFT_PRODUCTS.keys())


def get_gift_product_meta(product_type: str) -> dict:
    """Return metadata for a gift product type.
    
    Args:
        product_type: Product type key (e.g., 't_shirt', 'mug')
    
    Returns:
        Dictionary with emoji, display_name, printable_area, constraints, best_for, tools
    """
    return GIFT_PRODUCTS.get(
        product_type,
        {
            "emoji": "🎁",
            "display_name": "Custom Gift",
            "printable_area": "Variable",
            "constraints": "Varies by product",
            "best_for": "Personalized gifts",
            "tools": ["DALL-E 3", "Midjourney"],
        },
    )


def get_tone_description(tone: str) -> str:
    """Return design tone description.
    
    Args:
        tone: Design tone key (e.g., 'minimalist', 'playful', 'elegant')
    
    Returns:
        Design tone description and characteristics
    """
    return GIFT_DESIGN_TONES.get(tone, "Creative, unique design direction")


def get_all_tones() -> list:
    """Return all available design tones.
    
    Returns:
        List of tone keys available for gift designs
    """
    return list(GIFT_DESIGN_TONES.keys())


# --- ROLE HELPER FUNCTIONS ---------------------------------------------------
def list_professional_roles() -> list:
    """Return all available professional roles.
    
    Returns:
        List of role keys (e.g., ['ui_ux_designer', 'developer', 'marketer', ...])
    """
    return list(PROFESSIONAL_ROLES.keys())


def get_role_metadata(role: str) -> dict:
    """Return metadata for a professional role.
    
    Args:
        role: Role key (e.g., 'ui_ux_designer', 'graphic_designer', 'developer')
    
    Returns:
        Dictionary with emoji, display_name, expertise, guidance, tools, design_focus
    """
    return PROFESSIONAL_ROLES.get(
        role,
        {
            "emoji": "👤",
            "display_name": "Creative Professional",
            "expertise": ["design", "creativity", "visual thinking"],
            "guidance": "Apply professional design principles and best practices for quality output.",
            "tools": ["DALL-E 3", "Midjourney"],
            "design_focus": "Professional-grade design"
        },
    )


def get_role_guidance(role: str) -> str:
    """Return design guidance for a specific professional role.
    
    Args:
        role: Role key (e.g., 'ui_ux_designer', 'graphic_designer')
    
    Returns:
        Guidance text tailored to the role's expertise
    """
    metadata = get_role_metadata(role)
    return metadata.get("guidance", "Apply professional design principles and best practices.")


def get_role_expertise(role: str) -> list:
    """Return expertise areas for a specific professional role.
    
    Args:
        role: Role key (e.g., 'ui_ux_designer', 'marketer')
    
    Returns:
        List of expertise keywords for the role
    """
    metadata = get_role_metadata(role)
    return metadata.get("expertise", [])
