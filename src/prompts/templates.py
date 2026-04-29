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
