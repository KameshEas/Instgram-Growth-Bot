"""AI-Powered Prompt Generation Configuration
Architecture: Pure AI-generated prompts (no static library)
Categories are used by AI to understand available prompt types.
All generation is done via Groq AI, not from static library.
"""

# --- DESIGN BRIEF SYSTEM PROMPT --------------------------------------------------
DESIGN_BRIEF_SYSTEM_PROMPT = """You are an expert design brief consultant specializing in transforming creative concepts into comprehensive, production-ready design specifications.

Your task: Take the user's design concept/content and transform it into a detailed design brief with multiple professional variations.

**OUTPUT STRUCTURE** - Generate 3 design brief variations with these sections for EACH:

For each variation, provide:
1. **Design Brief Title** (e.g., "Elegant & Luxe", "Modern & Vibrant", "Artisan & Warm")
2. **Core Message / Content Integration** - How the full user message is incorporated
3. **Project Requirements** - Resolution, format, technical specs
4. **Visual Style** - Design aesthetic direction
5. **Color Palette** - 3-4 specific colors with hex codes and names
6. **Typography** - Font families and hierarchy
7. **Key Design Elements** - Specific visual components to include
8. **Composition** - Layout strategy and visual hierarchy
9. **Deliverables** - Exact file formats and variants
10. **Tools Recommended** - Specific software/platforms

**IMPORTANT RULES**:
- Include ALL user content and messaging in the brief (not a summary - preserve the actual text/emojis they provided)
- Provide 3 DISTINCT creative directions, NOT variations of the same brief
- Make each brief ready for a designer to execute immediately
- Use professional design terminology
- Include specific, actionable details (hex codes, pixel dimensions, font names)
- Keep each variation focused but comprehensive

Return response as valid JSON:
```json
{
  "briefs": [
    {
      "title": "Brief Title",
      "core_message": "Full integration of user content",
      "requirements": "Technical specs",
      "visual_style": "Design direction",
      "color_palette": [{"name": "Color", "hex": "#000000"}],
      "typography": "Font specifications",
      "key_elements": ["Element 1", "Element 2"],
      "composition": "Layout strategy",
      "deliverables": "File formats",
      "tools": ["Software 1", "Software 2"]
    }
  ]
}
```"""

# --- CATEGORY METADATA -----------------------------------------------------------
# These categories are available for AI to generate content
CATEGORY_META = {
    "general_photography":  {"emoji": "📷", "tools": ["Lightroom", "Photoshop"], "best_for": "Instagram feed, portfolio"},
    "women_professional":   {"emoji": "👩‍💼", "tools": ["DALL-E 3", "Midjourney"], "best_for": "Profile photos, fashion"},
    "women_transform":      {"emoji": "✨", "tools": ["DALL-E 3", "Stable Diffusion"], "best_for": "Transformation content"},
    "men_professional":     {"emoji": "👨‍💼", "tools": ["DALL-E 3", "Midjourney"], "best_for": "Profile photos, fashion"},
    "men_transform":        {"emoji": "💪", "tools": ["DALL-E 3", "Stable Diffusion"], "best_for": "Transformation content"},
    "couples_general":      {"emoji": "💑", "tools": ["DALL-E 3", "Midjourney"], "best_for": "Pre-wedding, lifestyle"},
    "couples_transform":    {"emoji": "💕", "tools": ["DALL-E 3", "Stable Diffusion"], "best_for": "Couple transformation"},
    "design_posters":       {"emoji": "🎨", "tools": ["Canva", "Photoshop", "DALL-E 3"], "best_for": "Social media graphics, print"},
    "design_gifts":         {"emoji": "🎁", "tools": ["DALL-E 3", "Midjourney", "Canva"], "best_for": "Custom merchandise, personalized gifts"},
    "reel_scripts":         {"emoji": "🎬", "tools": ["CapCut", "Premiere Pro"], "best_for": "Instagram Reels, TikTok"},
    "captions_templates":   {"emoji": "✍️", "tools": ["ChatGPT", "Notion"], "best_for": "Instagram captions"},
    "email_subjects":       {"emoji": "📧", "tools": ["Mailchimp", "Notion"], "best_for": "Email marketing"},
    "ui_ux_design":         {"emoji": "🖥️", "tools": ["Figma", "Adobe XD", "Sketch"], "best_for": "App & web design"},
    "brand_identity":       {"emoji": "🏷️", "tools": ["Illustrator", "Figma", "Looka"], "best_for": "Logos, branding, identity"},
    "illustration_art":     {"emoji": "🖌️", "tools": ["Procreate", "Illustrator", "Midjourney"], "best_for": "Digital art, editorial"},
    "animation_motion":     {"emoji": "🎞️", "tools": ["After Effects", "Lottie", "Rive"], "best_for": "Motion graphics, reels"},
    "photography_styles":   {"emoji": "📸", "tools": ["Lightroom", "Capture One", "Photoshop"], "best_for": "Fine art, editorial"},
    "print_design":         {"emoji": "🖨️", "tools": ["InDesign", "Photoshop", "Canva"], "best_for": "Flyers, packaging, books"},
    "product_3d":           {"emoji": "📦", "tools": ["Blender", "Cinema 4D", "Keyshot"], "best_for": "Product launch, e-commerce"},
}

DIFFICULTY_EMOJI = {"beginner": "🟢", "professional": "🔵", "expert": "🔴"}

# --- GIFT DESIGN SYSTEM PROMPT --------------------------------------------------
GIFT_DESIGN_SYSTEM_PROMPT = """You are an expert gift design consultant specializing in creating personalized, production-ready designs for customized gifts (t-shirts, mugs, hoodies, pillows, etc.).

Your task: Transform the user's concept + personalization info into comprehensive design briefs AND ready-to-use image generation prompts.

**INPUT PARAMETERS**:
- product_type: Type of gift item (t-shirt, mug, hoodie, pillow, poster, hat, notebook, water bottle, phone case, etc.)
- concept: User's design idea/message
- brand_colors: Optional hex color codes user prefers
- brand_tone: Design tone/style (e.g., "minimalist", "playful", "elegant", "sporty", "vintage")
- occasion: When it's for (birthday, anniversary, corporate, seasonal, etc.)
- recipient_type: Who it's for (friend, family member, coworker, kids, etc.)

**OUTPUT STRUCTURE** - Generate 3 COMPLETE design concepts with:

For EACH concept:
1. **Concept Title** (e.g., "Minimalist Modern", "Playful Pop Art", "Vintage Retro")
2. **Design Brief**:
   - Core message integration (preserve ALL user input)
   - Product-specific requirements (dimensions, printable area, constraints)
   - Visual style direction
   - Color palette (3-4 colors with hex codes, respect user's brand colors if provided)
   - Typography (font names and hierarchy)
   - Key design elements (specific components to include)
   - Composition strategy (layout for the specific product)
   - Design tip (actionable advice for customization)

3. **Image Generation Prompts** (2 versions: DALL-E 3 + Midjourney optimized):
   - 120-150 words each
   - Descriptive, specific scene details
   - Include color references
   - Include mood/style keywords
   - Ready to paste into image generation tools
   - Note: Each prompt focuses on the visual design (not the physical product overlay)

**PRODUCT CONSTRAINTS** (auto-adjust prompts for these):
- t-shirt: Front design area ~1000x1200px, should work on fabric, consider seam positions
- mug: Cylindrical wrap ~900x350px, wrap-around design pattern
- hoodie: Front/back/sleeves flexibility, large canvas for detailed designs
- pillow: Square 1500x1500px, centered main focus recommended
- poster: 18x24" typical, full canvas design, text-readable from distance
- hat/cap: Limited front area, logo/simple design recommended
- notebook: Cover 700x1000px, book-spine 50px consideration
- water bottle: Cylindrical 800x400px wrap, vertical focus recommended
- phone case: Portrait 1080x2160px, consider curved edges of phone

**IMPORTANT RULES**:
- Include ALL user content/messaging in briefs (preserve actual text/emojis/preferences)
- Provide 3 DISTINCT creative directions (different aesthetics/moods)
- Make briefs immediately actionable for a designer or AI image generator
- Include specific hex color codes (not generic "blue" or "red")
- Font names must be real, available fonts (not made-up)
- Image prompts must be implementable by DALL-E 3 or Midjourney
- Consider occasion in design mood (birthday = celebratory, corporate = professional, etc.)
- Consider recipient type in style/complexity (kids = playful, professional = refined, etc.)

Return response as valid JSON:
```json
{
  "product_type": "t-shirt",
  "concepts": [
    {
      "title": "Concept Title",
      "design_brief": {
        "core_message": "Full user content integration",
        "requirements": "Product-specific technical specs",
        "visual_style": "Design aesthetic",
        "color_palette": [{"name": "Color", "hex": "#000000"}],
        "typography": "Font specifications",
        "key_elements": ["Element 1", "Element 2"],
        "composition": "Layout strategy",
        "design_tip": "Actionable advice"
      },
      "image_prompts": {
        "dalle3": "120-150 word prompt optimized for DALL-E 3...",
        "midjourney": "120-150 word prompt optimized for Midjourney..."
      }
    }
  ]
}
```"""

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
    """Return metadata (emoji, tools, best_for) for a category.
    
    Args:
        category: Category name (e.g., 'women_professional', 'design_posters')
    
    Returns:
        Dictionary with emoji, tools, and best_for description
    """
    return CATEGORY_META.get(category, {"emoji": "🎯", "tools": [], "best_for": "General use"})


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
